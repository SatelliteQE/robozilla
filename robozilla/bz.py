import copy
import logging
from collections import defaultdict
import os
from xml.parsers.expat import ExpatError, ErrorString

import bugzilla
import fnmatch
from six.moves.xmlrpc_client import Fault

from robozilla.constants import (
    BUGZILLA_ENVIRON_USER_NAME,
    BUGZILLA_ENVIRON_USER_PASSWORD_NAME,
    BUGZILLA_QUERY_PRODUCT,
    BUGZILLA_URL,
    DEFAULT_INCLUDE_FIELDS,
    DUPLICATES_FIELD,
    CLONES_FIELD,
    DEPENDENT_FIELD
)

logger = logging.Logger(__name__)


def _filter_none(lst):
    """Filter None values out of lst

    :param lst: list to be filtered
    :return: generator filtering Nones
    """

    return filter(lambda value: value is not None, lst)


class BZReader(object):
    _flags_fields = ('name', 'status')
    _flags_force_include = []
    _flags_key_filters = ['sat-*']
    _always_use_all_fields = True

    def __init__(self,
                 credentials=None,
                 include_fields=None,
                 follow_duplicates=False,
                 follow_clones=False,
                 follow_depends=True
                 ):

        if credentials is None:
            credentials = {}

        if not credentials:
            if BUGZILLA_ENVIRON_USER_NAME in os.environ:
                credentials['user'] = os.environ[
                    BUGZILLA_ENVIRON_USER_NAME]

            if BUGZILLA_ENVIRON_USER_PASSWORD_NAME in os.environ:
                credentials['password'] = os.environ[
                    BUGZILLA_ENVIRON_USER_PASSWORD_NAME]

        self.credentials = credentials or {}
        self._cache = {}
        self._connection = None

        self.include_fields = include_fields or DEFAULT_INCLUDE_FIELDS
        self.follow_duplicates = follow_duplicates
        self.follow_clones = follow_clones
        self.follow_depends = follow_depends

        if self.follow_clones and CLONES_FIELD not in self.include_fields:
            self.include_fields.append(CLONES_FIELD)
        # DUPLICATES_FIELD is not included because it depends on `resolution`
        if self.follow_depends and DEPENDENT_FIELD not in self.include_fields:
            self.include_fields.append(DEPENDENT_FIELD)

        # To hold the id that started the call
        # also all already processed ids
        # and avoid circular infinite loops
        self.root_bug_id = None
        self.processed_bugs = []

    def _get_query_include_fields(self):
        if self._always_use_all_fields:
            # always return a copy of the list
            return list(self.include_fields)
        return [
            field for field in self.include_fields
            if field not in [DUPLICATES_FIELD, CLONES_FIELD, DEPENDENT_FIELD]
        ]

    def _get_connection(self):
        if not self._connection:
            bz_conn = bugzilla.RHBugzilla(url=BUGZILLA_URL, **self.credentials)
            self._connection = bz_conn
        return self._connection

    def _get_clones(self, bug_ids):
        """return a list of bugzilla bugs that are cloned from bug_ids"""
        include_fields = self._get_query_include_fields()
        if CLONES_FIELD not in include_fields:
            include_fields += [CLONES_FIELD]
        bz_conn = self._get_connection()
        query = bz_conn.build_query(product=BUGZILLA_QUERY_PRODUCT,
                                    include_fields=include_fields)
        query['bug_id_type'] = 'anyexact'
        query[CLONES_FIELD] = bug_ids
        return _filter_none(bz_conn.query(query))

    def get_bug_data_in_bulk(self, bugs, include_fields=None):
        """Get bug_data in bulk by given chunk in bugs
        bugs: a list of ids"""
        bz_conn = self._get_connection()
        include_fields = include_fields or self._get_query_include_fields()
        # To follow duplicates in bulk mode `dupe_of` must be part of
        # include_fields list
        result_bugs = list(_filter_none(
            bz_conn.getbugs(bugs, include_fields=include_fields)))
        chunk_data = {}
        # create a dict of bug id clones bugs
        bugs_clones = defaultdict(list)
        if self.follow_clones:
            for c_bug in self._get_clones(bugs):
                bug_id = getattr(c_bug, CLONES_FIELD)
                c_bug_data = self.set_bug_data_fields(
                    c_bug, base_data_only=True)
                bugs_clones[bug_id].append(c_bug_data)

        for bug in result_bugs:
            bug_clones_data = bugs_clones.get(bug.id, [])
            bug_data = self.set_bug_data_fields(
                bug, bugs_clones_data=bug_clones_data)
            chunk_data[bug_data['id']] = bug_data

        bugs_not_returned = set(bugs).difference(
            {
                str(bug.id) for bug in result_bugs
            }
        )

        if bugs_not_returned:
            logging.warning('objects for bugs ids not received {}'.format(
                bugs_not_returned))

        return chunk_data

    def get_bug_data(self, bug_id, include_fields=None, use_cacke=True):
        """Get data for a single bug_id"""
        if not bug_id:
            return

        if self.root_bug_id is None:
            self.root_bug_id = bug_id

        self.processed_bugs.append(bug_id)

        include_fields = include_fields or self.include_fields[:]
        bug_data = self._cache.get(str(bug_id))
        if not bug_data or not use_cacke:
            bz_conn = self._get_connection()
            try:
                bug = bz_conn.getbug(
                    bug_id,
                    include_fields=include_fields
                )

                if self.follow_duplicates and getattr(bug, 'resolution') == 'DUPLICATE':  # noqa
                    # in case of a DUPLICATE, call again taking the dupes
                    # but only if self.follow_duplicates is True
                    inc_fields = include_fields[:]  # avoid shadowing
                    if DUPLICATES_FIELD not in inc_fields:
                        inc_fields.append(DUPLICATES_FIELD)
                    bug = bz_conn.getbug(
                        bug_id,
                        include_fields=inc_fields
                    )

                if bug is not None:
                    bug_clones_data = []
                    if self.follow_clones:
                        bug_clones_data = [
                            self.set_bug_data_fields(
                                clone_bug, base_data_only=True)
                            for clone_bug in self._get_clones([bug_id])
                        ]
                    bug_data = self.set_bug_data_fields(
                        bug, bugs_clones_data=bug_clones_data)

            except ErrorString as error:
                logger.warning(
                    'Could not interpret bug. Error: {0}'.format(error)
                )
            except Fault as error:
                logger.warning(
                    'Could not fetch bug. Error: {0}'.format(error.faultString)
                )
            except ExpatError as error:
                logger.warning(
                    'Could not interpret bug. Error: {0}'.format(
                        ErrorString(error.code)
                    )
                )
        return bug_data

    def set_bug_data_fields(self, bug, bugs_clones_data=None,
                            base_data_only=False):
        """Get a bug object and returns a dict
        containing included_fields and flags and also
        add extra fields getting relations as dupes or
        clones"""
        if bugs_clones_data is None:
            bugs_clones_data = []

        bug_data = {}

        include_fields = self.include_fields[:]
        if self.follow_duplicates and getattr(bug, 'resolution') == 'DUPLICATE':  # noqa
            include_fields.append(DUPLICATES_FIELD)

        for field in include_fields:
            if field in bug.__dict__:
                # field can exist with hasattr(bug, field), but not returned
                # by getattr, and if we use getattr(bug, field, None)
                # this will make a request to bugzilla, forcing use to waste
                # time inutilly
                field_data = getattr(bug, field)
            else:
                # some fields are not returned if they are None
                # any way if it's not here it's a None
                # this reduce the time by x20
                field_data = None
            if field == 'flags' and self._flags_fields:
                flags_data = {}
                flags = field_data if field_data is not None else []
                for flag_entry in flags:
                    key_name, value_name = self._flags_fields
                    key = flag_entry.get(key_name, '')
                    value = flag_entry.get(value_name, '')
                    if key:
                        if self._flags_key_filters:
                            for key_filter in self._flags_key_filters:
                                if fnmatch.fnmatch(key, key_filter):
                                    flags_data[key] = value
                                    break
                        else:
                            flags_data[key] = value

                bug_data[field] = flags_data
            else:
                bug_data[field] = field_data

        status = bug_data.get('status')
        if status is not None:
            bug_data['status_resolution'] = status
            resolution = bug_data.get('resolution')
            if resolution is not None:
                bug_data['status_resolution'] = '{0}_{1}'.format(
                    status,
                    resolution
                )

        if not base_data_only:
            # getting dupes and clones are expensive and makes the elapsed time
            # to be 20x slow so they are by default disabled
            if self.follow_duplicates:
                dupe_of = bug_data.get(DUPLICATES_FIELD)
                if dupe_of and dupe_of not in self.processed_bugs:
                    bug_data['duplicate_of'] = self.get_bug_data(
                        bug_data[DUPLICATES_FIELD],
                        use_cacke=False
                    )
                else:
                    bug_data['duplicate_of'] = None

            if (CLONES_FIELD in self.include_fields and
                    self.follow_clones):
                cf_clone_of = bug_data.get(CLONES_FIELD)
                if cf_clone_of and cf_clone_of not in self.processed_bugs:
                    bug_data['clone_of'] = self.get_bug_data(cf_clone_of)
                else:
                    bug_data['clone_of'] = None

            if (DEPENDENT_FIELD in self.include_fields and
                    self.follow_depends):
                depends_on = [
                    dep_id for dep_id in
                    bug_data.get(DEPENDENT_FIELD, [])
                    if dep_id not in self.processed_bugs
                ]
                if depends_on:
                    bug_data['dependent_on'] = []
                    for depend_on in depends_on:
                        bug_data['dependent_on'].append(
                            self.get_bug_data(depend_on))
                else:
                    bug_data['dependent_on'] = None

        bug_data['clones'] = [
            bug_clone_data for bug_clone_data in bugs_clones_data]

        str_bug_id = str(bug.id)
        other_clones = {}

        def add_to_other_clones(data):
            if data['id'] not in other_clones and data['id'] != str_bug_id:
                other_clones[data['id']] = data

        bug_clone_of_data = bug_data.get('clone_of')
        if bug_clone_of_data:
            add_to_other_clones(bug_clone_of_data)
            for bug_clone_of_clone in bug_clone_of_data.get('clones', []):
                add_to_other_clones(bug_clone_of_clone)

        for bug_clone_data in bug_data['clones']:
            add_to_other_clones(bug_clone_data)

        bug_data['other_clones'] = other_clones

        bug_data['id'] = str_bug_id
        self._cache[str_bug_id] = bug_data
        return bug_data

    def bugs_status(self):
        return copy.deepcopy(self._cache)
