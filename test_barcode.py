import unittest
import barcode
import example_data

SAMPLE_FILE = example_data.BARCODE_0


class BarcodeTestCase(unittest.TestCase):
    
    def test_trim_to_indicator(self):
        self.assertEqual(barcode.trim_to_indicator("@After Indicator", "@"), "@After Indicator")
        self.assertEqual(barcode.trim_to_indicator("Before Indicator@After Indicator", "@"), "@After Indicator")
        self.assertRaises(ValueError, barcode.trim_to_indicator, "no indicator", "@")
    
    def test_read_file_header(self):
        file_header = barcode.read_file_header(SAMPLE_FILE)
        
        self.assertIsInstance(file_header, barcode.FileHeader)
        self.assertEqual(file_header.data_element_separator, "\n")
        self.assertEqual(file_header.record_separator, "")
        self.assertEqual(file_header.segment_terminator, "\n")
        self.assertEqual(file_header.aamva_version_number, 10)
        self.assertEqual(file_header.issuer_identification_number, 636000)
        self.assertEqual(file_header.jurisdiction_version_number, 0)
        self.assertEqual(file_header.number_of_entries, 2)
        
        self.assertRaises(ValueError, barcode.read_file_header, "this file is short")
        self.assertRaises(ValueError, barcode.read_file_header, SAMPLE_FILE[1:])
        self.assertRaises(ValueError, barcode.read_file_header, SAMPLE_FILE.replace("ANSI ", "OOPS "))
    
    def test_read_subfile_designator(self):
        designator0 = barcode.read_subfile_designator(SAMPLE_FILE, 0)
        designator1 = barcode.read_subfile_designator(SAMPLE_FILE, 1)

        self.assertIsInstance(designator0, barcode.SubfileDesignator)
        self.assertIsInstance(designator1, barcode.SubfileDesignator)
        
        self.assertTupleEqual(designator0, ("DL", 41, 276))
        self.assertTupleEqual(designator1, ("ZV", 318, 8))

    def test_read_subfile(self):
        subfile0 = barcode.read_subfile(SAMPLE_FILE, "\n", "\n", "DL", 41, 276)
        subfile1 = barcode.read_subfile(SAMPLE_FILE, "\n", "\n", "ZV", 318, 8)
        
        self.assertIsInstance(subfile0, dict)
        self.assertIsInstance(subfile1, dict)
        
        self.assertIn("DCS", subfile0)
        self.assertIn("ZVA", subfile1)
        
        self.assertNotIn("", subfile0)
        self.assertNotIn("", subfile1)
        
        self.assertEqual(subfile0["_type"], "DL")
        self.assertEqual(subfile1["_type"], "ZV")
        
        self.assertRaises(ValueError,barcode.read_subfile, SAMPLE_FILE, "\n", "\n", "DL", 40, 276)
        self.assertRaises(ValueError,barcode.read_subfile, SAMPLE_FILE, "\n", "\n", "DL", 41, 275)

    def test_read_file(self):
        file = barcode.read_file("garbage" + SAMPLE_FILE + "garbage")
        
        self.assertIsInstance(file, barcode.File)
        self.assertIsInstance(file[0], barcode.FileHeader)
        self.assertIsInstance(file[1], dict)
        self.assertEqual(len(file.elements), 30)
        self.assertEqual(file.elements["_type"], ["DL", "ZV"])
        self.assertEqual(file.elements["DCS"], "SAMPLE")
        self.assertEqual(file.elements["ZVA"], "01")
        
        self.assertRaises(ValueError, barcode.read_file, "@\n\n\nANSI 636000100000")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
