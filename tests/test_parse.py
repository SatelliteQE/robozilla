
from unittest import TestCase

from robozilla.parser import Parser

import base


class ParserTestCase(TestCase):

    def test_parse_simple(self):

        parser = Parser(base.files_path)
        bugs_data = parser.get_bugs_status()
        parser.parse(report=False)

        self.assertEqual(base.bugs_set, set(bugs_data.keys()))




