"""
:Name: kron
:Description: Uniform interface for dates and times in Python
:Version: 1.1.0
:Author: qtfkwk <qtfkwk+kron@gmail.com>
:File: kron.py
"""

# Standard modules

import datetime
import time

# External modules

import pytz
import tzlocal

# Classes

class timezone(object):
    """represent timezone, provide search mechanism, default to local
    timezone"""

    @classmethod
    def search(cls, name=None):
        """resolve timezone given a name; default: local timezone"""
        if name == None:
            return tzlocal.get_localzone().zone
        if name in pytz.all_timezones:
            return name
        name_ = name.lower()
        matches = []
        for t in pytz.all_timezones:
            t_ = t.lower()
            if name_ == t_:
                return t
            if name in t or name_ in t_:
                matches.append(t)
        if len(matches) == 1:
            return matches[0]
        else:
            return matches

    def __init__(self, name=None):
        """initialize a timezone object"""
        self.original = name
        self.name = self.search(name)
        if isinstance(self.name, list):
            if len(self.name) == 0:
                raise TimezoneFailure
            else:
                raise TimezoneMultiple
        self.pytz = pytz.timezone(self.name)

class duration(object):
    """represent a duration of time"""

    _units = ('days', 'hours', 'minutes', 'seconds')
    _values = dict(days=86400, hours=3600, minutes=60, seconds=1)

    def __init__(self, value=0):
        """initialize a duration object"""
        self.value = round(value, 6)

    def dict(self):
        """return a dictionary with duration represented as common
        units of time"""
        v = int(self.value)
        r = dict(days=0, hours=0, minutes=0, seconds=0)
        r['microseconds'] = int((self.value - v) * 10**6 + 0.5)
        for i in self._units:
            r[i] = int(v / self._values[i])
            v -= r[i] * self._values[i]
        return r

    def __cmp__(self, y):
        """compare two duration objects"""
        if isinstance(y, duration):
            return cmp(self.value, y.value)

    def __add__(self, y):
        """add two durations or a duration and an int or float"""
        if isinstance(y, duration):
            return duration(self.value + y.value)
        elif isinstance(y, (int, float)):
            return duration(self.value + y)

    def __sub__(self, y):
        """subtract two durations or a duration and an int or float"""
        if isinstance(y, duration):
            return duration(self.value - y.value)
        elif isinstance(y, (int, float)):
            return duration(self.value - y)

    def __mul__(self, y):
        """multiply a duration by an int or float"""
        if isinstance(y, (int, float)):
            return duration(self.value * y)
        else:
            raise DurationMultiplyError

    def __div__(self, y):
        """divide a duration by an int or float"""
        if isinstance(y, (int, float)):
            return duration(self.value / y)
        else:
            raise DurationDivideError

class _bdict(dict):
    """enhanced dictionary to store the formats"""

    def __missing__(self, key):
        if key == None:
            key = 'base'
        return self[key] if key in self else key

class timestamp(object):
    """represent a specific point in time, provide multiple ways of
    defining it and translating to other timezones and/or formats

    inputs
    * None: now
    * epoch seconds as int or float in UTC
    * string in base or some other format and/or timezone
    """

    _formats = _bdict(
        base='%Y-%m-%d %H:%M:%S',
        local='%Y-%m-%d %H:%M:%S %Z',
    )

    @classmethod
    def _time(cls, value=None, tz=None, fmt=None):
        """standalone class method similar to time.time() but should
        be more universally reliable; also processes a string
        timestamp; output is float epoch seconds"""
        if value == None:
            d = datetime.datetime.now()
        else:
            d = datetime.datetime.strptime(value, cls._formats[fmt])
        d = timezone(tz).pytz.localize(d)
        r = time.mktime(d.utctimetuple())
        r += d.microsecond / float(10**6)
        return r

    def __init__(self, value=None, tz=None, fmt=None):
        """initialize a timestamp object; internal storage is float
        epoch seconds with microsecond accuracy (values are rounded to
        6 decimal places)"""
        if isinstance(value, (int, float)):
            self.value = float(value)
        else:
            self.value = self._time(value, tz, fmt)
        self.value = round(self.value, 6)

    def __cmp__(self, y):
        """compare two timestamps"""
        if isinstance(y, timestamp):
            return cmp(self.value, y.value)
        else:
            raise TimestampComparisonError

    def __sub__(self, y):
        """subtract two timestamps to produce a duration object, or a
        duration, int, or float from a timestamp to produce a new
        timestamp object"""
        if isinstance(y, timestamp):
            return duration(abs(self.value - y.value))
        elif isinstance(y, duration):
            return timestamp(self.value - y.value)
        elif isinstance(y, (int, float)):
            return timestamp(self.value - y)

    def __add__(self, y):
        """add a duration, int, or float to a timestamp to produce a
        new timestamp object"""
        if isinstance(y, duration):
            return timestamp(self.value + y.value)
        elif isinstance(y, (int, float)):
            return timestamp(self.value + y)

    def __mul__(self, y):
        """cannot multiply a timestamp"""
        raise TimestampMultiplyError

    def __div__(self, y):
        """cannot divide a timestamp"""
        raise TimestampDivideError

    def str(self, tz=None, fmt='local'):
        """output the timestamp as a string in the given timezone and
        format; format may be a named format in the _formats
        dictionary, or any valid strftime format"""
        d = datetime.datetime.fromtimestamp(self.value)
        d = pytz.utc.localize(d)
        tz = timezone(tz).pytz
        d = tz.normalize(d.astimezone(tz))
        return d.strftime(self._formats[fmt])

# Error classes

class KronError(Exception):
    pass

class TimezoneFailure(KronError):
    pass

class TimezoneMultiple(KronError):
    pass

class DurationMultiplyError(KronError):
    pass

class DurationDivideError(KronError):
    pass

class TimestampComparisonError(KronError):
    pass

class TimestampMultiplyError(KronError):
    pass

class TimestampDivideError(KronError):
    pass

