Description
===========

Uniform interface for dates and times in Python

Features
========

* Classes for timezones, durations and timestamps
* Minimal dependencies (pytz, tzlocal)
* Microsecond accuracy
* Timestamp internal storage is float epoch seconds
* Duration internal storage is float seconds
* Default timezone is local timezone
* Comparison and arithmetic methods for timestamps and durations
* Test-driven development methodology

Example
=======

    >>> now = timestamp.timestamp()
    >>> now.value
    1457209599.132212
    >>> now.str()
    '2016-03-05 10:26:39 EST'
    >>> now.str('UTC')
    '2016-03-05 15:26:39 UTC'
    >>> now.str(fmt='%A, %B %d, %Y')
    'Saturday, March 05, 2016'
    >>> t = timestamp.timestamp(1257209442)
    >>> t.value
    1257209442.0
    >>> t.str()
    '2009-11-02 14:50:42 EST'
    >>> t.str('UTC')
    '2009-11-02 19:50:42 UTC'
    >>> t.str(fmt='%A, %B %d, %Y')
    'Monday, November 02, 2009'
    >>> d = now - t
    >>> d.dict()
    {'days': 2315, 'hours': 2, 'minutes': 28, 'seconds': 2,
    'microseconds': 809731}
    >>> local = timestamp.timezone()
    >>> local.name
    'America/New_York'
    >>> madrid = timestamp.timezone('madrid')
    >>> madrid.name
    'Europe/Madrid'

Version
=======

* 1.0.0: Initial release

Author
======

qtfkwk <qtfkwk+timestamp@gmail.com>

