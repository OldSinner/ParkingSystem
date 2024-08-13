import unittest
from lp_format import *
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

if __name__ == '__main__':
    unittest.main()