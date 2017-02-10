
import copy
import fnmatch
import os

import bugzilla

# to do handle errors
from six.moves.xmlrpc_client import Fault
from xml.parsers.expat import ExpatError, ErrorString

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
        if self.follow_duplicates and (
                    DUPLICATES_FIELD not in self.include_fields):
            self.include_fields.append(DUPLICATES_FIELD)
        if self.follow_depends and DEPENDENT_FIELD not in self.include_fields:
            self.include_fields.append(DEPENDENT_FIELD)

    def _get_query_include_fields(self):
        if self._always_use_all_fields:
            return self.include_fields
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
        return bz_conn.query(query)

    def get_bug_data_in_bulk(self, bugs):
        """Get bug_data in bulk by given chunk in bugs
        bugs: a list of ids"""
        bz_conn = self._get_connection()
        include_fields = self._get_query_include_fields()
        result_bugs = bz_conn.getbugs(bugs, include_fields=include_fields)
        chunk_data = {}
        # create a dict of bug id clones bugs
        bugs_clones = {}
        if self.follow_clones:
            for c_bug in self._get_clones(bugs):
                bug_id = getattr(c_bug, CLONES_FIELD)
                c_bug_data = self.set_bug_data_fields(c_bug,
                                                      base_data_only=True)
                if bug_id in bugs_clones:
                    bugs_clones[bug_id].append(c_bug_data)
                else:
                    bugs_clones[bug_id] = [c_bug_data]

        for bug in result_bugs:
            bug_clones_data = bugs_clones.get(bug.id, [])
            bug_data = self.set_bug_data_fields(
                bug, bugs_clones_data=bug_clones_data)
            chunk_data[bug_data['id']] = bug_data
        return chunk_data

    def get_bug_data(self, bug_id):
        """Get data for a single bug_id"""
        bug_data = self._cache.get(str(bug_id))
        if not bug_data:
            bz_conn = self._get_connection()
            try:
                bug = bz_conn.getbug(
                    bug_id,
                    include_fields=self.include_fields
                )
                bug_clones_data = []
                if self.follow_clones:
                    bug_clones_data = [
                        self.set_bug_data_fields(
                            clone_bug, base_data_only=True)
                        for clone_bug in self._get_clones([bug_id])
                    ]
                bug_data = self.set_bug_data_fields(
                    bug, bugs_clones_data=bug_clones_data)

            except (ExpatError, ErrorString, Fault):
                # to handle this
                pass

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
        for field in self.include_fields:
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

        if bug_data['resolution']:
            bug_data['status_resolution'] = '{0}_{1}'.format(
                bug_data['status'],
                bug_data['resolution']
            )
        else:
            bug_data['status_resolution'] = bug_data['status']

        if not base_data_only:
            # getting dupes and clones are expensive and makes the elapsed time
            # to be 20x slow so they are by default disabled
            if (DUPLICATES_FIELD in self.include_fields and
                    self.follow_duplicates):
                if bug_data[DUPLICATES_FIELD]:
                    bug_data['duplicate_of'] = self.get_bug_data(
                        bug_data[DUPLICATES_FIELD])
                else:
                    bug_data['duplicate_of'] = None

            if (CLONES_FIELD in self.include_fields and
                    self.follow_clones):
                if bug_data[CLONES_FIELD]:
                    bug_data['clone_of'] = self.get_bug_data(
                        bug_data[CLONES_FIELD])
                else:
                    bug_data['clone_of'] = None

            if (DEPENDENT_FIELD in self.include_fields and
                    self.follow_depends):
                if bug_data[DEPENDENT_FIELD]:
                    bug_data['dependent_on'] = []
                    for depend_on in bug_data[DEPENDENT_FIELD]:
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

        bug_clone_of_data = bug_data.get('clone_of', None)
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
