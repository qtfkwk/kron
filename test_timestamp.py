import unittest
import timestamp
import tzlocal
import pytz
import datetime
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
