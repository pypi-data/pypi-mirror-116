import datetime
import decimal
from collections import namedtuple

from essencia.settings import SEPARATOR
from essencia.enum.string import EnumStr
from essencia.enum.integer import EnumInt


def is_dunder(string: str):
    return True if string.startswith("_") and string.endswith("_") else False


def is_public(string: str):
    return True if not string.startswith("_") else False


def is_private(string: str):
    return True if string.startswith("_") and not string.endswith("_") else False


def make_private(string: str):
    return f'_{string}' if is_public(string) else string


def unprivate(string: str):
    return string[ 1: ] if is_private(string) else string


def unprivate_dunder(string: str):
    return string[ 1: ][ :-1 ] if is_dunder(string) else string


def split(string: str, separator: str = SEPARATOR):
    if separator in string:
        return [ i.strip() for i in string.split(separator) ]
    return


def only_digits(v) -> str:
    return "".join(filter(str.isdigit, str(v)))


def parse_int(v) -> int:
    digits = only_digits(v=v)
    if digits != '':
        return int(digits)
    raise ValueError


def parse_date(v=None) -> datetime.date:
    D = namedtuple("D", "year month day", defaults=[ *datetime.date.today().timetuple()[ :2 ], 1 ])
    if isinstance(v, str):
        try:
            value = datetime.date.fromisoformat(v)
        except:
            rs = [ parse_int(x) for x in v.split("-") ]
            print(rs)
            d = D(*rs)
            print(f'the value of D tuple is {d}')
            value = datetime.date(*D(*d))
    elif isinstance(v, datetime.datetime):
        value = v.date()
    elif isinstance(v, (tuple, list)):
        value = datetime.date(*D(*v))
    else:
        raise ValueError("could not parse {} to date".format(v))
    return value


def cpf_format(value):
    if value:
        if value == ("None" or "none" or "null"):
            return None
        _v = str(value)
        r = "".join(filter(str.isdigit, _v))
        if len(r) != 11:
            raise ValueError("são necessários exatamente 11 dígitos para o CPF")
        cpf = r
    else:
        cpf = None
    return int(cpf)


def json_parse(value):
    if value == None:
        return 'null'
    elif isinstance(value, str):
        return value
    elif isinstance(value, int):
        return value
    elif isinstance(value, float):
        return value
    elif isinstance(value, decimal.Decimal):
        return value.__str__()
    elif isinstance(value, list):
        return [ json_parse(i) for i in value ]
    elif isinstance(value, dict):
        return {k: json_parse(v) for k, v in value.items()}
    elif isinstance(value, bool):
        return 'true' if value == True else 'false'
    # elif isinstance(value, (EnumInt, EnumStr)):
    #     return type(value)(value)
    else:
        return str(value)


def normalize_tuple_size(value, size) -> tuple:
    vsize = len(value)
    if vsize == size:
        return tuple([ *value ])
    elif vsize > size:
        return tuple(value[ :size ])
    elif vsize < size:
        rem = size - vsize
        return tuple([ *value, *[ 1 for _ in range(rem) ] ])


def parse_to_date(value):
    def parse_str(value):
        return datetime.date.fromisoformat(value)

    def parse_tuple_or_list(value):
        return datetime.date(*normalize_tuple_size(value, 3))

    if type(value) == str:
        return parse_str(value)
    elif type(value) == tuple:
        return parse_tuple_or_list(value)
    elif type(value) == list:
        return parse_tuple_or_list(value)
    else:
        raise ValueError(f"{value} of type {type(value)} should be str, tuple or list")


def parse_to_datetime(value):
    def parse_str(value):
        return datetime.datetime.fromisoformat(value)

    def parse_tuple_or_list(value):
        return datetime.datetime(*normalize_tuple_size(value, 6))

    if type(value) == str:
        return parse_str(value)
    elif type(value) == tuple:
        return parse_tuple_or_list(value)
    elif type(value) == list:
        return parse_tuple_or_list(value)
    else:
        raise ValueError(f"{value} of type {type(value)} should be str, tuple or list")
