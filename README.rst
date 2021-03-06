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
* `Named formats <https://kron.readthedocs.io/#id11>`_
* Timestamp object "helper" methods for timezones and formats
* Command line tool
* Substitutes for ``time.time()``:
  `time <https://kron.readthedocs.io/#id14>`_,
  `time_ntp <https://kron.readthedocs.io/#id15>`_,
  `time_utc <https://kron.readthedocs.io/#id16>`_
* Supports Python versions >= 3.5.1 and >= 2.7.11

