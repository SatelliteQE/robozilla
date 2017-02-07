import os
import sys

from robozilla.parser import Parser
from robozilla.constants import DEFAULT_INCLUDE_FIELDS


def main():
    _current_environment_path = os.path.realpath(os.path.curdir)
    scan_dir = _current_environment_path
    print(_current_environment_path)

    if len(sys.argv) > 1:
        scan_dir = sys.argv[1]
    else:
        pass

    parser = Parser(
        scan_dir,
        filters=None,
        reporter=None,
        bz_reader=None,
        environment=None,
        reader_options={
            'follow_duplicates': True,
            'include_fields': DEFAULT_INCLUDE_FIELDS + ['dupe_of']
        }
    )
    parser.parse(report=True)


if __name__ == '__main__':
    main()
