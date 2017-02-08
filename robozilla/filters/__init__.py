from robozilla.filters.decorator import BZDecorator  # noqa
from robozilla.filters.isopen import BZIsOpen  # noqa


reg = {
    'decorator': BZDecorator,
    'function': BZIsOpen
}

_names_separator = ','


def get_filters(name):
    name = name.strip()
    if name == 'all':
        return list(reg.values())
    else:
        if name in reg:
            return [reg[name]]
        else:
            # try to see if it's a list with a separator
            if _names_separator in name:
                names = name.split(_names_separator)
                list_filters = []
                for fil_name in names:
                    fil = get_filters(fil_name)
                    if fil:
                        list_filters += fil
                if list_filters:
                    return list_filters

    return None
