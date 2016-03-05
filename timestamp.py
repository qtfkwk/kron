import tzlocal
import pytz
class timezone(object):
    @classmethod
    def search(cls, name=None):
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
        self.original = name
        self.name = self.search(name)
        if isinstance(self.name, list):
            if len(self.name) == 0:
                raise TimezoneFailure
            else:
                raise TimezoneMultiple
        self.pytz = pytz.timezone(self.name)
class TimezoneFailure(Exception):
    pass
class TimezoneMultiple(Exception):
    pass
class duration(object):
    _units = ('days', 'hours', 'minutes', 'seconds')
    _values = dict(days=86400, hours=3600, minutes=60, seconds=1)
    def __init__(self, value=0):
        self.value = float(value)
    def dict(self):
        v = int(self.value)
        r = dict(days=0, hours=0, minutes=0, seconds=0)
        r['microseconds'] = int((self.value - v) * 10**6 + 0.5)
        for i in self._units:
            r[i] = int(v / self._values[i])
            v -= r[i] * self._values[i]
        return r
    def __cmp__(self, y):
        if isinstance(y, duration):
            return cmp(self.value, y.value)
    def __add__(self, y):
        if isinstance(y, duration):
            return duration(self.value + y.value)
        elif isinstance(y, (int, float)):
            return duration(self.value + y)
    def __sub__(self, y):
        if isinstance(y, duration):
            return duration(self.value - y.value)
        elif isinstance(y, (int, float)):
            return duration(self.value - y)
    def __mul__(self, y):
        if isinstance(y, (int, float)):
            return duration(self.value * y)
        else:
            raise DurationMultiplyError
    def __div__(self, y):
        if isinstance(y, (int, float)):
            return duration(self.value / y)
        else:
            raise DurationDivideError
class DurationMultiplyError(Exception):
    pass
class DurationDivideError(Exception):
    pass
class _bdict(dict):
    def __missing__(self, key):
        if key == None:
            key = 'base'
        return self[key] if key in self else key
import time
import datetime
class timestamp(object):
    _formats = _bdict(
        base='%Y-%m-%d %H:%M:%S',
    )
    def __init__(self, value=None, tz=None, fmt=None):
        if value == None:
            self.value = time.time()
        elif isinstance(value, (int, float)):
            self.value = float(value)
        else:
            d = datetime.datetime.strptime(value, self._formats[fmt])
            d = timezone(tz).pytz.localize(d)
            self.value = time.mktime(d.utctimetuple())
            self.value += d.microsecond / float(10**6)
