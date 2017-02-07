from robozilla.filters.base import Base


class BZIsOpen(Base):
    name = 'bz_bug_is_open'
    find_string = "bz_bug_is_open("
    re_pattern = "bz_bug_is_open\( *(?:\'|\")*([0-9]+)(?:\'|\")* *\)"
