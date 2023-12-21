from BarcodeFile import BarcodeFile
import example_data

file = BarcodeFile.decode(example_data.barcode0)
print(dir(file))
print(file.encode())

