from BarcodeFile import BarcodeFile
import example_data

file = BarcodeFile.from_str(example_data.barcode0)
print(file)
print(file.to_str())

