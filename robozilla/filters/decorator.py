from robozilla.filters.base import Base


class BZDecorator(Base):
    name = 'skip_if_bug_open'
    find_string = "@skip_if_bug_open("
    re_pattern = (r"@skip_if_bug_open\( *(?:\'bugzilla\'|\"bugzilla\")"
                  r" *, *(?:\'|\")*([0-9]+)(?:\'|\")* *\)")
