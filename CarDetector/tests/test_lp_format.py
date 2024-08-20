import unittest
from Helpers.lp_format import *


class TestSum(unittest.TestCase):
    def test_format_license_plate_good_long(self):
        data = ["CB", "123AS", "PL"]
        self._extracted_from_test_format_license_plate_GOOD_3(data, -1, "CB123AS")

    def test_format_license_plate_bad_long(self):
        data = ["ABAŻUR", "TOJJKO", "PL"]
        self._extracted_from_test_format_license_plate_GOOD_3(data, 1, "")

    def test_format_license_plate_GOOD(self):
        data = ["DDZ", "39414"]
        self._extracted_from_test_format_license_plate_GOOD_3(data, -1, "DDZ39414")

    # TODO Rename this here and in `test_format_license_plate_good_long`, `test_format_license_plate_bad_long` and `test_format_license_plate_GOOD`
    def _extracted_from_test_format_license_plate_GOOD_3(self, data, arg1, arg2):
        code, res = format_license_plate(data)
        self.assertEqual(code, arg1)
        self.assertEqual(res, arg2)


if __name__ == "__main__":
    unittest.main()
