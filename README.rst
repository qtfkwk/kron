Features
========

* Classes for durations, timestamps and timezones
* Minimal non-standard dependencies
  (`ntplib <https://pypi.python.org/pypi/ntplib>`_,
  `pytz <https://pypi.python.org/pypi/pytz>`_,
  `tzlocal <https://pypi.python.org/pypi/tzlocal>`_)
* Microsecond accuracy
* Timestamp internal storage is float epoch seconds in UTC
* Duration internal storage is float seconds
* Timezone name search by regular expression
* Default timezone is local timezone
* Comparison and arithmetic methods for timestamps and durations
* Test-driven development methodology
* Named formats
* Helper methods for timezones and formats
* Command line tool

Installation
============

::

    $ pip install kron

Or::

    $ git clone https://github.com/qtfkwk/kron.git
    $ cd kron
    $ python setup.py install

Update
======

::

    $ pip install -U kron

Or::

    $ cd kron
    $ git pull
    $ python setup.py install

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

Command line tool
-----------------

::

    $ kron -h
    usage: kron.py [-h] [-T TIMEZONE] [-F FORMAT] [-t TIMEZONE] [-f FORMAT]
                   [ARG [ARG ...]]
    
    positional arguments:
      ARG          one or more timestamp input values; int/float epoch seconds,
                   timestamp string in base or any format specified by -F;
                   default: now
    
    optional arguments:
      -h, --help   show this help message and exit
      -T TIMEZONE  input timezone; default: local timezone
      -F FORMAT    input format; default: "base" ("%Y-%m-%d %H:%M:%S")
      -t TIMEZONE  output timezone; default: local timezone
      -f FORMAT    output format; default: "basetz" ("%Y-%m-%d %H:%M:%S %Z")
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

Versions
========

* 1.0.0 (2016-03-05): Initial release
* 1.0.1 (2016-03-05): Finished rename
* 1.1.0 (2016-03-06): More formats, improved documentation, fix
  `issue #1 <https://github.com/qtfkwk/kron/issues/1>`_
* 1.1.1 (2016-03-06): Added description to setup.py
* 1.2.0 (2016-03-08): Helper methods for timezone and formats;
  command line tool
* 1.3.0 (2016-03-11): Converted timestamp internal storage to UTC
  (`issue #2 <https://github.com/qtfkwk/kron/issues/2>`_);
  added Network Time Protocol (RFC 1305) functionality via ntplib
  module; added time, time_ntp, time_utc functions; improved
  documentation
* 1.3.1 (2016-03-11): Fixed classifers; added version test

Discussion
==========

Dates and times are not one of Python's strengths. Even doing basic
work requires using multiple standard and non-standard modules and
effort to get it right. This module seeks to leverage the necessary
modules for handling dates and times but provide a simple and uniform
interface for doing so.

Background
==========

Kron was started as a portfolio project to demonstrate proficiency in
Python as well as practice the test-driven development (TDD) process
in concert with git and Github. The topic was selected to address some
personal points of pain experienced while working with dates and times
in Python.

The importance of correct representation of dates and times in the
area of digital forensics cases cannot be overstated. While a myriad
of poorly designed and implemented code contribute, the *core problem*
is the absence of a simple abstraction to represent a specific point
in time.

Kron drastically simplifies working with dates and times by making the
central "timestamp" class represent a specific point in time, and
enabling it to be created, modified, and viewed in a few natural ways.

See also
========

* Kron at `PyPI <https://pypi.python.org/pypi/kron>`_,
  `Github <https://github.com/qtfkwk/kron>`_
* Network Time Protocol (RFC 1305) at
  `Wikipedia <https://en.wikipedia.org/wiki/Network_Time_Protocol>`_,
  `IETF <https://tools.ietf.org/html/rfc1305>`_

Issues
======

Please view/report any issues
`here <https://github.com/qtfkwk/kron/issues>`_.

Ideas
=====

* Command line tool
    * Timezone searching
    * List formats
    * Duration calculations
* Parser to find timestamps inside text/data/filesystems
* Add clock, calendar/timeline, events...
* Alternate output formats including visual/graphical...

Author
======

qtfkwk <qtfkwk+kron@gmail.com>

Legal
=====

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

