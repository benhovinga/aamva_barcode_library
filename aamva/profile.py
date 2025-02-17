from datetime import date
from typing import Union, Mapping

from barcode import BarcodeFile
from dates import get_date_format
from issuing_authority import get_authority_by_id


def build_profile(barcode_file: BarcodeFile) -> Mapping[str, Union[str, int, date]]:
    aamva_version = barcode_file.header.aamva_version
    issuing_authority = get_authority_by_id(barcode_file.header.issuer_id)
    country = issuing_authority.country
    date_format = get_date_format(aamva_version, country)
