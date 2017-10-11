
import os
from robozilla.bz import BZReader

this_path = os.path.abspath(os.path.dirname(__file__))
files_path = os.path.join(this_path, 'files')


class BZReaderForTest(BZReader):

    _cache_data = None

    def __init__(self, *args, **kwargs):
        super(BZReaderForTest, self).__init__(*args, **kwargs)
        if self._cache_data is not None:
            self.set_cache(self._cache_data)

    def _get_connection(self):
        """This object has not to connect to bugzilla, work only with cache"""
        return None

    def get_bug_data_in_bulk(self, bugs):
        bugs_data = {}
        for bug_id in bugs:
            bugs_data[bug_id] = self.get_bug_data(bug_id)

        return bugs_data

    def set_cache(self, data):
        self._cache = data
