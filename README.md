# AAMVA DL/ID Barcode Library

### Version: v0.5-beta

*The American Association of Motor Vehicle Administrators* (AAMVA) releases a standards guide for driver license and identification card design. The *[2020 AAMVA DL/ID Card Design Standard](https://www.aamva.org/getmedia/99ac7057-0f4d-4461-b0a2-3a5532e1b35c/AAMVA-2020-DLID-Card-Design-Standard.pdf)* outlines the specifications for the Mandatory PDF417 Bar Code in Annex D.

This library isn't intended to "scan" these barcodes, but rather parse the data passed in from a barcode scanning tool. The end goal is to display a cards profile in a human readable format.

## Quick Start Example

```python
>>> from aamva.barcode import parse_barcode_string

>>> barcode_string = "@\n\x1e\rANSI 636000100102DL00410278ZV03190008DLDAQT64235789\nDCSSAMPLE\nDDEN\nDACMICHAEL\nDDFN\nDADJOHN\nDDGN\nDCUJR\nDCAD\nDCBK\nDCDPH\nDBD06062019\nDBB06061986\nDBA12102024\nDBC1\nDAU068 in\nDAYBRO\nDAG2300 WEST BROAD STREET\nDAIRICHMOND\nDAJVA\nDAK232690000  \nDCF2424244747474786102204\nDCGUSA\nDCK123456789\nDDAF\nDDB06062018\nDDC06062020\nDDD1\rZVZVA01\r"
# Example output string from PDF417 barcode scanning tool

>>> barcode_file = parse_barcode_string(barcode_string)
# Parse the barcode string to extract the subfiles and elements

>>> barcode_file
# BarcodeFile(header=FileHeader(issuer_id=636000, aamva_version=10, number_of_entries=2, jurisdiction_version=1), subfiles=(Subfile(subfile_type='DL', elements={'DAQ': 'T64235789', 'DCS': 'SAMPLE', 'DDE': 'N', 'DAC': 'MICHAEL', 'DDF': 'N', 'DAD': 'JOHN', 'DDG': 'N', 'DCU': 'JR', 'DCA': 'D', 'DCB': 'K', 'DCD': 'PH', 'DBD': '06062019', 'DBB': '06061986', 'DBA': '12102024', 'DBC': '1', 'DAU': '068 in', 'DAY': 'BRO', 'DAG': '2300 WEST BROAD STREET', 'DAI': 'RICHMOND', 'DAJ': 'VA', 'DAK': '232690000  ', 'DCF': '2424244747474786102204', 'DCG': 'USA', 'DCK': '123456789', 'DDA': 'F', 'DDB': '06062018', 'DDC': '06062020', 'DDD': '1'}), Subfile(subfile_type='ZV', elements={'ZVA': '01'})))
```

Currently in `v0.5-beta` the we can take the barcode file string (captured from a barcode scanning tool) and break it down into it's various parts. These parts are the file header, subfiles, and subfile elements.

The subfile elements is where the profile is stored. This is information like first name, last name, birthday, etc. Profile propertie names like `customer_family_name` are too large for the limited space of the barcode so all property names have been encoded with a three letter name, like `DCS`. This is a form of compression the barcode file uses.

In addition to encoding property names, many properties have different encoding methods for their values. For example gender is represented by an int. 1 = male, 2 = female, 9 = not specified.

The next step in the development process is to decode each of the subfile element into human readable propeties.

## Resources

Below are some resources that made creating this library possible.

- [AAMVA 2020 DL/ID Card Design Standard](https://www.aamva.org/getmedia/99ac7057-0f4d-4461-b0a2-3a5532e1b35c/AAMVA-2020-DLID-Card-Design-Standard.pdf) (aamva.org)
    - Annex D - Mandatory PDF417 Bar Code
    - _The encoding scheme in Annex I (Optional Comact Encoding) is not yet implemented_
- [AAMVA D20 Data Dictionary 7.0](https://www.aamva.org/getmedia/4373f9e2-468b-4304-b0ee-12d7c867ad7e/D20-Data-Dictionary-7-0.pdf) (aamva.org)
    - A.9.2 Driver Eye Color
    - A.9.3 Driver Hair Color
    - A.9.8 Driver Race and Ethnicity
- [List of Issuer Identification Numbers (IIN)](https://www.aamva.org/identity/issuer-identification-numbers-(iin)) (aamva.org)
- [Some older standards listed here](https://docs.scandit.com/parser/dlid.html)


## Deep Dive

I will write about the process later... 😮‍💨