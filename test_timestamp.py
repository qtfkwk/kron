import unittest
import timestamp
import tzlocal
import pytz
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
