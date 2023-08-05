import json
from datetime import datetime, date, time
from .time_util import datetime_format_json, date_format as default_date_format, \
    time_format as default_time_format
from enum import Enum

# default converts
converters = {
}


class JSONEncoder(json.JSONEncoder):
    def __init__(self, datetime_format=None, date_format=None, time_format=None, converters=None, *args,
                 **kwargs):
        self.datetime_format = datetime_format or datetime_format_json
        self.date_format = date_format or default_date_format
        self.time_format = time_format or default_time_format
        self.converters = converters
        super(JSONEncoder, self).__init__(*args, **kwargs)

    def default(self, obj):

        typ = type(obj)
        if self.converters:
            if typ in self.converters:
                return self.converters[typ](obj)
            for t, fn in self.converters.items():
                if isinstance(obj, t):
                    return fn(obj)

        if isinstance(obj, datetime):
            return obj.strftime(self.datetime_format)
        if isinstance(obj, date):
            return obj.strftime(self.date_format)
        if isinstance(obj, time):
            return obj.strftime(self.time_format)

        if isinstance(obj, Enum):
            return obj.value,

        if typ in converters:
            return converters[typ](obj)
        for t, fn in converters.items():
            if isinstance(obj, t):
                return fn(obj)
        return super(JSONEncoder, self).default(obj)


def dumps(obj, cls=JSONEncoder, **kwargs):
    """
    :param datetime_format: default "%Y-%m-%d %H:%M:%S%z"
    :param date_format: default "%Y-%m-%d"
    :param time_format: default "%H:%M:%S"
    :param converts: {type:fn(x)}
    """
    return json.dumps(obj, cls=cls, **kwargs)


def loads(s, **kwargs):
    if s is None:
        return None
    return json.loads(s, **kwargs)


class JSONSerializer:

    def __init__(self, datetime_format: str = None, date_format: str = None, time_format: str = None):
        self.converters = {}
        self.datetime_format = datetime_format
        self.date_format = date_format
        self.time_format = time_format

    def from_dict(self, fields=None):
        def wrap(cls):
            if fields is None:
                self.converters[cls] = lambda x: x.__dict__
            else:
                fs = set(fields)
                self.converters[cls] = lambda x: {k: v for k, v in x.__dict__.items() if k in fs}
            return cls

        return wrap

    def from_json_decode(self):
        def wrap(cls):
            self.converters[cls] = lambda x: x.json_decode()
            return cls
        return wrap

    def loads(self, s):
        return loads(s)

    def dumps(self, obj, converters: dict = None, datetime_format=None, date_format=None, time_format=None):
        if converters is None:
            converters = self.converters
        else:
            converters.update(self.converters)
        return dumps(obj, converters=converters, datetime_format=datetime_format or self.datetime_format,
                     date_format=date_format or self.date_format, time_format=time_format or self.time_format)
