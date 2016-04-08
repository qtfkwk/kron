Kron Documentation
++++++++++++++++++

Description
===========

Uniform interface for dates and times

.. include:: ../../README.rst

Quick start
===========

Install
-------

::

    $ pip install kron

Update
------

::

    $ pip install -U kron

Examples
========

Python code/interpreter
-----------------------

::

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

Command line tool
-----------------

::

    $ kron -h
    usage: kron.py [-h] [-V] [-T TIMEZONE] [-F FORMAT] [-t TIMEZONE] [-f FORMAT]
                   [-s TIMEZONE]
                   [ARG [ARG ...]]
    
    positional arguments:
      ARG            one or more timestamps; int/float epoch seconds, string in
                     the base format or the format specified by -F; default: now
    
    optional arguments:
      -h, --help     show this help message and exit
      -V, --version  print version and exit
      -T TIMEZONE    input timezone; default: local timezone
      -F FORMAT      input format; default: "base" ("%Y-%m-%d %H:%M:%S")
      -t TIMEZONE    output timezone; default: local timezone
      -f FORMAT      output format; default: "basetz" ("%Y-%m-%d %H:%M:%S %Z");
                     try "all" for a demonstration
      -s TIMEZONE    search timezones
    $ kron
    2016-03-11 00:41:46 EST
    $ kron -t utc
    2016-03-11 05:42:13 UTC
    $ kron -f iso8601
    2016-03-11T05:43:10Z
    $ kron '2005-04-04 09:12:00'
    2005-04-04 09:12:00 EDT
    $ kron '2005-04-04 09:12:00' -f weekday
    Monday
    $ kron '2006-11-13 21:22:00' -T UTC
    2006-11-13 16:22:00 EST
    $ kron '2006-11-13 21:22:00' -T UTC -t Madrid -t los_angeles \
    > -f iso8601 -f rfc2822
    {
        "2006-11-13 21:22:00": {
            "Madrid": {
                "iso8601": "2006-11-13T21:22:00Z",
                "rfc2822": "Mon, 13 Nov 2006 22:22:00 +0100"
            },
            "los_angeles": {
                "iso8601": "2006-11-13T21:22:00Z",
                "rfc2822": "Mon, 13 Nov 2006 13:22:00 -0800"
            }
        }
    }
    $ kron -s mad
    Atlantic/Madeira
    Europe/Madrid

Discussion
==========

Dates and times are not one of Python's strengths. Doing basic work
requires using multiple standard and non-standard modules and effort
to get it right. This module leverages the necessary modules for
handling dates and times but provides a simple and uniform interface
for doing so.

Background
==========

Kron begun as a portfolio project to demonstrate proficiency in
Python as well as practice the test-driven development (TDD) process
in concert with git and Github. The topic was selected to address some
personal points of pain experienced while working with dates and times
in Python.

The importance of correct representation of dates and times in the
area of digital forensics and other fields cannot be overstated. While
a myriad of poorly designed and implemented code contribute, the
**core problem** is the absence of a simple abstraction to represent a
specific point in time.

Kron is built around the "timestamp" class, which represents a
specific point in time. Timestamp objects can be created, modified,
and viewed in a few *natural* ways.

The "duration" class represents a duration of time and the difference
of two timestamp objects.

The "timezone" class is provided to simplify specifying a timezone by
allowing a partial string or regular expression to search for the
proper name.

Versions
========

