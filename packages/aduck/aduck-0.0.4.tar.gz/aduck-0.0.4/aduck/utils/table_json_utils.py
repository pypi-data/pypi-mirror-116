from .json_util import loads
from datetime import datetime, date, time
from .time_util import datetime_format_json, date_format, time_format


def to_datetimes(datetimes_json: str, fmt=datetime_format_json) -> [datetime]:
    """

    :param datetimes_json:
    :param fmt:
    :return:
    """
    if datetimes_json is None:
        return None
    r = loads(datetimes_json)
    return [datetime.strptime(v, fmt) if v is not None else None for v in r]


def to_dates(dates_json: str, fmt=date_format) -> [date]:
    if dates_json is None:
        return None
    r = loads(dates_json)
    if r is None:
        return None
    return [datetime.strptime(v, fmt).date() if v is not None else None for v in r]


def to_times(times_json: str, fmt=time_format) -> [time]:
    if times_json is None:
        return None
    r = loads(times_json)
    if r is None:
        return None
    return [datetime.strptime(v, fmt).time() if v is not None else None for v in r]


def to_floats(floats_json: str, ndigits: int = None) -> [float]:
    if floats_json is None:
        return None
    r = loads(floats_json)
    if r is None:
        return None
    if ndigits is not None:
        return [round(float(v), ndigits) if v is not None else None for v in r]
    return [float(v) if v is not None else None for v in r]


def to_ints(ints_json: str) -> [int]:
    if ints_json is None:
        return None
    r = loads(ints_json)
    if r is None:
        return None
    return [int(v) if v is not None else None for v in r]


def to_bools(bools_json: str) -> [bool]:
    if bools_json is None:
        return None
    r = loads(bools_json)
    if r is None:
        return None
    return [bool(v) if v is not None else None for v in r]


def to_strs(strs_json: str) -> [bool]:
    if strs_json is None:
        return None
    r = loads(strs_json)
    return r
