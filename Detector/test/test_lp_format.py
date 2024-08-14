import unittest
from Helpers.lp_format import *
class TestSum(unittest.TestCase):
    def test_format_license_plate_good_long(self):
        data = ["CB","123AS","PL"]
        code, res = format_license_plate(data)
        self.assertEqual(code, -1)
        self.assertEqual(res, "CB123AS")
    def test_format_license_plate_bad_long(self):
        data = ["ABAŻUR","TOJJKO","PL"]
        code, res = format_license_plate(data)
        print(res)
        self.assertEqual(code, 1)
        self.assertEqual(res, "")
    def test_format_license_plate_GOOD(self):
        data = ["DDZ","39414"]
        code, res = format_license_plate(data)
        print(res)
        self.assertEqual(code, -1)
        self.assertEqual(res, "DDZ39414")

if __name__ == '__main__':
    unittest.main()