+---------+------------+----------------------------------------------+
| Version | Date       | Description                                  |
+=========+============+==============================================+
| 1.0.0   | 2016-03-05 | Initial release                              |
+---------+------------+----------------------------------------------+
| 1.0.1   | 2016-03-05 | Finished rename                              |
+---------+------------+----------------------------------------------+
| 1.1.0   | 2016-03-06 | More formats, improved documentation         |
+---------+------------+----------------------------------------------+
| 1.1.1   | 2016-03-06 | Added description to setup.py                |
+---------+------------+----------------------------------------------+
| 1.2.0   | 2016-03-08 | Helper methods for timezone and formats;     |
|         |            | command line tool                            |
+---------+------------+----------------------------------------------+
| 1.3.0   | 2016-03-11 | Converted timestamp internal storage to UTC; |
|         |            | added Network Time Protocol (RFC 1305)       |
|         |            | functionality via ntplib module; added time, |
|         |            | time_ntp, time_utc functions; improved       |
|         |            | documentation                                |
+---------+------------+----------------------------------------------+
| 1.3.1   | 2016-03-11 | Added version test                           |
+---------+------------+----------------------------------------------+
| 1.3.2   | 2016-03-11 | Fixed classifers                             |
+---------+------------+----------------------------------------------+
| 1.4.0   | 2016-03-13 | Improved documentation                       |
+---------+------------+----------------------------------------------+
| 1.4.1   | 2016-03-13 | Fix command line tool                        |
+---------+------------+----------------------------------------------+
| 1.4.2   | 2016-03-14 | Add release script; fix versions table       |
+---------+------------+----------------------------------------------+
| 1.5.0   | 2016-03-16 | Support Python 3.5.1 and 2.7.11; default NTP |
|         |            | server: us.pool.ntp.org; fix release script  |
+---------+------------+----------------------------------------------+
| 1.5.1   | 2016-03-16 | Convert release script to python; improve    |
|         |            | documentation; other minor fixes             |
+---------+------------+----------------------------------------------+
| 1.5.2   | 2016-03-16 | Restore release script to bash; fix readme   |
+---------+------------+----------------------------------------------+
| 1.5.3   | 2016-03-16 | Move readme content to package documentation |
+---------+------------+----------------------------------------------+
| 1.6.0   | 2016-03-23 | Add timezone search to CLI (-s); "all"       |
|         |            | psuedo output format; improve documentation  |
+---------+------------+----------------------------------------------+
| 1.6.1   | 2016-03-23 | Fix release script                           |
+---------+------------+----------------------------------------------+
| 1.6.2   | 2016-04-08 | Avoid importing kron in setup.py; change     |
|         |            | version to __version__; add dependency       |
|         |            | future to setup.py; fix spelling in          |
|         |            | documentation                                |
+---------+------------+----------------------------------------------+
| 1.6.3   | 2016-04-08 | Upload new version due to PyPI upload error  |
+---------+------------+----------------------------------------------+

Issues
======

Please view/report any issues
`here <https://github.com/qtfkwk/kron/issues?q=is%3Aissue>`_.

Developers
==========

Download source
---------------

::

    $ git clone https://github.com/qtfkwk/kron.git

Install from source
-------------------

::

    $ cd kron
    $ python setup.py install

Update
------

::

    $ cd kron
    $ git pull
    $ python setup.py install

Build distributions
-------------------

::

    $ cd kron
    $ python setup.py sdist
    $ python setup.py bdist_wheel

Build documentation
-------------------

::

    $ cd kron
    $ make -C doc html

Ideas
=====

* Command line tool

    * Duration calculations

* Parser to find timestamps inside text/data/filesystems
* Add clock, calendar/timeline, events...
* Alternate output formats including visual/graphical...

See also
========

* Kron: `PyPI <https://pypi.python.org/pypi/kron>`_,
  `Github <https://github.com/qtfkwk/kron>`_,
  `Documentation <https://pythonhosted.org/kron>`_,
  `API Reference <https://pythonhosted.org/kron/#id5>`_
* Python built-in modules

    * `calendar <http://docs.python.org/library/calendar.html>`_
    * `datetime <http://docs.python.org/library/datetime.html>`_
    * `time <http://docs.python.org/library/time.html>`_

* Python non-standard modules at PyPI

    * `ntplib <https://pypi.python.org/pypi/ntplib>`_
    * `pytz <https://pypi.python.org/pypi/pytz>`_
    * `tzlocal <https://pypi.python.org/pypi/tzlocal>`_

* Network Time Protocol (RFC 1305) at
  `Wikipedia <https://en.wikipedia.org/wiki/RFC_1305>`_,
  `IETF <https://tools.ietf.org/html/rfc1305>`_
* Internet Message Format (RFC 2822) at
  `Wikipedia <https://en.wikipedia.org/wiki/RFC_2822>`_,
  `IETF <https://tools.ietf.org/html/rfc2822>`_
* Date and time format (ISO 8601) at
  `Wikipedia <https://en.wikipedia.org/wiki/ISO_8601>`_,
  `ISO <http://www.iso.org/iso/iso8601>`_,
  `xkcd <https://xkcd.com/1179/>`_
