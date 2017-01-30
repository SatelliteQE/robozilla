from __future__ import print_function
import re


class Base(object):
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
    def re_retrieve(cls, text):
        bug_ids = []
        if cls.re_pattern:
            bug_ids = cls._get_compiled_re().findall(text)
        return bug_ids


class BZDecorator(Base):
    find_string = "@skip_if_bug_open("
    re_pattern = ("@skip_if_bug_open\( *(?:\'bugzilla\'|\"bugzilla\")"
                  " *, *([0-9]{7}) *\)")


class BZIsOpen(Base):
    find_string = "bz_bug_is_open("
    re_pattern = "bz_bug_is_open\( *([0-9]{7}) *\)"
