#!/usr/bin/env python

"""
:Name: kron
:Description: Uniform interface for dates and times in Python
:Version: 1.2.0
:Author: qtfkwk <qtfkwk+kron@gmail.com>
:File: kron.py
"""

# Standard modules

import argparse
import datetime
import json
import re
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
        """resolve timezone given a name

        if name is...
        * None: returns local timezone name
        * string that is an exact match in proper or lower case:
          itself
        * empty string ('') or wildcard regular expression ('.*'):
          returns all timezone names
        * any other string: used as a regular expression; multiple or
          zero matches returns a list"""
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
            if re.search(name, t) or re.search(name_, t_):
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
        basetz='%Y-%m-%d %H:%M:%S %Z',
        HH='%H',
        HH_MM='%H:%M',
        HH_MM_SS='%H:%M:%S',
        HHMM='%H%M',
        HHMMSS='%H%M%S',
        MM='%M',
        SS='%S',
        abbr_date='%a, %b %d, %Y',
        abbr_month='%b',
        abbr_weekday='%a',
        ampm='%p',
        ccyy='%Y',
        ccyymm='%Y%m',
        ccyymmdd='%Y%m%d',
        date='%A, %B %d, %Y',
        dd='%d',
        hh='%I',
        hh_MM='%I:%M',
        hh_MM_ampm='%I:%M %p',
        hh_MM_SS='%I:%M:%S',
        hh_MM_SS_ampm='%I:%M:%S %p',
        hours='%H',
        hours12='%I',
        hours24='%H',
        iso8601='%Y-%m-%dT%H:%M:%SZ',
        julian='%j',
        microseconds='%f',
        minutes='%M',
        mm='%m',
        mm_dd_yy='%m/%d/%y',
        mmdd='%m%d',
        mon='%b',
        month='%B',
        national='%a %b %d %X %Z %Y',
        national_date='%x',
        national_time='%X',
        rfc2822='%a, %d %b %Y %H:%M:%S %z',
        seconds='%S',
        tz='%Z',
        tz_offset='%z',
        week_number_mon='%W',
        week_number_sun='%U',
        weekday='%A',
        year='%Y',
        yy='%y',
        yymm='%y%m',
        yymmdd='%y%m%d',
        yyyy='%Y',
        yyyy_mm_dd='%Y/%m/%d',
        yyyymm='%Y%m',
        yyyymmdd='%Y%m%d',
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
        if fmt == 'iso8601':
            tz = 'UTC'
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
        elif isinstance(value, (str, unicode)) and \
        re.search(r'^\d+\.?\d*$', value):
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

    def str(self, tz=None, fmt=None):
        """output the timestamp as a string in the given timezone and
        format; format may be a named format in the _formats
        dictionary, or any valid strftime format"""
        d = datetime.datetime.fromtimestamp(self.value)
        d = pytz.utc.localize(d)
        if fmt == 'iso8601':
            tz = 'UTC'
        tz = timezone(tz).pytz
        d = tz.normalize(d.astimezone(tz))
        if fmt == None:
            fmt = 'basetz'
        return d.strftime(self._formats[fmt])

    def utc(self, fmt='basetz'):
        """utc timezone helper"""
        return self.str('UTC', fmt)

    def rfc2822(self, tz=None):
        """rfc2822 format helper"""
        return self.str(tz, 'rfc2822')

    def iso8601(self):
        """iso8601 timezone/format helper"""
        return self.str(fmt='iso8601')

    def dict(self, tz=[None], fmt=['basetz']):
        """convert the timestamp to multiple timezones and/or formats
        and return results as a dictionary"""
        if not isinstance(tz, list):
            tz = [tz]
        if not isinstance(fmt, list):
            fmt = [fmt]
        r = {}
        for t in tz:
            if t == None:
                t = 'localtz'
            r[t] = {}
            for f in fmt:
                if f == None:
                    f = 'basetz'
                r[t][f] = self.str(t if t != 'localtz' else None, f)
        return r

    def json(self, tz=[None], fmt=['basetz']):
        """convert the dict to a pretty-printed json string"""
        return _json(self.dict(tz, fmt))

# Functions

def _json(obj):
    """drop-in replacement for json.dumps()"""
    return json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))

def cli(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('-t', metavar='TIMEZONE', action='append', default=[], \
        help=('output timezone'))
    p.add_argument('-f', metavar='FORMAT', action='append', default=[], \
        help=('output format'))
    p.add_argument('-T', metavar='TIMEZONE', action='store', \
        help=('input timezone'))
    p.add_argument('-F', metavar='FORMAT', action='store', \
        help=('input format'))
    p.add_argument('args', metavar='ARG', action='store', nargs='*', \
        help=('one or more timestamp input values; int/float epoch seconds,' + \
        ' timestamp string in base or any format specified by -F;' + \
        ' default: now'))
    a = p.parse_args(argv)
    for i in (a.args, a.t, a.f):
        if i == None:
            i = []
        if i == []:
            i.append(None)
    if len(a.args) + len(a.t) + len(a.f) == 3:
        return timestamp(a.args[0], a.T, a.F).str(a.t[0], a.f[0])
    r = {}
    for i in a.args:
        r[i if i != None else 'now'] = timestamp(i, a.T, a.F).dict(a.t, a.f)
    return _json(r)

def main():
    import sys
    print cli(sys.argv[1:])

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

# Main

if __name__ == '__main__':
    main()