* ``strftime`` at
  `linux.die.net <http://linux.die.net/man/3/strftime>`_,
  `Python time.strftime
  <https://docs.python.org/2/library/time.html#time.strftime>`_
* tz database (zoneinfo, Olson database, tzfile) at
  `IANA <http://www.iana.org/time-zones>`_,
  `Wikipedia <https://en.wikipedia.org/wiki/Tz_database>`_,
  `List of time zones
  <https://en.wikipedia.org/wiki/List_of_tz_database_time_zones>`_,
  `tzfile manpage <http://linux.die.net/man/5/tzfile>`_

Author
======

"qtfkwk"
qtfkwk+kron@gmail.com,
`@qtfimik <https://twitter.com/qtfimik>`_

License
=======

::

    Copyright (c) 2016, qtfkwk
    All rights reserved.
    
    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:
    
    * Redistributions of source code must retain the above copyright notice, this
      list of conditions and the following disclaimer.
    
    * Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.
    
    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
    AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
    FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
    DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
    CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
    OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


API Reference
=============

Named formats
-------------

Formats are used for two events during the lifetime of a ``timestamp``
object. The first is when the object is created. This format is passed
to ``strptime`` to parse the values from the string. The second is any
time the object is converted to a string via the ``str`` method or
some method that calls ``str``. This format is passed to ``strftime``
to format the timestamp.

Kron provides a means to specify ``strftime``/``strptime`` formats as
"named formats", which are listed in the table below, and available in
the ``timestamp.formats`` dictionary. If the value passed for a
``fmt`` argument matches a named format name, then the appropriate
format string is substituted when it is used. Otherwise, the specified
format is used as is.

For more information about ``strftime`` formats, please consult ``man
strftime`` or visit ``strftime`` at
`linux.die.net <http://linux.die.net/man/3/strftime>`_ and/or
`Python time.strftime
<https://docs.python.org/2/library/time.html#time.strftime>`_.

