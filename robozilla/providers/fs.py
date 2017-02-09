import fnmatch
import os

from robozilla.constants import FILE_NAME_PATTERN


class FilesProvider(object):

    def __init__(self, root_folder_path):

        if not os.path.exists(root_folder_path):
            raise IOError('path does not exist: {0}'.format(root_folder_path))

        self._scan_path = root_folder_path

    def get_files(self, scan_path=None):
        if scan_path is None:
            scan_path = self._scan_path
        if os.path.isfile(scan_path):
            if fnmatch.fnmatch(scan_path, FILE_NAME_PATTERN):
                yield scan_path

        else:
            for name in sorted(os.listdir(scan_path)):
                full_path = os.path.join(scan_path, name)
                if os.path.isdir(full_path):
                    for file_path in self.get_files(full_path):
                        yield file_path
                elif os.path.isfile(full_path):
                    if fnmatch.fnmatch(full_path, FILE_NAME_PATTERN):
                        yield full_path
                else:
                    pass
