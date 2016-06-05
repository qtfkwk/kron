#!/usr/bin/env python

# Name: kron
# Description: Uniform interface for dates and times
# Version: 1.6.5
# File: kron.py
# Author: qtfkwk <qtfkwk+kron@gmail.com>
# Copyright: (C) 2016 by qtfkwk
# License: BSD 2-Clause License (https://opensource.org/licenses/BSD-2-Clause)

"""Uniform interface for dates and times

* Documentation: https://pythonhosted.org/kron
* API Reference: https://pythonhosted.org/kron/#api-reference
"""

from __future__ import division
from __future__ import print_function
from past.builtins import cmp
from builtins import object

# Standard modules

import argparse
import datetime
import json
import re
import calendar

# External modules

import ntplib
import pytz
import tzlocal

# Variables

__version__ = '1.6.5'

# Classes

class duration(object):
    """Represents a duration of time
    
    ``value`` is float seconds.

    Internal storage is float seconds and accessible via the ``value``
    property.

    Duration objects can be compared via ``<``, ``>``, ``<=``, ``>=``,
    ``==``, and ``!=`` with each other or an int/float value in
    seconds.

    Duration objects support various arithmetic operations via ``+``,
    ``-``, ``*``, ``/``.

    +----------+----------------------+---------------+
    | Operator | Other type           | Returned type |
    +==========+======================+===============+
    | ``+``    | timestamp            | timestamp     |
    +          +----------------------+---------------+
    |          | int, float, duration | duration      |
    +----------+----------------------+---------------+
    | ``-``    | int, float, duration | duration      |
    +----------+----------------------+---------------+
    | ``*``    | int, float           | duration      |
    +----------+----------------------+---------------+
    | ``/``    | int, float           | duration      |
    +----------+----------------------+---------------+

    Arithmetic operations with a type not listed in the above table
    raises one of ``DurationAddError``, ``DurationDivideError``,
    ``DurationMultipyError``, or ``DurationSubtractError``.
    """

    _units = ('days', 'hours', 'minutes', 'seconds')
    _values = dict(days=86400, hours=3600, minutes=60, seconds=1)

    def __init__(self, value=0):
        self.value = float(round(value, 6))

    def dict(self):
        """Returns a dictionary with the duration as the count of
        days, hours, minutes, seconds, and microseconds"""
        v = int(self.value)
        r = dict(days=0, hours=0, minutes=0, seconds=0)
        r['microseconds'] = int((self.value - v) * 10**6 + 0.5)
        for i in self._units:
            r[i] = v // self._values[i]
            v -= r[i] * self._values[i]
        return r

    def __cmp__(self, y):
        """Compare two duration objects"""
        if isinstance(y, duration):
            return cmp(self.value, y.value)
        elif isinstance(y, (int, float)):
            return cmp(self.value, y)
        else:
            raise DurationComparisonError

    def __lt__(self, y):
        """Compare two duration objects via < (Python 3)"""
        if isinstance(y, duration):
            return self.value < y.value
        elif isinstance(y, (int, float)):
            return self.value < y
        else:
            raise DurationComparisonError

    def __le__(self, y):
        """Compare two duration objects via <= (Python 3)"""
        if isinstance(y, duration):
            return self.value <= y.value
        elif isinstance(y, (int, float)):
            return self.value <= y
        else:
            raise DurationComparisonError

    def __gt__(self, y):
        """Compare two duration objects via > (Python 3)"""
        if isinstance(y, duration):
            return self.value > y.value
        elif isinstance(y, (int, float)):
            return self.value > y
        else:
            raise DurationComparisonError

    def __ge__(self, y):
        """Compare two duration objects via >= (Python 3)"""
        if isinstance(y, duration):
            return self.value >= y.value
        elif isinstance(y, (int, float)):
            return self.value >= y
        else:
            raise DurationComparisonError

    def __eq__(self, y):
        """Compare two duration objects via == (Python 3)"""
        if isinstance(y, duration):
            return self.value == y.value
        elif isinstance(y, (int, float)):
            return self.value == y
        else:
            raise DurationComparisonError

    def __add__(self, y):
        """Add two durations or a duration and an int or float"""
        if isinstance(y, duration):
            return duration(self.value + y.value)
        elif isinstance(y, (int, float)):
            return duration(self.value + y)
        elif isinstance(y, timestamp):
            return timestamp(self.value + y.value)
        else:
            raise DurationAddError

    def __sub__(self, y):
        """Subtract two durations or a duration and an int or float"""
        if isinstance(y, duration):
            return duration(self.value - y.value)
        elif isinstance(y, (int, float)):
            return duration(self.value - y)
        else:
            raise DurationSubtractError

    def __mul__(self, y):
        """Multiply a duration by an int or float"""
        if isinstance(y, (int, float)):
            return duration(self.value * y)
        else:
            raise DurationMultiplyError

    def __div__(self, y):
        """Divide a duration by an int or float"""
        if isinstance(y, (int, float)):
            return duration(self.value / y)
        else:
            raise DurationDivideError

    def __truediv__(self, y):
        """Divide a duration by an int or float"""
        if isinstance(y, (int, float)):
            return duration(self.value / y)
        else:
            raise DurationDivideError

    def __floordiv__(self, y):
        """Divide a duration by an int or float"""
        if isinstance(y, (int, float)):
            return duration(self.value // y)
        else:
            raise DurationDivideError

class _bdict(dict):
    """Enhanced dictionary used to store the formats"""

    def __missing__(self, key):
        if key == None:
            key = 'base'
        return self[key] if key in self else key

class timestamp(object):
    """Represents a specific point in time
    
    ``value`` can be:

    * int/float in epoch seconds in UTC or a string that looks like
      one: sets the value directly
    * Anything else is passed to the ``time`` function along with the
      values of the ``tz``, ``fmt``, and ``ntp`` arguments

    Internal storage is float epoch seconds in UTC and accessible via
    the ``value`` property.

    Timestamp objects can be compared via ``<``, ``>``, ``<=``, ``>=``,
    ``==``, and ``!=`` with each other.

    Timestamp objects support various arithmetic operations via ``+``
    and ``-``.

    +----------+----------------------+---------------+
    | Operator | Other type           | Returned type |
    +==========+======================+===============+
    | ``+``    | int, float, duration | timestamp     |
    +----------+----------------------+---------------+
    | ``-``    | int, float, duration | timestamp     |
    +          +----------------------+---------------+
    |          | timestamp            | duration      |
    +----------+----------------------+---------------+

    Arithmetic operations with a type not listed in the above table
    raises one of ``TimestampAddError``, ``TimestampDivideError``,
    ``TimestampMultipyError``, or ``TimestampSubtractError``.
    """

    formats = _bdict(
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
        rfc2822_='%a, %d %b %Y %H:%M:%S',
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

    def __init__(self, value=None, tz=None, fmt=None, ntp=False):
        if isinstance(value, (int, float)):
            self.value = float(value)
        elif isinstance(value, str) and \
        re.search(r'^\d+\.?\d*$', value):
            self.value = float(value)
        else:
            self.value = time(value, tz, fmt, ntp)
        self.value = round(self.value, 6)

    def __cmp__(self, y):
        """Compare two timestamps"""
        if isinstance(y, timestamp):
            return cmp(self.value, y.value)
        else:
            raise TimestampComparisonError

    def __lt__(self, y):
        """Compare two timestamps via < (Python 3)"""
        if isinstance(y, timestamp):
            return self.value < y.value
        else:
            raise TimestampComparisonError

    def __le__(self, y):
        """Compare two timestamps via <= (Python 3)"""
        if isinstance(y, timestamp):
            return self.value <= y.value
        else:
            raise TimestampComparisonError

    def __gt__(self, y):
        """Compare two timestamps via > (Python 3)"""
        if isinstance(y, timestamp):
            return self.value > y.value
        else:
            raise TimestampComparisonError

    def __ge__(self, y):
        """Compare two timestamps via >= (Python 3)"""
        if isinstance(y, timestamp):
            return self.value >= y.value
        else:
            raise TimestampComparisonError

    def __eq__(self, y):
        """Compare two timestamps via == (Python 3)"""
        if isinstance(y, timestamp):
            return self.value == y.value
        else:
            raise TimestampComparisonError

    def __sub__(self, y):
        """Subtract two timestamps to produce a duration object, or a
        duration, int, or float from a timestamp to produce a new
        timestamp object"""
        if isinstance(y, timestamp):
            return duration(abs(self.value - y.value))
        elif isinstance(y, duration):
            return timestamp(self.value - y.value)
        elif isinstance(y, (int, float)):
            return timestamp(self.value - y)
        else:
            raise TimestampSubtractError

    def __add__(self, y):
        """Add a duration, int, or float to a timestamp to produce a
        new timestamp object"""
        if isinstance(y, duration):
            return timestamp(self.value + y.value)
        elif isinstance(y, (int, float)):
            return timestamp(self.value + y)
        else:
            raise TimestampAddError

    def __mul__(self, y):
        """Cannot multiply a timestamp"""
        raise TimestampMultiplyError

    def __div__(self, y):
        """Cannot divide a timestamp"""
        raise TimestampDivideError

    def __truediv__(self, y):
        """Cannot divide a timestamp"""
        raise TimestampDivideError

    def __floordiv__(self, y):
        """Cannot divide a timestamp"""
        raise TimestampDivideError

    def str(self, tz=None, fmt=None):
        """Returns the timestamp as a string in the local or given
        timezone and the 'basetz' or given format"""
        d = datetime.datetime.fromtimestamp(self.value)
        d = timezone().pytz.localize(d)
        if fmt == 'iso8601':
            tz = 'UTC'
        if tz != pytz.utc:
            tz = timezone(tz).pytz
            d = tz.normalize(d.astimezone(tz))
        if fmt == None:
            fmt = 'basetz'
        return d.strftime(self.formats[fmt])

    def utc(self, fmt='basetz'):
        """Returns the timestamp as a string in the UTC timezone and
        the 'basetz' or given format"""
        return self.str('UTC', fmt)

    def rfc2822(self, tz=None):
        """Returns the timestamp as a string in the local or given
        timezone and the 'rfc2822' format"""
        return self.str(tz, 'rfc2822')

    def iso8601(self):
        """Returns the timestamp as a string in the UTC timezone
        (implied) and the 'iso8601' format"""
        return self.str(fmt='iso8601')

    def dict(self, tz=[None], fmt=['basetz']):
        """Returns the timestamp as a dictionary with keys as the
        given timezones and values as dictionaries with keys as the
        given formats (default: 'basetz')"""
        if fmt == 'all' or isinstance(fmt, list) and 'all' in fmt:
            fmt = list(self.formats.keys())
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
        """Returns the dictionary produced by the ``dict`` method as a
        pretty-printed JSON string"""
        return _json(self.dict(tz, fmt))

class timezone(object):
    """Represent a timezone

    ``name`` is stored in the ``original`` property, and resolved to a
    timezone name via ``timezone.search``, which is stored in the
    ``name`` property.

    A pytz object is created for the given name and accessible via the
    ``pytz`` property.
    """

    def __init__(self, name=None):
        self.original = name
        self.name = self.search(name)
        if isinstance(self.name, list):
            if len(self.name) == 0:
                raise TimezoneFailure('No timezone found for "%s"' % name)
            else:
                raise TimezoneMultiple('Found multiple possible timezones' + \
                    ' for "%s": %s' % (name, ', '.join(self.name)))
        self.pytz = pytz.timezone(self.name)

    @classmethod
    def search(cls, name=None):
        """Resolve timezone given a name

        ``name`` can be:

        * omitted or None: returns name of the local timezone
        * string matching a timezone name in ``pytz.all_timezones``:
          returns the timezone name in proper case
        * empty string ('') or wildcard regular expression ('.*'):
          returns a list with all timezone names
        * any other string: used as a regular expression; multiple or
          zero matches returns a list with the matched timezone names
        """
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

# Error classes

class KronError(Exception):
    """Base exception class"""
    pass

class DurationAddError(KronError):
    pass

class DurationComparisonError(KronError):
    pass

class DurationDivideError(KronError):
    pass

class DurationMultiplyError(KronError):
    pass

class DurationSubtractError(KronError):
    pass

class NTPError(KronError):
    pass

class TimeEpochError(KronError):
    pass

class TimeFormatError(KronError):
    pass

class TimeTimezoneError(KronError):
    pass

class TimestampAddError(KronError):
    pass

class TimestampComparisonError(KronError):
    pass

class TimestampMultiplyError(KronError):
    pass

class TimestampDivideError(KronError):
    pass

class TimestampSubtractError(KronError):
    pass

class TimezoneFailure(KronError):
    pass

class TimezoneMultiple(KronError):
    pass

# Functions

def time(value=None, tz=None, fmt=None, ntp=False):
    """Primitive functional interface for the ``timestamp`` class;
    similar to ``time.time()``, except more flexible and consistent;
    optionally attempts to use NTP with a fallback to use system time;
    can also process a string timestamp; returns float epoch seconds
    in UTC

    ``value`` can be:

    * omitted or None: use current date and time now (via system time
      if ``ntp`` is False (default) or NTP if ``ntp`` is True); raises
      ``TimeTimezoneError`` if ``tz`` is specified or
      ``TimeFormatError`` if ``fmt`` is specified
    * string timestamp in the ``base`` format or given by ``fmt`` and
      the local timezone or given by ``tz``
    """
    if value == None:
        # now
        if tz != None:
            raise TimeTimezoneError('defined tz while value is None')
        if fmt != None:
            raise TimeFormatError('defined fmt while value is None')
        if ntp:
            try:
                r = time_ntp()
            except NTPError:
                r = time_utc()
        else:
            r = time_utc()
    else:
        # process as a string timestamp
        d = datetime.datetime.strptime(value, timestamp.formats[fmt])
        if fmt == 'iso8601':
            tz = 'UTC'
        r = time_utc(d, tz)
    return r

def time_ntp(server='us.pool.ntp.org'):
    """Similar to ``time_utc``, except uses NTP

    ``server`` can be any Internet or other network-based NTP server.

    ``time_ntp`` raises ``NTPError`` if it fails to retrieve the time
    from the server.
    """
    c = ntplib.NTPClient()
    try:
        res = c.request(server, version=3)
    except:
        raise NTPError
    # convert from seconds since 1900 to seconds since 1970
    r = res.tx_timestamp - 2208988800
    # convert to utc
    r = time_utc(r)
    return r

def time_utc(epoch=None, tz=None):
    """Similar to ``time.time()``, except always returns float epoch
    seconds in UTC

    ``epoch`` argument can be one of the following; otherwise it
    raises ``TimeEpochError``.

    * omitted or None: use current date and time now (via system time)
    * int/float: epoch seconds in UTC
    * datetime.datetime object
    
    ``tz`` is passed to ``timezone()``.
    """
    if epoch == None:
        d = datetime.datetime.now()
    elif isinstance(epoch, (int, float)):
        d = datetime.datetime.fromtimestamp(epoch)
    elif isinstance(epoch, datetime.datetime):
        d = epoch
    else:
        raise TimeEpochError('epoch must be None, int, float, or datetime')
    d = timezone(tz).pytz.localize(d)
    r = calendar.timegm(d.utctimetuple())
    r += d.microsecond / float(10**6)
    return r

def cli(argv=None):
    """Backend function for command line interface"""
    p = argparse.ArgumentParser()
    p.add_argument('-V', '--version', action='store_true', \
        help='print version and exit')
    p.add_argument('-T', metavar='TIMEZONE', action='store', \
        help='input timezone; default: local timezone')
    p.add_argument('-F', metavar='FORMAT', action='store', \
        help='input format; default: "base" ("%%Y-%%m-%%d %%H:%%M:%%S")')
    p.add_argument('-t', metavar='TIMEZONE', action='append', default=[], \
        help='output timezone; default: local timezone')
    p.add_argument('-f', metavar='FORMAT', action='append', default=[], \
        help='output format; default: "basetz" ("%%Y-%%m-%%d ' + \
             '%%H:%%M:%%S %%Z"); try "all" for a demonstration')
    p.add_argument('-s', metavar='TIMEZONE', action='store', \
        help='search timezones')
    p.add_argument('args', metavar='ARG', action='store', nargs='*', \
        help='one or more timestamps; int/float epoch seconds,' + \
        ' string in the base format or the format specified by -F;' + \
        ' default: now')
    a = p.parse_args(argv)
    if a.version:
        return __version__
    if a.s != None:
        r = timezone.search(a.s)
        if not isinstance(r, list):
            r = [r]
        return '\n'.join(r)
    for i in (a.args, a.t, a.f):
        if i == None:
            i = []
        if i == []:
            i.append(None)
    if len(a.args) + len(a.t) + len(a.f) == 3 and not 'all' in a.f:
        return timestamp(a.args[0], a.T, a.F).str(a.t[0], a.f[0])
    r = {}
    for i in a.args:
        r[i if i != None else 'now'] = timestamp(i, a.T, a.F).dict(a.t, a.f)
    return _json(r)

def main():
    """Frontend function for command line interface"""
    import sys
    print(cli(sys.argv[1:]))

def _json(obj):
    """Drop-in replacement for json.dumps() with pretty-printing"""
    return json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))

# Main

if __name__ == '__main__':
    main()

