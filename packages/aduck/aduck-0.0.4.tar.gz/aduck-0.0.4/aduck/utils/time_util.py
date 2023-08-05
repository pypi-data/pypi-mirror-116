import time as time_, os
from datetime import timezone, timedelta, date, datetime, time

# ref: https://docs.python.org/3/library/datetime.html
datetime_format_json = '%Y-%m-%d %H:%M:%S%z'
date_format = '%Y-%m-%d'
time_format = '%H:%M:%S'

datetime_format_simple = '%Y-%m-%d %H:%M:%S'
time_format_short = '%H:%M'


def get_sys_timezone():
    tz = os.environ.get("TZ")
    if tz is not None:
        return timezone(timedelta(hours=int(tz)))
    return timezone(timedelta(hours=-time_.timezone // 3600))


SYSTEM_TIMEZONE = get_sys_timezone()


def parse_date(date_str, fmt=date_format) -> date:
    return datetime.strptime(date_str, fmt).date()


def parse_datetime(date_str, fmt=datetime_format_simple) -> datetime:
    return datetime.strptime(date_str, fmt)


def parse_time(date_str, fmt=time_format) -> time:
    return datetime.strptime(date_str, fmt).time()


def parse_datetimetz(date_str, fmt=datetime_format_json) -> datetime:
    return datetime.strptime(date_str, fmt)


def to_date(day: date, fmt=date_format) -> str:
    return day.strftime(fmt)


def to_datetime(day: datetime, fmt=datetime_format_simple) -> str:
    return day.strftime(fmt)


def to_datetimetz(day: datetime, fmt=datetime_format_json) -> str:
    return day.strftime(fmt)


def to_time(day: datetime or time, fmt=time_format) -> str:
    return day.strftime(fmt)
