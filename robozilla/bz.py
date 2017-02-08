
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

    def _get_connection(self):
        # bz_credentials to be defined, for the moment connect as anonymous
        if not self._connection:
            bz_conn = bugzilla.RHBugzilla(**self.credentials)
            bz_conn.connect(BUGZILLA_URL)
            self._connection = bz_conn
        return self._connection

    def get_bug_data_in_bulk(self, bugs):
        """Get bug_data in bulk by given chunk in bugs
        bugs: a list of ids"""
        bz_conn = self._get_connection()
        include_fields = [
            field for field in self.include_fields
            if field not in ['dupe_of']
        ]
        result = bz_conn.getbugs(bugs, include_fields=include_fields)
        chunk_data = {}
        for data in result:
            bug_data = self.set_bug_data_fields(data)
            chunk_data[bug_data['id']] = bug_data
        return chunk_data

    def get_bug_data(self, bug_id):
        """Get data for a single bug_id"""
        bug_data = self._cache.get(bug_id)
        if not bug_data:
            bz_conn = self._get_connection()
            try:
                bug = bz_conn.getbug(
                    bug_id,
                    include_fields=self.include_fields
                )
                bug_data = self.set_bug_data_fields(bug)

            except (ExpatError, ErrorString, Fault):
                # to handle this
                pass

        return bug_data

    def set_bug_data_fields(self, bug):
        """Get a bug object and returns a dict
        containing included_fields and flags and also
        add extra fields getting relations as dupes or
        clones"""
        bug_data = {}
        for field in self.include_fields:
            if field == 'flags' and self._flags_fields:
                flags_data = {}
                flags = getattr(bug, field, [])
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
                bug_data[field] = getattr(bug, field, None)

        if bug.resolution:
            bug_data['status_resolution'] = '{0}_{1}'.format(
                bug.status,
                bug.resolution
            )
        else:
            bug_data['status_resolution'] = bug.status

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

        bug_data['id'] = str(bug.id)
        self._cache[bug_data['id']] = bug_data
        return bug_data

    def bugs_status(self):
        return copy.deepcopy(self._cache)
