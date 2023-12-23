import unittest
import barcode


class TestBarcode(unittest.TestCase):
    
    def setUp(self) -> None:
        self.example_file = """@

ANSI 636000100002DL00410276ZV03180008DLDAQT64235789
DCSSAMPLE
DDEN
DACMICHAEL
DDFN
DADJOHN
DDGN
DCUJR
DCAD
DCBK
DCDPH
DBD06062019
DBB06061986
DBA12102024
DBC1
DAU068 in
DAYBRO
DAG2300 WEST BROAD STREET
DAIRICHMOND
DAJVA
DAK232690000 
DCF2424244747474786102204
DCGUSA
DCK123456789
DDAF
DDB06062018
DDC06062020
DDD1
ZVZVA01

"""
        return super().setUp()
    
    def test_trim_to_indicator(self):
        self.assertEqual(barcode.trim_to_indicator("@After Indicator", "@"), "@After Indicator")
        self.assertEqual(barcode.trim_to_indicator("Before Indicator@After Indicator", "@"), "@After Indicator")
        self.assertRaises(ValueError, barcode.trim_to_indicator, "no indicator", "@")
    
    def test_read_file_header(self):
        file_header = barcode.read_file_header(self.example_file)
        
        self.assertIsInstance(file_header, barcode.FileHeader)
        self.assertEqual(file_header.compliance_indicator, "@")
        self.assertEqual(file_header.data_element_separator, "\n")
        self.assertEqual(file_header.record_separator, "")
        self.assertEqual(file_header.segment_terminator, "\n")
        self.assertEqual(file_header.file_type, "ANSI ")
        self.assertEqual(file_header.aamva_version_number, 10)
        self.assertEqual(file_header.issuer_identification_number, 636000)
        self.assertEqual(file_header.jurisdiction_version_number, 0)
        self.assertEqual(file_header.number_of_entries, 2)
    
    def test_read_subfile_designators(self):
        file_header = barcode.read_file_header(self.example_file)
        subfile_designators = barcode.read_subfile_designators(self.example_file, file_header)
        
        self.assertIsInstance(subfile_designators, tuple)
        self.assertIsInstance(subfile_designators[0], barcode.SubfileDesignator)
        self.assertIsInstance(subfile_designators[1], barcode.SubfileDesignator)
        self.assertTupleEqual(subfile_designators, (("DL", 41, 276), ("ZV", 318, 8)))


if __name__ == "__main__":
    unittest.main()
