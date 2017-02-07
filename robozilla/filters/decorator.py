from robozilla.filters.base import Base


class BZDecorator(Base):
    name = 'skip_if_bug_open'
    find_string = "@skip_if_bug_open("
    re_pattern = ("@skip_if_bug_open\( *(?:\'bugzilla\'|\"bugzilla\")"
                  " *, *(?:\'|\")*([0-9]+)(?:\'|\")* *\)")
