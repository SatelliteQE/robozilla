
import os

from robozilla.bz import BZReader

this_path = os.path.abspath(os.path.dirname(__file__))
files_path = os.path.join(this_path, 'files')

bugs_set = {'1123360', '1405428', '1402826', '1328925', '1333805', '1219610'}
# , 981639, 1372372
_cache_data = dict()


class BZReaderForTest(BZReader):

    def _get_connection(self):
        """This object has not to connect to bugzilla, work only with cache"""
        return None

    def set_cache(self, data):
        self._cache = data
