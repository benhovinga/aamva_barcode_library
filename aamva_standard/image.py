from PIL import Image as PIL
from pdf417decoder import PDF417Decoder
from barcode import parse_file
from pprint import pprint

image = PIL.open("_private/license.png")
decoder = PDF417Decoder(image)

if (decoder.decode() > 0):
    decoded = decoder.barcode_data_index_to_string(0)
    file = parse_file(decoded)
    pprint(file)
