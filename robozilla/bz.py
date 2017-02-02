
import copy
import os

import bugzilla

# to do handle errors
from six.moves.xmlrpc_client import Fault
from xml.parsers.expat import ExpatError, ErrorString

from robozilla.constants import (
    BUGZILLA_ENVIRON_USER_NAME,
    BUGZILLA_ENVIRON_USER_PASSWORD_NAME,
    BUGZILLA_URL
)


class BZReader(object):

    include_fields = ['id', 'status', 'whiteboard', 'resolution', 'flags']
    _flags_fields = ('name', 'status')
    _exclude_flags = []

    def __init__(self, credentials=None):
        if credentials is None:
            credentials = {}
            if BUGZILLA_ENVIRON_USER_NAME in os.environ:
                credentials['user'] = os.environ[
                    BUGZILLA_ENVIRON_USER_NAME]

            if BUGZILLA_ENVIRON_USER_PASSWORD_NAME in os.environ:
                credentials['password'] = os.environ[
                    BUGZILLA_ENVIRON_USER_PASSWORD_NAME]

        self.credentials = credentials
        self._cache = {}
        self._connection = None

    def _get_connection(self):
        # bz_credentials to be defined, for the moment connect as anonymous
        if not self._connection:
            bz_conn = bugzilla.RHBugzilla(**self.credentials)
            bz_conn.connect(BUGZILLA_URL)
            self._connection = bz_conn
        return self._connection

    def get_bug_data(self, bug_id):
        bug_data = self._cache.get(bug_id, None)
        if not bug_data:
            bz_conn = self._get_connection()
            try:
                bug = bz_conn.getbug(
                    bug_id,
                    # include_fields=self.include_fields
                )
                bug_data = {}
                for field in self.include_fields:
                    if field == 'flags':
                        flags_data = {}
                        flags = getattr(bug, field, [])
                        for flag_entry in flags:
                            key_name, value_name = self._flags_fields
                            key = flag_entry.get(key_name, '')
                            if key:
                                flags_data[key] = flag_entry.get(
                                    value_name, '')

                        bug_data[field] = flags_data
                    else:
                        bug_data[field] = getattr(bug, field)

                self._cache[bug_id] = bug_data

            except (ExpatError, ErrorString, Fault):
                # to handle this
                pass

        return bug_data

    def bugs_status(self):
        return copy.deepcopy(self._cache)
