from unittest import TestCase

from robozilla.query.exp import decode_exp_unit, decode_exp_list


class QueryExpTestCase(TestCase):

    def test_is_empty(self):
        a = decode_exp_unit('flagtypes.name[]')
        self.assertDictEqual(a, {'o': 'isempty', 'f': 'flagtypes.name'})

    def test_is_not_empty(self):
        a = decode_exp_unit('flagtypes.name![]')
        self.assertDictEqual(a, {'o': 'isnotempty', 'f': 'flagtypes.name'})

    def test_case_sub_string(self):
        exp_dict = decode_exp_unit('component!~~Doc')
        self.assertDictEqual(
            exp_dict,
            {'f': 'component',
             'o': 'casesubstring',
             'v': 'Doc',
             'n': '1',
             }
        )

    def test_case_sub_string_ne(self):
        exp_dict = decode_exp_unit('component!~~Doc')
        self.assertDictEqual(
            exp_dict,
            {'f': 'component',
             'o': 'casesubstring',
             'v': 'Doc',
             'n': '1',
             }
        )

    def test_case_sub_string_ne_with_escape(self):
        exp_dict = decode_exp_unit(r'component!~~Doc\~~')
        self.assertDictEqual(
            exp_dict,
            {'f': 'component',
             'o': 'casesubstring',
             'v': r'Doc~~',
             'n': '1',
             }
        )


class QueryExpListTestCase(TestCase):

    def test_is_empty_and_contain(self):
        exp_text = 'flagtypes.name[],flagtypes.name~sat-6.2'
        value = decode_exp_list(exp_text)
        self.assertIsInstance(value, list)
        self.assertEqual(len(value), 2)
        operators = {exp.get('o') for exp in value}
        self.assertEqual(operators, {'isempty', 'substring'})
        asserted_opr = []
        for exp in value:
            opr = exp['o']
            if opr == 'substring':
                self.assertDictEqual(
                    exp,
                    {'v': 'sat-6.2', 'o': 'substring', 'f': 'flagtypes.name'}
                )
                asserted_opr.append('substring')
            elif opr == 'isempty':
                self.assertDictEqual(
                    exp,
                    {'o': 'isempty', 'f': 'flagtypes.name'}
                )
                asserted_opr.append('isempty')
        self.assertEqual(set(asserted_opr), operators)

    def test_is_empty_and_contain_with_escape(self):
        # escape the list separator and the compare operator in value
        exp_text = r'flagtypes.name[],flagtypes.name~sat-6\,2\~'
        value = decode_exp_list(exp_text)
        # the value should looks like:
        # [
        #  {'o': 'isempty', 'f': 'flagtypes.name'},
        #  {'v': 'sat-6,2~', 'o': 'substring', 'f': 'flagtypes.name'}
        # ]
        self.assertIsInstance(value, list)
        self.assertEqual(len(value), 2)
        operators = {exp.get('o') for exp in value}
        self.assertEqual(operators, {'isempty', 'substring'})
        asserted_opr = []
        for exp in value:
            opr = exp['o']
            if opr == 'substring':
                self.assertDictEqual(
                    exp,
                    {'v': 'sat-6,2~', 'o': 'substring', 'f': 'flagtypes.name'}
                )
                asserted_opr.append('substring')
            elif opr == 'isempty':
                self.assertDictEqual(
                    exp,
                    {'o': 'isempty', 'f': 'flagtypes.name'}
                )
                asserted_opr.append('isempty')
        self.assertEqual(set(asserted_opr), operators)
