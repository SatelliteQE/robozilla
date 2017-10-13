
from robozilla.parser import Parser

from .base import BZReaderForTest, files_path
from .data import cache_data


def test_parse_simple():
    bugs_set = {'1123360', '1405428', '1402826', '1328925', '1333805',
                '1219610', '1461026'}

    bz_reader = BZReaderForTest()
    bz_reader.set_cache(cache_data)
    parser = Parser(files_path, bz_reader=bz_reader)

    bugs_data = parser.get_bugs_status()

    assert bugs_set == set(bugs_data.keys())


if __name__ == '__main__':
    test_parse_simple()
