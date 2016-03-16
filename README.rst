Features
========

* Classes for durations, timestamps and timezones
* Minimal non-standard dependencies
  (`ntplib <https://pypi.python.org/pypi/ntplib>`_,
  `pytz <https://pypi.python.org/pypi/pytz>`_,
  `tzlocal <https://pypi.python.org/pypi/tzlocal>`_)
* Microsecond accuracy (float epoch seconds are *rounded* to 6 decimal
  places)
* Timestamp internal storage is float epoch seconds in UTC
* Duration internal storage is float seconds
* Timezone name search by regular expression
* Default timezone is local timezone
* Comparison and arithmetic methods for timestamps and durations
* Test-driven development methodology
* Named formats
* Timestamp object "helper" methods for timezones and formats
* Command line tool
* Substitutes for ``time.time()``: time, time_ntp, time_utc

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
      -f FORMAT      output format; default: "basetz" ("%Y-%m-%d %H:%M:%S %Z")
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

The "duration" class represent a duration of time, which is also the
difference of two timestamp objects.

The "timezone" class is provided to simplify specifying a timezone by
allowing a partial string or regular expression to search for the
proper name.

Versions
========

+---------+------------+-----------------------------------------------+
| Version | Date       | Description                                   |
+=========+============+===============================================+
| 1.0.0   | 2016-03-05 | Initial release                               |
+---------+------------+-----------------------------------------------+
| 1.0.1   | 2016-03-05 | Finished rename                               |
+---------+------------+-----------------------------------------------+
| 1.1.0   | 2016-03-06 | More formats, improved documentation, fix     |
|         |            | `issue #1                                     |
|         |            | <https://github.com/qtfkwk/kron/issues/1>`_   |
+---------+------------+-----------------------------------------------+
| 1.1.1   | 2016-03-06 | Added description to setup.py                 |
+---------+------------+-----------------------------------------------+
| 1.2.0   | 2016-03-08 | Helper methods for timezone and formats;      |
|         |            | command line tool                             |
+---------+------------+-----------------------------------------------+
| 1.3.0   | 2016-03-11 | Converted timestamp internal storage to UTC   |
|         |            | (`issue #2                                    |
|         |            | <https://github.com/qtfkwk/kron/issues/2>`_); |
|         |            | added Network Time Protocol (RFC 1305)        |
|         |            | functionality via ntplib module; added        |
|         |            | time, time_ntp, time_utc functions;           |
|         |            | improved documentation                        |
+---------+------------+-----------------------------------------------+
| 1.3.1   | 2016-03-11 | Added version test                            |
+---------+------------+-----------------------------------------------+
| 1.3.2   | 2016-03-11 | Fixed classifers                              |
+---------+------------+-----------------------------------------------+
| 1.4.0   | 2016-03-13 | Improved documentation                        |
+---------+------------+-----------------------------------------------+
| 1.4.1   | 2016-03-13 | Fix command line tool                         |
+---------+------------+-----------------------------------------------+
| 1.4.2   | 2016-03-14 | Fix `issue #3                                 |
|         |            | <https://github.com/qtfkwk/kron/issues/3>`_;  |
|         |            | add release script; fix versions table        |
+---------+------------+-----------------------------------------------+
| 1.5.0   | 2016-03-16 | Support Python 3.5.1 and 2.7.11; default NTP  |
|         |            | server: us.pool.ntp.org; fix release script   |
+---------+------------+-----------------------------------------------+

Issues
======

Please view/report any issues
`here <https://github.com/qtfkwk/kron/issues?utf8=✓&q=is%3Aissue>`_.

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

* Python 3
* Command line tool

    * Timezone searching
    * List formats
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
  `Wikipedia <https://en.wikipedia.org/wiki/Network_Time_Protocol>`_,
  `IETF <https://tools.ietf.org/html/rfc1305>`_
* ``strftime`` at
  `linux.die.net <http://linux.die.net/man/3/strftime>`_,
  `Python time.strftime
  <https://docs.python.org/2/library/time.html#time.strftime>`_

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

