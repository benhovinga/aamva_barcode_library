from example_data import barcode1, barcode2

HEADER_LENGTH = 21

type Header = tuple[str, str, str, str, str, int, int, int, int]
type SubfileDesignator = tuple[str, int, int]
type Subfile = dict[str, str]


def validate_header(blob: str) -> None:
    """Raises an excpetion if header fails checks"""
    if len(blob) < HEADER_LENGTH:
        raise Exception('Header too short')
    elif blob[0] != '@':
        raise Exception('Missing compliance indicator')
    elif blob[4:9] != 'ANSI ':
        raise Exception('Header missing file type')

def read_header(blob: str) -> Header:
    header: Header = (
        str(blob[0]),       # Compliance Indicator
        str(blob[1]),       # Data Element Separator
        str(blob[2]),       # Record Separator
        str(blob[3]),       # Segment Terminator
        str(blob[4:9]),     # File Type
        int(blob[9:15]),    # Issuer Identification Number
        int(blob[15:17]),   # AAMVA Version Number
        int(blob[17:19]),   # Jurisdiction Version Number
        int(blob[19:21])    # Number of Entries
    )
    return header

def read_subfile_designators(blob: str, header: Header) -> list[SubfileDesignator]:
    output: list[SubfileDesignator] = []
    for i in range(header[8]):
        start: int = i * 10 + HEADER_LENGTH
        designator: SubfileDesignator = (
            str(blob[start:start+2]),       # Subfile Type
            int(blob[start+2:start+6]),     # Offset
            int(blob[start+6:start+10])     # Length
        )
        output.append(designator)
    return output

def read_subfile(blob: str, header: Header, designator: SubfileDesignator) -> Subfile:
    def trim_subfile() -> str:
        start: int = designator[1]
        end: int = designator[1] + designator[2]
        if blob[start:start + 2] != designator[0]:
            raise Exception('Subfile and designator are not the same type')
        elif blob[end] != header[3]:
            raise Exception('Subfile missing segment terminator')
        return blob[start + 2: end - 1]
    
    sub_blob: str = trim_subfile()
    elements: list[str] = sub_blob.split(header[1])
    elements: list[str] = filter(None, map(lambda i: i.strip(), elements))
    subfile: Subfile = {}
    for row in elements:
        key: str = row[:3]
        value: str = row[3:]
        subfile[key] = value
    return subfile

def parse_data_elements(subfile: Subfile):
    pass

identification1 = dict()
identification2 = dict()

# Validation
validate_header(barcode1)
validate_header(barcode2)

# Read Header
header1: Header = read_header(barcode1)
header2: Header = read_header(barcode2)
print(header1)
print(header2)

# Read all Subfile Designators
sub_des1: SubfileDesignator = read_subfile_designators(barcode1, header1)
sub_des2: SubfileDesignator = read_subfile_designators(barcode2, header2)
print(sub_des1)
print(sub_des2)

# Read first subfile
subfile1 = read_subfile(barcode1, header1, sub_des1[0])
del barcode1, header1, sub_des1
subfile2 = read_subfile(barcode2, header2, sub_des2[0])
print(subfile1)
print(subfile2)