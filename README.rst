Description
===========

Uniform interface for dates and times in Python

Features
========

* Classes for durations, timestamps and timezones
* Minimal non-standard dependencies
  (`pytz <https://pypi.python.org/pypi/pytz>`_,
  `tzlocal <https://pypi.python.org/pypi/tzlocal>`_)
* Microsecond accuracy
* Timestamp internal storage is float epoch seconds
* Duration internal storage is float seconds
* Timezone name search by regular expression
* Default timezone is local timezone
* Comparison and arithmetic methods for timestamps and durations
* Test-driven development methodology
* Named formats

Example
=======

    >>> from kron import duration, timestamp, timezone
    >>> now = timestamp()
    >>> now.value
    1457246861.121305
    >>> now.str()
    '2016-03-05 20:47:41 EST'
    >>> now.str('UTC')
    '2016-03-06 01:47:41 UTC'
    >>> now.str(fmt='%A, %B %d, %Y')
    'Saturday, March 05, 2016'
    >>> t = timestamp(1257209442)
    >>> t.value
    1257209442.0
    >>> t.str()
    '2009-11-02 14:50:42 EST'
    >>> t.str('UTC')
    '2009-11-02 19:50:42 UTC'
    >>> t.str(fmt='%A, %B %d, %Y')
    'Monday, November 02, 2009'
    >>> t.str(fmt='iso8601')
    '2009-11-02T19:50:42Z'
    >>> t.str(fmt='date')
    'Monday, November 02, 2009'
    >>> t.str(fmt='national')
    'Mon Nov 02 14:50:42 EST 2009'
    >>> t.str(fmt='rfc2822')
    'Mon, 02 Nov 2009 14:50:42 -0500'
    >>> for fmt in sorted(t._formats):
    ...     print '%s: "%s" => "%s"' % (fmt, t._formats[fmt], t.str(fmt=fmt))
    ...
    HH: "%H" => "14"
    HHMM: "%H%M" => "1450"
    HHMMSS: "%H%M%S" => "145042"
    HH_MM: "%H:%M" => "14:50"
    HH_MM_SS: "%H:%M:%S" => "14:50:42"
    MM: "%M" => "50"
    SS: "%S" => "42"
    abbr_date: "%a, %b %d, %Y" => "Mon, Nov 02, 2009"
    abbr_month: "%b" => "Nov"
    abbr_weekday: "%a" => "Mon"
    ampm: "%p" => "PM"
    base: "%Y-%m-%d %H:%M:%S" => "2009-11-02 14:50:42"
    ccyy: "%Y" => "2009"
    ccyymm: "%Y%m" => "200911"
    ccyymmdd: "%Y%m%d" => "20091102"
    date: "%A, %B %d, %Y" => "Monday, November 02, 2009"
    dd: "%d" => "02"
    hh: "%I" => "02"
    hh_MM: "%I:%M" => "02:50"
    hh_MM_SS: "%I:%M:%S" => "02:50:42"
    hh_MM_SS_ampm: "%I:%M:%S %p" => "02:50:42 PM"
    hh_MM_ampm: "%I:%M %p" => "02:50 PM"
    hours: "%H" => "14"
    hours12: "%I" => "02"
    hours24: "%H" => "14"
    iso8601: "%Y-%m-%dT%H:%M:%SZ" => "2009-11-02T19:50:42Z"
    julian: "%j" => "306"
    local: "%Y-%m-%d %H:%M:%S %Z" => "2009-11-02 14:50:42 EST"
    microseconds: "%f" => "000000"
    minutes: "%M" => "50"
    mm: "%m" => "11"
    mm_dd_yy: "%m/%d/%y" => "11/02/09"
    mmdd: "%m%d" => "1102"
    mon: "%b" => "Nov"
    month: "%B" => "November"
    national: "%a %b %d %X %Z %Y" => "Mon Nov 02 14:50:42 EST 2009"
    national_date: "%x" => "11/02/09"
    national_time: "%X" => "14:50:42"
    rfc2822: "%a, %d %b %Y %H:%M:%S %z" => "Mon, 02 Nov 2009 14:50:42 -0500"
    seconds: "%S" => "42"
    tz: "%Z" => "EST"
    tz_offset: "%z" => "-0500"
    week_number_mon: "%W" => "44"
    week_number_sun: "%U" => "44"
    weekday: "%A" => "Monday"
    year: "%Y" => "2009"
    yy: "%y" => "09"
    yymm: "%y%m" => "0911"
    yymmdd: "%y%m%d" => "091102"
    yyyy: "%Y" => "2009"
    yyyy_mm_dd: "%Y/%m/%d" => "2009/11/02"
    yyyymm: "%Y%m" => "200911"
    yyyymmdd: "%Y%m%d" => "20091102"
    >>> t = timestamp('1999-10-12 01:18:43', 'UTC')
    >>> t.value
    939709123.0
    >>> t.str()
    '1999-10-11 22:18:43 EDT'
    >>> t.str('Los_Angeles')
    '1999-10-11 19:18:43 PDT'
    >>> t.str(fmt='%A, %B %d, %Y')
    'Monday, October 11, 1999'
    >>> d = now - t
    >>> d.dict()
    {'days': 5990, 'hours': 0, 'minutes': 28, 'seconds': 58, 'microseconds': 121305}
    >>> local = timezone()
    >>> local.name
    'America/New_York'
    >>> madrid = timezone('madrid')
    >>> madrid.name
    'Europe/Madrid'

Versions
========

* 1.0.0 (2016-03-05): Initial release
* 1.0.1 (2016-03-05): Finished rename
* 1.1.0 (2016-03-06): More formats, improved documentation, fix
  `issue #1 <https://github.com/qtfkwk/kron/issues/1>`_
* 1.1.1 (2016-03-06): Added description to setup.py

Discussion
==========

Dates and times are not one of Python's strengths. Even doing basic
work with dates and times requires using multiple standard and non-
standard modules and effort to get it right. This module seeks to
leverage the necessary modules for handling dates and times but
provide a simple and uniform interface for doing so.

References
==========

* PyPI: https://pypi.python.org/pypi/kron
* Github: https://github.com/qtfkwk/kron

Issues
======

Please report any issues via
`Github Issues <https://github.com/qtfkwk/kron/issues>`_.

Ideas
=====

* Helper methods for timezones, formats
* Command line tool
* Parser to find timestamps inside text/data/filesystems
* Add clock, calendar/timeline, events...

Author
======

qtfkwk <qtfkwk+kron@gmail.com>

