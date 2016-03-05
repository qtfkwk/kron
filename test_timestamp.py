import unittest
import timestamp
import tzlocal
class Test(unittest.TestCase):
    def test_timezone_search_default(self):
        h = timestamp.timezone.search()
        w = tzlocal.get_localzone().zone
        self.assertEqual(h, w)
