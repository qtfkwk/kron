import unittest
import timestamp
import tzlocal
import pytz
import datetime
import time
class Test(unittest.TestCase):
    def test_timezone_search_default(self):
        h = timestamp.timezone.search()
        w = tzlocal.get_localzone().zone
        self.assertEqual(h, w)
    def test_timezone_search_complete_name(self):
        for w in pytz.all_timezones:
            h = timestamp.timezone.search(w)
            self.assertEqual(h, w)
    def test_timezone_search_lower_complete_name(self):
        for w in pytz.all_timezones:
            h = timestamp.timezone.search(w.lower())
            self.assertEqual(h, w)
    def test_timezone_search_partial(self):
        h = timestamp.timezone.search('Madrid')
        w = 'Europe/Madrid'
        self.assertEqual(h, w)
    def test_timezone_search_partial_lower(self):
        h = timestamp.timezone.search('madrid')
        w = 'Europe/Madrid'
        self.assertEqual(h, w)
    def test_timezone_search_multiple(self):
        h = timestamp.timezone.search('mad')
        w = ['Atlantic/Madeira', 'Europe/Madrid']
        self.assertEqual(h, w)
    def test_timezone_search_failure(self):
        h = timestamp.timezone.search('nonexistent')
        w = []
        self.assertEqual(h, w)
    def test_timezone_default(self):
        h = timestamp.timezone()
        w = tzlocal.get_localzone().zone
        self.assertEqual(h.original, None)
        self.assertEqual(h.name, w)
        self.assertIsInstance(h.pytz, datetime.tzinfo)
        self.assertEqual(h.pytz.zone, w)
    def test_timezone_name(self):
        n = 'UTC'
        h = timestamp.timezone(n)
        self.assertEqual(h.original, n)
        self.assertEqual(h.name, n)
        self.assertIsInstance(h.pytz, datetime.tzinfo)
        self.assertEqual(h.pytz.zone, n)
    def test_timezone_failure(self):
        n = 'nonexistent'
        self.assertRaises(timestamp.TimezoneFailure, timestamp.timezone, n)
    def test_timezone_multiple(self):
        n = 'mad'
        self.assertRaises(timestamp.TimezoneMultiple, timestamp.timezone, n)
    def test_duration_default(self):
        h = timestamp.duration()
        self.assertEqual(h.value, 0)
        self.assertIsInstance(h.value, float)
        w = dict(days=0, hours=0, minutes=0, seconds=0, microseconds=0)
        self.assertEqual(h.dict(), w)
    def test_duration_value1(self):
        w = 9876543.21
        h = timestamp.duration(w)
        self.assertEqual(h.value, w)
        w = dict(days=114, hours=7, minutes=29, seconds=3, microseconds=210000)
        self.assertEqual(h.dict(), w)
    def test_duration_value2(self):
        w = 1234567.89
        h = timestamp.duration(w)
        self.assertEqual(h.value, w)
        w = dict(days=14, hours=6, minutes=56, seconds=7, microseconds=890000)
        self.assertEqual(h.dict(), w)
    def test_duration_value3(self):
        w = 1231207.89
        h = timestamp.duration(w)
        self.assertEqual(h.value, w)
        w = dict(days=14, hours=6, minutes=0, seconds=7, microseconds=890000)
        self.assertEqual(h.dict(), w)
    def test_duration_cmp(self):
        d1 = timestamp.duration(1111111.111)
        d2 = timestamp.duration(2222222.222)
        d3 = timestamp.duration(2222222.222)
        d4 = timestamp.duration(3333333.333)
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
    def test_duration_math(self):
        d1 = timestamp.duration(1111111.111)
        d2 = timestamp.duration(2222222.222)
        d3 = timestamp.duration(2222222.222)
        d4 = timestamp.duration(3333333.333)
        d5 = timestamp.duration(1111116.111)
        d6 = timestamp.duration(1111106.111)
        d7 = timestamp.duration(5555555.555)
        d8 = timestamp.duration(2469135801975.3086)
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
        self.assertRaises(timestamp.DurationMultiplyError, multiply_durations)
        def divide_durations():
            return d1 / d2
        self.assertRaises(timestamp.DurationDivideError, divide_durations)
    def test_timestamp_default(self):
        h = timestamp.timestamp()
        self.assertIsInstance(h.value, float)
    def test_timestamp_int(self):
        w = 1457128501
        h = timestamp.timestamp(w)
        self.assertEqual(h.value, w)
        self.assertIsInstance(h.value, float)
    def test_timestamp_float(self):
        w = 1457128501.987349
        h = timestamp.timestamp(w)
        self.assertEqual(h.value, w)
        self.assertIsInstance(h.value, float)
    def test_timestamp_str1(self):
        h = timestamp.timestamp('2016-03-04 16:55:01', 'UTC')
        w = 1457128501
        self.assertEqual(h.value, w)
        self.assertIsInstance(h.value, float)
    def test_timestamp_str2(self):
        h = timestamp.timestamp('2016-03-04 11:55:01', 'EST')
        w = 1457128501
        self.assertEqual(h.value, w)
        self.assertIsInstance(h.value, float)
    def test_timestamp_str3(self):
        h = timestamp.timestamp('2016-03-04 17:55:01', 'Madrid')
        w = 1457128501
        self.assertEqual(h.value, w)
        self.assertIsInstance(h.value, float)
