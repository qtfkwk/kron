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

* 1.0.0: Initial release
* 1.0.1: Finished rename
* 1.1.0: More formats, improved documentation

Discussion
==========

Dates and times are not one of Python's strengths. This module seeks
to leverage the necessary modules for handling dates and times but
provide a simple and uniform interface.

Ideas
=====

* Command line interface
* Helper methods
* Parser to find timestamps inside text/data
* Clock
* Calendar

Author
======

qtfkwk <qtfkwk+kron@gmail.com>

