# Name: kron
# Description: Uniform interface for dates and times
# Version: 1.6.12
# File: test_kron.py
# Author: qtfkwk <qtfkwk+kron@gmail.com>
# Copyright: (C) 2016 by qtfkwk
# License: BSD 2-Clause License (https://opensource.org/licenses/BSD-2-Clause)

# Variables

skip_network_tests = False
additional_ntp_servers = []

# Standard modules

import datetime
import json
import sys
import unittest

# External modules

import pytz
import tzlocal

# Internal modules

import kron

# Classes

class Test(unittest.TestCase):

    def test_timezone_search_default(self):
        h = kron.timezone.search()
        w = h
        try:
            w = tzlocal.get_localzone().zone
        except:
            pass
        self.assertEqual(h, w)

    def test_timezone_search_complete_name(self):
        for w in pytz.all_timezones:
            h = kron.timezone.search(w)
            self.assertEqual(h, w)

    def test_timezone_search_lower_complete_name(self):
        for w in pytz.all_timezones:
            h = kron.timezone.search(w.lower())
            self.assertEqual(h, w)

    def test_timezone_search_partial(self):
        h = kron.timezone.search('Madrid')
        w = 'Europe/Madrid'
        self.assertEqual(h, w)

    def test_timezone_search_partial_lower(self):
        h = kron.timezone.search('madrid')
        w = 'Europe/Madrid'
        self.assertEqual(h, w)

    def test_timezone_search_multiple(self):
        h = kron.timezone.search('mad')
        w = ['Atlantic/Madeira', 'Europe/Madrid']
        self.assertEqual(h, w)

    def test_timezone_search_failure(self):
        h = kron.timezone.search('nonexistent')
        w = []
        self.assertEqual(h, w)

    def test_timezone_search_all(self):
        h = kron.timezone.search('')
        w = pytz.all_timezones
        self.assertEqual(h, w)

    def test_timezone_default(self):
        h = kron.timezone()
        w = h.name
        try:
            w = tzlocal.get_localzone().zone
        except:
            pass
        self.assertEqual(h.original, None)
        self.assertEqual(h.name, w)
        self.assertIsInstance(h.pytz, datetime.tzinfo)
        self.assertEqual(h.pytz.zone, w)

    def test_timezone_name(self):
        n = 'UTC'
        h = kron.timezone(n)
        self.assertEqual(h.original, n)
        self.assertEqual(h.name, n)
        self.assertIsInstance(h.pytz, datetime.tzinfo)
        self.assertEqual(h.pytz.zone, n)

    def test_timezone_failure(self):
        n = 'nonexistent'
        self.assertRaises(kron.TimezoneFailure, kron.timezone, n)

    def test_timezone_multiple(self):
        n = 'mad'
        self.assertRaises(kron.TimezoneMultiple, kron.timezone, n)

    def test_duration_default(self):
        h = kron.duration()
        self.assertEqual(h.value, 0)
        self.assertIsInstance(h.value, float)
        w = dict(days=0, hours=0, minutes=0, seconds=0, microseconds=0)
        self.assertEqual(h.dict(), w)

    def test_duration_value1(self):
        w = 9876543.21
        h = kron.duration(w)
        self.assertEqual(h.value, w)
        w = dict(days=114, hours=7, minutes=29, seconds=3, microseconds=210000)
        self.assertEqual(h.dict(), w)

    def test_duration_value2(self):
        w = 1234567.89
        h = kron.duration(w)
        self.assertEqual(h.value, w)
        w = dict(days=14, hours=6, minutes=56, seconds=7, microseconds=890000)
        self.assertEqual(h.dict(), w)

    def test_duration_value3(self):
        w = 1231207.89
        h = kron.duration(w)
        self.assertEqual(h.value, w)
        w = dict(days=14, hours=6, minutes=0, seconds=7, microseconds=890000)
        self.assertEqual(h.dict(), w)

    def test_duration_cmp(self):
        d1 = kron.duration(1111111.111)
        d2 = kron.duration(2222222.222)
        d3 = kron.duration(2222222.222)
        d4 = kron.duration(3333333.333)
        # d1 < d2 == d3 < d4
        self.assertLess(d1, d2)          # d1 < d2
        self.assertLess(d1, d4)          # d1 < d4
        self.assertLessEqual(d1, d2)     # d1 <= d2
        self.assertLessEqual(d1, d4)     # d1 <= d4
        self.assertNotEqual(d1, d2)      # d1 != d2
        self.assertNotEqual(d1, d4)      # d1 != d4
        self.assertGreater(d4, d3)       # d4 > d3
        self.assertGreater(d4, d1)       # d4 > d1
        self.assertGreaterEqual(d4, d3)  # d4 >= d3
        self.assertGreaterEqual(d4, d1)  # d4 >= d1
        self.assertNotEqual(d4, d3)      # d4 != d3
        self.assertNotEqual(d4, d1)      # d4 != d1
        self.assertEqual(d2, d3)         # d2 == d3
        self.assertLessEqual(d2, d3)     # d2 <= d3
        self.assertGreaterEqual(d2, d3)  # d2 >= d3
        self.assertGreater(d1, 56)
        def cmp_str():
            d1 > 'impossible'
        self.assertRaises(kron.DurationComparisonError, cmp_str)

    def test_duration_math(self):
        d1 = kron.duration(1111111.111)
        d2 = kron.duration(2222222.222)
        d3 = kron.duration(2222222.222)
        d4 = kron.duration(3333333.333)
        d5 = kron.duration(1111116.111)
        d6 = kron.duration(1111106.111)
        d7 = kron.duration(5555555.555)
        d8 = kron.duration(2469135801975.3086)
        t1 = kron.timestamp(1457128501)
        t2 = d1 + t1
        i = 5
        f = 2222222.222
        self.assertEqual(d1 + d2, d4)  # d1 + d2 = d4
        self.assertEqual(d1 + i, d5)   # d1 + i = d5
        self.assertEqual(d1 + f, d4)   # d1 + f = d4
        self.assertEqual(d4 - d3, d1)  # d4 - d3 = d1
        self.assertEqual(d1 - i, d6)   # d1 - i = d6
        self.assertEqual(d4 - f, d1)   # d4 - f = d1
        self.assertEqual(d1 * i, d7)   # d1 * i = d7
        self.assertEqual(d1 * f, d8)   # d1 * f = d8
        self.assertEqual(d7 / i, d1)   # d7 / i = d1
        self.assertEqual(d8 / f, d1)   # d8 / f = d1
        def multiply_durations():
            return d1 * d2
        self.assertRaises(kron.DurationMultiplyError, multiply_durations)
        def divide_durations():
            return d1 / d2
        self.assertRaises(kron.DurationDivideError, divide_durations)
        def add_duration_string():
            return d1 + 'impossible'
        self.assertRaises(kron.DurationAddError, add_duration_string)
        def subtract_duration_string():
            return d1 - 'impossible'
        self.assertRaises(kron.DurationSubtractError, subtract_duration_string)
        self.assertIsInstance(t2, kron.timestamp)
        self.assertEqual(d1.value + t1.value, t2.value)
        def subtract_duration_timestamp():
            return d1 - t2
        self.assertRaises(kron.DurationSubtractError, \
            subtract_duration_timestamp)

    def test_timestamp_default(self):
        h = kron.timestamp()
        self.assertIsInstance(h.value, float)
        r = r'^\d{4}-\d\d-\d\d \d\d:\d\d:\d\d UTC$'
        if sys.version_info >= (3,):
            self.assertRegex(h.str('UTC'), r)
        else:
            self.assertRegexpMatches(h.str('UTC'), r)

    def test_timestamp_int(self):
        w = 1457128501
        h = kron.timestamp(w)
        self.assertEqual(h.value, w)
        self.assertIsInstance(h.value, float)
        w = dict(
            EST='2016-03-04 16:55:01',
            UTC='2016-03-04 21:55:01',
            CET='2016-03-04 22:55:01',
        )
        for tz, v in list(w.items()):
            self.assertEqual(h.str(tz), v + ' ' + tz)
            self.assertEqual(h.str(tz, 'basetz'), v + ' ' + tz)
            self.assertEqual(h.str(tz, 'base'), v)

    def test_timestamp_float(self):
        w = 1457128501.987349
        h = kron.timestamp(w)
        self.assertEqual(h.value, w)
        self.assertIsInstance(h.value, float)
        w = dict(
            EST='2016-03-04 16:55:01',
            UTC='2016-03-04 21:55:01',
            CET='2016-03-04 22:55:01',
        )
        for tz, v in list(w.items()):
            self.assertEqual(h.str(tz), v + ' ' + tz)
            self.assertEqual(h.str(tz, 'basetz'), v + ' ' + tz)
            self.assertEqual(h.str(tz, 'base'), v)

    def test_timestamp_str1(self):
        h = kron.timestamp('2016-03-04 21:55:01', 'UTC')
        w = 1457128501
        self.assertEqual(h.value, w)
        self.assertIsInstance(h.value, float)

    def test_timestamp_str2(self):
        h = kron.timestamp('2016-03-04 16:55:01', 'EST')
        w = 1457128501
        self.assertEqual(h.value, w)
        self.assertIsInstance(h.value, float)

    def test_timestamp_str3(self):
        h = kron.timestamp('2016-03-04 22:55:01', 'Madrid')
        w = 1457128501
        self.assertEqual(h.value, w)
        self.assertIsInstance(h.value, float)

    def test_timestamp_str4(self):
        v = '1457128501'
        h = kron.timestamp(v)
        self.assertEqual(h.value, float(v))
        self.assertIsInstance(h.value, float)

    def test_timestamp_str5(self):
        h = kron.timestamp('2016-03-04T21:55:01Z', fmt='iso8601')
        w = 1457128501
        self.assertEqual(h.value, w)
        self.assertIsInstance(h.value, float)

    def test_timestamp_str6(self):
        h = kron.timestamp('Fri, 04 Mar 2016 21:55:01', 'UTC', 'rfc2822_')
        w = 1457128501
        self.assertEqual(h.value, w)
        self.assertIsInstance(h.value, float)

    def test_timestamp_cmp(self):
        t1 = kron.timestamp(1457128501)
        t2 = kron.timestamp(1457128501.987349)
        t3 = kron.timestamp(1457128501.987349)
        t4 = kron.timestamp(1457128502)
        # t1 < t2 == t3 < t4
        self.assertLess(t1, t2)          # t1 < t2
        self.assertLess(t1, t4)          # t1 < t4
        self.assertLessEqual(t1, t2)     # t1 <= t2
        self.assertLessEqual(t1, t4)     # t1 <= t4
        self.assertNotEqual(t1, t2)      # t1 != t2
        self.assertNotEqual(t1, t4)      # t1 != t4
        self.assertGreater(t4, t3)       # t4 > t3
        self.assertGreater(t4, t1)       # t4 > t1
        self.assertGreaterEqual(t4, t3)  # t4 >= t3
        self.assertGreaterEqual(t4, t1)  # t4 >= t1
        self.assertNotEqual(t4, t3)      # t4 != t3
        self.assertNotEqual(t4, t1)      # t4 != t1
        self.assertEqual(t2, t3)         # t2 == t3
        self.assertLessEqual(t2, t3)     # t2 <= t3
        self.assertGreaterEqual(t2, t3)  # t2 >= t3
        def cmp_int(i):
            t1 > i
        self.assertRaises(kron.TimestampComparisonError, cmp_int, 6)
        def cmp_float(f):
            t1 < f
        self.assertRaises(kron.TimestampComparisonError, cmp_float, 7.2)
        def cmp_str(s):
            t1 == s
        self.assertRaises(kron.TimestampComparisonError, cmp_str, 'asdf')

    def test_timestamp_math(self):
        t1 = kron.timestamp(1457128501)
        t2 = kron.timestamp(1457128501.987349)
        t3 = kron.timestamp(1457128501.987349)
        t4 = kron.timestamp(1457128502)
        i = 1
        f = 0.987349
        # t1 < t2 == t3 < t4
        self.assertEqual(t1 + (t2 - t1), t3)  # t1 + (t2 - t1) = t3
        self.assertEqual(t1 + f, t2)          # t1 + f = t2
        self.assertEqual(t1 + i, t4)          # t1 + i = t4
        self.assertEqual(t4 - (t4 - t3), t2)  # t4 - (t4 - t3) = t2
        self.assertEqual(t4 - (1 - f), t3)    # t4 - (1 - f) = t3
        self.assertEqual(t4 - i, t1)          # t4 - i = t1
        # t1 * any raises
        def mul_ts(ts, y):
            ts * y
        self.assertRaises(kron.TimestampMultiplyError, mul_ts, t1, t2)
        self.assertRaises(kron.TimestampMultiplyError, mul_ts, t1, i)
        self.assertRaises(kron.TimestampMultiplyError, mul_ts, t1, f)
        # t1 / any raises
        def div_ts(ts, y):
            ts / y
        self.assertRaises(kron.TimestampDivideError, div_ts, t1, t2)
        self.assertRaises(kron.TimestampDivideError, div_ts, t1, i)
        self.assertRaises(kron.TimestampDivideError, div_ts, t1, f)
        def sub_str():
            t1 - 'impossible'
        self.assertRaises(kron.TimestampSubtractError, sub_str)
        def add_str():
            t1 + 'impossible'
        self.assertRaises(kron.TimestampAddError, add_str)

    def test_timestamp_formats(self):
        w = 1457139301.123456
        _h = kron.timestamp(w)
        tz = 'CST'
        h = _h.value
        self.assertEqual(h, w)
        self.assertIsInstance(h, float)
        f = dict(
            Day_Month_Nth='Friday, March 4th',
            Day_Month_Nth_YYYY='Friday, March 4th, 2016',
            HH='18',
            HHMM='1855',
            HHMMSS='185501',
            HH_MM='18:55',
            HH_MM_SS='18:55:01',
            MM='55',
            Month_Nth='March 4th',
            Month_Nth_YYYY='March 4th, 2016',
            SS='01',
            abbr_date='Fri, Mar 04, 2016',
            abbr_month='Mar',
            abbr_weekday='Fri',
            ampm='PM',
            base='2016-03-04 18:55:01',
            basetz='2016-03-04 18:55:01 CST',
            ccyy='2016',
            ccyymm='201603',
            ccyymmdd='20160304',
            d='Fri',
            date='Friday, March 04, 2016',
            day='Friday',
            dd='04',
            dd_Mon_yyyy='04 Mar 2016',
            hh='06',
            hh_MM='06:55',
            hh_MM_SS='06:55:01',
            hh_MM_SS_ampm='06:55:01 PM',
            hh_MM_ampm='06:55 PM',
            hours='18',
            hours12='06',
            hours24='18',
            iso8601='2016-03-05T00:55:01Z',
            julian='064',
            microseconds='123456',
            minutes='55',
            mm='03',
            mm_dd_yy='03/04/16',
            mmdd='0304',
            mon='Mar',
            month='March',
            national='Fri Mar 04 18:55:01 CST 2016',
            national_date='03/04/16',
            national_time='18:55:01',
            rfc2822='Fri, 04 Mar 2016 18:55:01 -0600',
            seconds='01',
            tz='CST',
            tz_offset='-0600',
            week_number_mon='09',
            week_number_sun='09',
            weekday='Friday',
            year='2016',
            yy='16',
            yymm='1603',
            yymmdd='160304',
            yyyy='2016',
            yyyy_mm_dd='2016/03/04',
            yyyymm='201603',
            yyyymmdd='20160304',
        )
        for fmt, w in list(f.items()):
            h = _h.str(tz, fmt)
            self.assertEqual(h, w)

    def test_timestamp_dict(self):
        h = kron.timestamp(1457128501)
        w = {}
        w['UTC'] = dict(
            basetz='2016-03-04 21:55:01 UTC',
        )
        self.assertEqual(h.dict('UTC'), w)
        w['UTC']['base'] = '2016-03-04 21:55:01'
        self.assertEqual(h.dict('UTC', ['base', 'basetz']), w)
        self.assertEqual(h.dict('UTC', ['basetz', 'base']), w)
        w['EST'] = dict(
            base='2016-03-04 16:55:01',
            basetz='2016-03-04 16:55:01 EST',
        )
        self.assertEqual(h.dict(['EST', 'UTC'], ['base', 'basetz']), w)
        self.assertEqual(h.dict(['UTC', 'EST'], ['basetz', 'base']), w)
        w['CET'] = dict(
            base='2016-03-04 22:55:01',
            basetz='2016-03-04 22:55:01 CET',
        )
        self.assertEqual(h.dict(list(w.keys()), ['base', 'basetz']), w)

    def test_timestamp_pseudo_format_all(self):
        a = '1457128501'
        h = kron.timestamp(a)
        w = {a:dict(UTC=dict(
            HH='21',
            HHMM='2155',
            HHMMSS='215501',
            HH_MM='21:55',
            HH_MM_SS='21:55:01',
            MM='55',
            SS='01',
            abbr_date='Fri, Mar 04, 2016',
            abbr_month='Mar',
            abbr_weekday='Fri',
            ampm='PM',
            base='2016-03-04 21:55:01',
            basetz='2016-03-04 21:55:01 UTC',
            ccyy='2016',
            ccyymm='201603',
            ccyymmdd='20160304',
            d='Fri',
            date='Friday, March 04, 2016',
            day='Friday',
            dd='04',
            dd_Mon_yyyy='04 Mar 2016',
            hh='09',
            hh_MM='09:55',
            hh_MM_SS='09:55:01',
            hh_MM_SS_ampm='09:55:01 PM',
            hh_MM_ampm='09:55 PM',
            hours='21',
            hours12='09',
            hours24='21',
            iso8601='2016-03-04T21:55:01Z',
            julian='064',
            microseconds='000000',
            minutes='55',
            mm='03',
            mm_dd_yy='03/04/16',
            mmdd='0304',
            mon='Mar',
            month='March',
            national='Fri Mar 04 21:55:01 UTC 2016',
            national_date='03/04/16',
            national_time='21:55:01',
            rfc2822='Fri, 04 Mar 2016 21:55:01 +0000',
            rfc2822_='Fri, 04 Mar 2016 21:55:01',
            seconds='01',
            tz='UTC',
            tz_offset='+0000',
            week_number_mon='09',
            week_number_sun='09',
            weekday='Friday',
            year='2016',
            yy='16',
            yymm='1603',
            yymmdd='160304',
            yyyy='2016',
            yyyy_mm_dd='2016/03/04',
            yyyymm='201603',
            yyyymmdd='20160304',
        ))}
        self.maxDiff = None
        self.assertEqual(h.dict('UTC', 'all'), w[a])
        self.assertEqual(kron.cli(['-t', 'UTC', '-f', 'all', a]), \
            kron._json(w))

    def test_timestamp_json(self):
        h = kron.timestamp(1457128501)
        w = {}
        w['UTC'] = dict(
            basetz='2016-03-04 21:55:01 UTC',
        )
        self.assertEqual(h.json('UTC'), kron._json(w))
        w['UTC']['base'] = '2016-03-04 21:55:01'
        self.assertEqual(h.json('UTC', ['base', 'basetz']), kron._json(w))
        self.assertEqual(h.json('UTC', ['basetz', 'base']), kron._json(w))
        w['EST'] = dict(
            base='2016-03-04 16:55:01',
            basetz='2016-03-04 16:55:01 EST',
        )
        self.assertEqual(h.json(['EST', 'UTC'], ['base', 'basetz']), \
            kron._json(w))
        self.assertEqual(h.json(['UTC', 'EST'], ['basetz', 'base']), \
            kron._json(w))
        w['CET'] = dict(
            base='2016-03-04 22:55:01',
            basetz='2016-03-04 22:55:01 CET',
        )
        self.assertEqual(h.json(list(w.keys()), ['base', 'basetz']), kron._json(w))

    def test_timestamp_utc(self):
        h = kron.timestamp(1457128501)
        w = '2016-03-04 21:55:01 UTC'
        self.assertEqual(h.str('UTC'), w)
        self.assertEqual(h.utc(), w)
        self.assertEqual(h.utc('basetz'), w)
        w = '2016-03-04 21:55:01'
        self.assertEqual(h.utc('base'), w)

    def test_timestamp_rfc2822(self):
        h = kron.timestamp(1457128501)
        w = 'Fri, 04 Mar 2016 21:55:01 +0000'
        self.assertEqual(h.str('UTC', 'rfc2822'), w)
        self.assertEqual(h.rfc2822('UTC'), w)

    def test_timestamp_iso8601(self):
        h = kron.timestamp(1457128501)
        w = '2016-03-04T21:55:01Z'
        self.assertEqual(h.str(fmt='iso8601'), w)
        self.assertEqual(h.iso8601(), w)

    @classmethod
    def _args(cls, a, t, f, T=[], F=[]):
        """convert arguments into an argv list"""
        r = []
        for i in (('-t', t), ('-f', f), ('-T', T), ('-F', F)):
            for j in i[1]:
                r.extend([i[0], j])
        r.extend(a)
        return r

    def test_cli1(self):
        """single timezone, default format"""
        a = ['1457128501']
        t = ['UTC']
        f = []
        h = kron.cli(self._args(a, t, f))
        w = '2016-03-04 21:55:01 UTC'
        self.assertEqual(h, w)

    def test_cli2(self):
        """single timezone, single format"""
        a = ['1457128501']
        t = ['UTC']
        f = ['national']
        h = kron.cli(self._args(a, t, f))
        w = 'Fri Mar 04 21:55:01 UTC 2016'
        self.assertEqual(h, w)

    def test_cli3(self):
        """single timezone, multiple formats
        multiple timezones, multiple formats"""
        a = ['1457128501']
        w = {a[0]:dict(UTC=dict(
            HH='21',
            HHMM='2155',
            HHMMSS='215501',
            HH_MM='21:55',
            HH_MM_SS='21:55:01',
            MM='55',
            SS='01',
            abbr_date='Fri, Mar 04, 2016',
            abbr_month='Mar',
            abbr_weekday='Fri',
            ampm='PM',
            base='2016-03-04 21:55:01',
            basetz='2016-03-04 21:55:01 UTC',
            ccyy='2016',
            ccyymm='201603',
            ccyymmdd='20160304',
            date='Friday, March 04, 2016',
            dd='04',
            hh='09',
            hh_MM='09:55',
            hh_MM_SS='09:55:01',
            hh_MM_SS_ampm='09:55:01 PM',
            hh_MM_ampm='09:55 PM',
            hours='21',
            hours12='09',
            hours24='21',
            iso8601='2016-03-04T21:55:01Z',
            julian='064',
            microseconds='000000',
            minutes='55',
            mm='03',
            mm_dd_yy='03/04/16',
            mmdd='0304',
            mon='Mar',
            month='March',
            national='Fri Mar 04 21:55:01 UTC 2016',
            national_date='03/04/16',
            national_time='21:55:01',
            rfc2822='Fri, 04 Mar 2016 21:55:01 +0000',
            seconds='01',
            tz='UTC',
            tz_offset='+0000',
            week_number_mon='09',
            week_number_sun='09',
            weekday='Friday',
            year='2016',
            yy='16',
            yymm='1603',
            yymmdd='160304',
            yyyy='2016',
            yyyy_mm_dd='2016/03/04',
            yyyymm='201603',
            yyyymmdd='20160304',
        ))}
        t = ['UTC']
        f = sorted(w[a[0]]['UTC'].keys())
        self.assertEqual(kron.cli(self._args(a, t, f)), kron._json(w))
        t.append('PST8PDT')
        w[a[0]]['PST8PDT'] = dict(
            HH='13',
            HHMM='1355',
            HHMMSS='135501',
            HH_MM='13:55',
            HH_MM_SS='13:55:01',
            MM='55',
            SS='01',
            abbr_date='Fri, Mar 04, 2016',
            abbr_month='Mar',
            abbr_weekday='Fri',
            ampm='PM',
            base='2016-03-04 13:55:01',
            basetz='2016-03-04 13:55:01 PST',
            ccyy='2016',
            ccyymm='201603',
            ccyymmdd='20160304',
            date='Friday, March 04, 2016',
            dd='04',
            hh='01',
            hh_MM='01:55',
            hh_MM_SS='01:55:01',
            hh_MM_SS_ampm='01:55:01 PM',
            hh_MM_ampm='01:55 PM',
            hours='13',
            hours12='01',
            hours24='13',
            iso8601='2016-03-04T21:55:01Z',
            julian='064',
            microseconds='000000',
            minutes='55',
            mm='03',
            mm_dd_yy='03/04/16',
            mmdd='0304',
            mon='Mar',
            month='March',
            national='Fri Mar 04 13:55:01 PST 2016',
            national_date='03/04/16',
            national_time='13:55:01',
            rfc2822='Fri, 04 Mar 2016 13:55:01 -0800',
            seconds='01',
            tz='PST',
            tz_offset='-0800',
            week_number_mon='09',
            week_number_sun='09',
            weekday='Friday',
            year='2016',
            yy='16',
            yymm='1603',
            yymmdd='160304',
            yyyy='2016',
            yyyy_mm_dd='2016/03/04',
            yyyymm='201603',
            yyyymmdd='20160304',
        )
        self.assertEqual(kron.cli(self._args(a, t, f)), kron._json(w))

    def test_cli4(self):
        """multiple timezones, default format"""
        a = ['1457128501']
        t = ['UTC', 'EST5EDT']
        f = []
        h = kron.cli(self._args(a, t, f))
        w = kron._json({a[0]:dict(
            EST5EDT=dict(basetz='2016-03-04 16:55:01 EST'),
            UTC=dict(basetz='2016-03-04 21:55:01 UTC'),
        )})
        self.assertEqual(h, w)

    def test_cli5(self):
        """multiple timezones, single format"""
        a = ['1457128501']
        t = ['UTC', 'PST8PDT']
        f = ['rfc2822']
        w = kron._json({a[0]:dict(
            PST8PDT=dict(rfc2822='Fri, 04 Mar 2016 13:55:01 -0800'),
            UTC=dict(rfc2822='Fri, 04 Mar 2016 21:55:01 +0000'),
        )})
        h = kron.cli(self._args(a, t, f))
        self.assertEqual(h, w)

    def test_cli6(self):
        """timestamp in base format"""
        a = ['2016-03-04 21:55:01']
        T = ['UTC']
        t = ['UTC']
        f = []
        h = kron.cli(self._args(a, t, f, T))
        w = '2016-03-04 21:55:01 UTC'
        self.assertEqual(h, w)

    def test_cli7(self):
        """timestamp in iso8601 format"""
        a = ['2014-01-23T09:06:12Z']
        T = []
        F = ['iso8601']
        t = ['UTC']
        f = []
        h = kron.cli(self._args(a, t, f, T, F))
        w = '2014-01-23 09:06:12 UTC'
        self.assertEqual(h, w)

    def test_cli8(self):
        """version"""
        w = kron.__version__
        self.assertEqual(kron.cli(['-V']), w)
        self.assertEqual(kron.cli(['--version']), w)

    def test_cli_search_timezone(self):
        h = kron.cli(['-s', ''])
        w = '\n'.join(pytz.all_timezones)
        self.assertEqual(h, w)

    def test_cli_search_timezone_partial_lower(self):
        h = kron.cli(['-s', 'madrid'])
        w = 'Europe/Madrid'
        self.assertEqual(h, w)

    def test_cli_search_timezone_multiple(self):
        h = kron.cli(['-s', 'mad'])
        w = '\n'.join(['Atlantic/Madeira', 'Europe/Madrid'])
        self.assertEqual(h, w)

    def test_time_utc(self):
        self.assertIsInstance(kron.time_utc(), float)
        self.assertIsInstance(kron.time_utc(123456.789), float)
        h = kron.time_utc(datetime.datetime.now())
        self.assertIsInstance(h, float)
        self.assertRaises(kron.TimeEpochError, kron.time_utc, 'nonexistent')

    @unittest.skipIf(skip_network_tests, \
    'skipping NTP tests that require network')
    def test_time_ntp_with_network(self):
        self.assertIsInstance(kron.time_ntp(), float)
        for s in additional_ntp_servers:
            self.assertIsInstance(kron.time_ntp(s), float)
        self.assertIsInstance(kron.time(ntp=True), float)
        self.assertIsInstance(kron.timestamp(ntp=True), kron.timestamp)

    def test_time_ntp(self):
        self.assertRaises(kron.NTPError, kron.time_ntp, 'nonexistent')

    def test_time(self):
        self.assertIsInstance(kron.time(), float)
        self.assertRaises(kron.TimeTimezoneError, kron.time, None, 'UTC')
        self.assertRaises(kron.TimeFormatError, kron.time, None, None, 'base')
        w = 1457128501
        h = kron.time('2016-03-04 21:55:01', 'UTC')
        self.assertIsInstance(h, float)
        self.assertEqual(h, w)
        h = kron.time('2016-03-04 16:55:01', 'EST')
        self.assertIsInstance(h, float)
        self.assertEqual(h, w)
        h = kron.time('2016-03-04 22:55:01', 'Madrid')
        self.assertIsInstance(h, float)
        self.assertEqual(h, w)
        h = kron.time('2016-03-04T21:55:01Z', fmt='iso8601')
        self.assertIsInstance(h, float)
        self.assertEqual(h, w)
        h = kron.time('Fri, 04 Mar 2016 21:55:01', 'UTC', 'rfc2822_')
        self.assertIsInstance(h, float)
        self.assertEqual(h, w)

if __name__ == '__main__':
    unittest.main()

