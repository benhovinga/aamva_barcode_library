from example_data import barcode0

def decode_license(raw_string: str):
    def next_bytes(string: str, index: int, byte_len: int):
        value = string[index:index + byte_len]
        next_index = index + byte_len
        return value, next_index
    
    def get_header(byte_string: str):
        HEADER_FIELDS = (
            # Field name, byte length, type
            ("compliance_indicator", 1, str),
            ("data_element_separator", 1, str),
            ("record_separator", 1, str),
            ("segment_terminator", 1, str),
            ("file_type", 5, str),
            ("issuer_identification_number", 6, int),
            ("aamva_version_number", 2, int),
            ("jurisdiction_version_number", 2, int),
            ("number_of_entries", 2, int),
            ("subfile_type", 2, str),
            ("offset", 4, int),
            ("length", 4, int)
        )
        index = 0
        header = dict()
        for field in HEADER_FIELDS:
            header[field[0]], index = next_bytes(byte_string, index, field[1])
        return header
    
    def get_data(byte_string:str, header: dict):
        start = int(header["offset"])
        end = int(header["length"]) + start
        data_string = byte_string[start + 2:end-1]
        data_list = tuple(filter(None, data_string.split("\n")))
        mapped_data = tuple(map(lambda item: (item[:3], item[3:]), data_list))
        return mapped_data
    
    byte_string = raw_string[raw_string.index("@"):]
    # Start byte string from compliance indicator (@)
    
    header = get_header(byte_string)
    data = get_data(byte_string, header)
    
    return header, data


from pprint import pprint
pprint(decode_license(barcode0))
