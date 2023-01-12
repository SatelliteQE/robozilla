"""
  all compare strings, the
  note : with * supported
    * equals : is equal to
    * notequals : is not equal to
    * anyexactis : equal to any of the strings
    * substring : contains the string
    * casesubstring : contains the string (exact case)
    * notsubstring : does not contain the string

    * anywordssubstr : contains any of the strings
    * allwordssubstr : contains all of the strings
    * nowordssubstr : contains none of the strings
    regexp : matches regular expression
    notregexp : does not match regular expression
    * lessthan : is less than
    * lessthaneq : is less than or equal to
    * greaterthan : is greater than
    * greaterthaneq : is greater than or equal to
    * anywords : contains any of the words
    * allwords : contains all of the words
    * nowords : contains none of the words
    changedbefore : changed before
    changedafter : changed after
    changedfrom : changed from
    changedto : changed to
    changedby : changed by
    matches : maches
    notmatches : does not match
    * isempty : is empty
    * isnotempty : is not empty

"""
from collections import OrderedDict

FIELDS_ALIAS = {
    'start_date': 'chfieldfrom',
    'end_date': 'chfieldto',
    'flag_name': 'flagtypes.name'
}

EXP_LIST_SEPARATOR = ','
EXP_ESCAPE_STR = '\\'
EXP_TEMP_ESCAPE_STR = '-@@_$_escape_separator_$_@@@-'

NEGATION_STR = '!'

COMPARE_STRINGS = [
    ('=', 'equals'),
    ('!=', 'notequals'),
    ('~[==]', 'anyexactis'),
    ('~~', 'casesubstring'),
    ('!~', 'notsubstring'),
    ('~', 'substring'),

    ('~[~]', 'anywordssubstr'),
    ('=[~]', 'allwordssubstr'),
    ('![~]', 'nowordssubstr'),

    ('<', 'lessthan'),
    ('<=', 'lessthaneq'),
    ('=<', 'lessthaneq'),
    ('>', 'greaterthan'),
    ('>=', 'greaterthaneq'),
    ('=>', 'greaterthaneq'),

    ('~[=]', 'anywords'),
    ('=[=]', 'allwords'),
    ('![=]', 'nowords'),
    ('![]', 'isnotempty'),
    ('[]', 'isempty'),
]


class NoCompareStringNotFoundError(Exception):
    """compare string not found Error"""


def _escape_get_string(string_to_be_escaped):
    return '{0}{1}'.format(EXP_ESCAPE_STR, string_to_be_escaped)


def _escape_string_to_temp(string_to_be_escaped, text):
    escape_string = _escape_get_string(string_to_be_escaped)
    if escape_string in text:
        return text.replace(escape_string, EXP_TEMP_ESCAPE_STR)

    return text


def _escape_restore_string(string_to_be_escaped, text):
    if EXP_TEMP_ESCAPE_STR in text:
        return text.replace(EXP_TEMP_ESCAPE_STR,
                            string_to_be_escaped)
    else:
        return text


def decode_exp_unit(text, raise_not_found=True):
    """ return a dict with keys f, v, o , n
    :type text: str
    :type raise_not_found: bool
    :returns: dict
    """
    value = {}
    if not text:
        return value
    cmp_str_found = False
    for cmp_str, cmp_value in COMPARE_STRINGS:
        text = _escape_string_to_temp(cmp_str, text)
        if cmp_str in text:
            cmp_str_found = True
            ops = text.split(cmp_str)
            # get the field
            negation = None
            field_op = cmp_value
            field_op_value = ''

            if len(ops) > 0:
                field = ops[0]
                if field.endswith(NEGATION_STR):
                    negation = True
                    # remove the negation from field
                    field = field[:-len(NEGATION_STR)]

                if len(ops) > 1:
                    field_op_value = ops[1]

                if field:
                    value['f'] = _escape_restore_string(cmp_str,
                                                        field.strip(' '))
                    value['o'] = _escape_restore_string(cmp_str,
                                                        field_op.strip(' '))
                    if field_op_value:
                        value['v'] = _escape_restore_string(cmp_str,
                                                            field_op_value)
                    if negation is True:
                        value['n'] = '1'

            break

    if raise_not_found and not cmp_str_found:
        raise NoCompareStringNotFoundError(
            'No compare string found in: {}'.format(text))

    return value


def decode_exp_list(text):
    """return a list of exp
    :type text: str
    :returns: List[dict]
    """
    value = []
    if not text:
        return value

    text = _escape_string_to_temp(EXP_LIST_SEPARATOR, text)

    if EXP_LIST_SEPARATOR in text:
        exp_list = text.split(EXP_LIST_SEPARATOR)
    else:
        exp_list = [text]
    for exp_text in exp_list:
        exp_text = _escape_restore_string(EXP_LIST_SEPARATOR, exp_text)
        exp = decode_exp_unit(exp_text)
        value.append(exp)

    return value


def decode_groups(include_all='', include_any='', **kwargs):
    # I should have three groups
    # include_from_kwargs AND (include_any with OR ) AND
    # (exclude_text with OR )
    query = OrderedDict()
    # get the kwargs first
    for key, value in kwargs.items():
        key_alias = FIELDS_ALIAS.get(key)
        if key_alias:
            key = key_alias
        query[key] = value

    groups = {'AND': include_all, 'OR': include_any}

    def add_query_field(index, field_data):
        f = field_data.get('f')
        f_alias = FIELDS_ALIAS.get(f)
        if f_alias:
            f = f_alias
        query['f{}'.format(index)] = f
        o = field_data.get('o')
        query['o{}'.format(index)] = o
        v = field_data.get('v')
        if v is not None:
            query['v{}'.format(index)] = v

        n = field_data.get('n')
        if n:
            query['n{}'.format(index)] = n

    field_index = 0
    for op_j, value in groups.items():
        group_dicts = decode_exp_list(value)

        field_index += 1
        query['f{}'.format(field_index)] = 'OP'
        query['j{}'.format(field_index)] = op_j

        for group_dict in group_dicts:
            field_index += 1
            add_query_field(field_index, group_dict)

        field_index += 1
        query['f{}'.format(field_index)] = 'CP'

    return query
