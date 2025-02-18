from datetime import date
from typing import NamedTuple, Union, Optional, Callable

from dates import DateFormat, parse_date

DecodeReturnType = Union[str, int, date]


class DataElement(NamedTuple):
    code: str
    name: str
    supported_versions: tuple[int, ...]
    decode_function: Callable[[str, Optional[DateFormat]], DecodeReturnType]


def decode_string(value: str) -> str:
    return value.strip()


def decode_date(value: str, date_format: DateFormat) -> date:
    return parse_date(value, date_format)


def decode_int(value: str) -> int:
    return int(value.strip())


def decode_eye_color(value: str) -> str:
    raise NotImplementedError("TODO")


DATA_ELEMENTS = ()
