
import copy

import bugzilla

# to do handle errors
from six.moves.xmlrpc_client import Fault
from xml.parsers.expat import ExpatError, ErrorString

BUGZILLA_URL = "https://bugzilla.redhat.com/xmlrpc.cgi"

# class BugFetchError(Exception):
#     """Indicates an error occurred while fetching information about a bug."""


class BZReader(object):

    default_include_fields = ['id', 'status', 'resolution']

    def __init__(self):
        self._cache = {}
        self._connection = None

    def _get_connetion(self):
        # bz_credentials to be defined, for the moment connect as anonymous
        if not self._connection:
            bz_credentials = {}
            bz_conn = bugzilla.RHBugzilla(**bz_credentials)
            bz_conn.connect(BUGZILLA_URL)
            self._connection = bz_conn
        return self._connection

    def get_state(self, bug_id):
        bug_data = self._cache.get(bug_id, None)
        if not bug_data:
            bz_conn = self._get_connetion()
            try:
                bug = bz_conn.getbug(
                    bug_id,
                    include_fields=self.default_include_fields
                )
                bug_data = {}
                for field in self.default_include_fields:
                    bug_data[field] = getattr(bug, field)

                self._cache[bug_id] = bug_data

            except (ExpatError, ErrorString, Fault):
                # to handle this
                pass

        return bug_data

    def bugs_status(self):
        return copy.deepcopy(self._cache)