+-----------------+----------------------+---------------------------+
| Name            | Format string        | Example                   |
+=================+======================+===========================+
| HH              | "%H"                 | "14"                      |
+-----------------+----------------------+---------------------------+
| HHMM            | "%H%M"               | "1450"                    |
+-----------------+----------------------+---------------------------+
| HHMMSS          | "%H%M%S"             | "145042"                  |
+-----------------+----------------------+---------------------------+
| HH_MM           | "%H:%M"              | "14:50"                   |
+-----------------+----------------------+---------------------------+
| HH_MM_SS        | "%H:%M:%S"           | "14:50:42"                |
+-----------------+----------------------+---------------------------+
| MM              | "%M"                 | "50"                      |
+-----------------+----------------------+---------------------------+
| SS              | "%S"                 | "42"                      |
+-----------------+----------------------+---------------------------+
| abbr_date       | "%a, %b %d, %Y"      | "Mon, Nov 02, 2009"       |
+-----------------+----------------------+---------------------------+
| abbr_month      | "%b"                 | "Nov"                     |
+-----------------+----------------------+---------------------------+
| abbr_weekday    | "%a"                 | "Mon"                     |
+-----------------+----------------------+---------------------------+
| ampm            | "%p"                 | "PM"                      |
+-----------------+----------------------+---------------------------+
| base            | "%Y-%m-%d %H:%M:%S"  | "2009-11-02 14:50:42"     |
+-----------------+----------------------+---------------------------+
| basetz          | "%Y-%m-%d            | "2009-11-02 14:50:42 EST" |
|                 | %H:%M:%S %Z"         |                           |
+-----------------+----------------------+---------------------------+
| ccyy            | "%Y"                 | "2009"                    |
+-----------------+----------------------+---------------------------+
| ccyymm          | "%Y%m"               | "200911"                  |
+-----------------+----------------------+---------------------------+
| ccyymmdd        | "%Y%m%d"             | "20091102"                |
+-----------------+----------------------+---------------------------+
| date            | "%A, %B %d, %Y"      | "Monday, November 02,     |
|                 |                      | 2009"                     |
+-----------------+----------------------+---------------------------+
| dd              | "%d"                 | "02"                      |
+-----------------+----------------------+---------------------------+
| hh              | "%I"                 | "02"                      |
+-----------------+----------------------+---------------------------+
| hh_MM           | "%I:%M"              | "02:50"                   |
+-----------------+----------------------+---------------------------+
| hh_MM_SS        | "%I:%M:%S"           | "02:50:42"                |
+-----------------+----------------------+---------------------------+
| hh_MM_SS_ampm   | "%I:%M:%S %p"        | "02:50:42 PM"             |
+-----------------+----------------------+---------------------------+
| hh_MM_ampm      | "%I:%M %p"           | "02:50 PM"                |
+-----------------+----------------------+---------------------------+
| hours           | "%H"                 | "14"                      |
+-----------------+----------------------+---------------------------+
| hours12         | "%I"                 | "02"                      |
+-----------------+----------------------+---------------------------+
| hours24         | "%H"                 | "14"                      |
+-----------------+----------------------+---------------------------+
| iso8601         | "%Y-%m-%dT%H:%M:%SZ" | "2009-11-02T19:50:42Z"    |
+-----------------+----------------------+---------------------------+
| julian          | "%j"                 | "306"                     |
+-----------------+----------------------+---------------------------+
| microseconds    | "%f"                 | "000000"                  |
+-----------------+----------------------+---------------------------+
| minutes         | "%M"                 | "50"                      |
+-----------------+----------------------+---------------------------+
| mm              | "%m"                 | "11"                      |
+-----------------+----------------------+---------------------------+
| mm_dd_yy        | "%m/%d/%y"           | "11/02/09"                |
+-----------------+----------------------+---------------------------+
| mmdd            | "%m%d"               | "1102"                    |
+-----------------+----------------------+---------------------------+
| mon             | "%b"                 | "Nov"                     |
+-----------------+----------------------+---------------------------+
| month           | "%B"                 | "November"                |
+-----------------+----------------------+---------------------------+
| national        | "%a %b %d            | "Mon Nov 02 14:50:42 EST  |
|                 | %X %Z %Y"            | 2009:                     |
+-----------------+----------------------+---------------------------+
| national_date   | "%x"                 | "11/02/09"                |
+-----------------+----------------------+---------------------------+
| national_time   | "%X"                 | "14:50:42"                |
+-----------------+----------------------+---------------------------+
| rfc2822         | "%a, %d %b %Y        | "Mon, 02 Nov 2009         |
|                 | %H:%M:%S %z"         | 14:50:42 -0500"           |
+-----------------+----------------------+---------------------------+
| seconds         | "%S"                 | "42"                      |
+-----------------+----------------------+---------------------------+
| tz              | "%Z"                 | "EST"                     |
+-----------------+----------------------+---------------------------+
| tz_offset       | "%z"                 | "-0500"                   |
+-----------------+----------------------+---------------------------+
| week_number_mon | "%W"                 | "44"                      |
+-----------------+----------------------+---------------------------+
| week_number_sun | "%U"                 | "44"                      |
+-----------------+----------------------+---------------------------+
| weekday         | "%A"                 | "Monday"                  |
+-----------------+----------------------+---------------------------+
| year            | "%Y"                 | "2009"                    |
+-----------------+----------------------+---------------------------+
| yy              | "%y"                 | "09"                      |
+-----------------+----------------------+---------------------------+
| yymm            | "%y%m"               | "0911"                    |
+-----------------+----------------------+---------------------------+
| yymmdd          | "%y%m%d"             | "091102"                  |
+-----------------+----------------------+---------------------------+
| yyyy            | "%Y"                 | "2009"                    |
+-----------------+----------------------+---------------------------+
| yyyy_mm_dd      | "%Y/%m/%d"           | "2009/11/02"              |
+-----------------+----------------------+---------------------------+
| yyyymm          | "%Y%m"               | "200911"                  |
+-----------------+----------------------+---------------------------+
| yyyymmdd        | "%Y%m%d"             | "20091102"                |
+-----------------+----------------------+---------------------------+

Classes
-------

duration
''''''''

.. autoclass:: kron.duration
   :members:

timestamp
'''''''''

.. autoclass:: kron.timestamp
   :members:

timezone
''''''''

.. autoclass:: kron.timezone
   :members:

Functions
---------

time
''''

.. autofunction:: kron.time

time_ntp
''''''''

.. autofunction:: kron.time_ntp

time_utc
''''''''

.. autofunction:: kron.time_utc

