import re


class Base(object):
    name = 'generic'
    find_string = None
    # default pattern
    re_pattern = "[0-9]{7}"
    _re_compiled = None
    _re_flags = 0

    @classmethod
    def is_string_present(cls, text):
        if cls.find_string and cls.find_string in text:
            return True

        return False

    @classmethod
    def _get_compiled_re(cls):
        if not cls._re_compiled:
            cls._re_compiled = re.compile(cls.re_pattern, cls._re_flags)

        return cls._re_compiled

    @classmethod
    def retrieve(cls, text):
        bug_ids = []
        if cls.find_string and not cls.is_string_present(text):
            return bug_ids

        if cls.re_pattern:
            bug_ids = cls._get_compiled_re().findall(text)

        return bug_ids
