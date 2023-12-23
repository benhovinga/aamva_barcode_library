import unittest
import barcode


class TestBarcode(unittest.TestCase):
    
    def test_trim_to_indicator(self):
        self.assertEqual(barcode.trim_to_indicator("@After Indicator", "@"), "@After Indicator")
        self.assertEqual(barcode.trim_to_indicator("Before Indicator@After Indicator", "@"), "@After Indicator")
        self.assertRaises(ValueError, barcode.trim_to_indicator, "no indicator", "@")


if __name__ == "__main__":
    unittest.main()
