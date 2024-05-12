from __future__ import annotations
import datetime


COUNTRY_FORMAT = {
    "Canada": "YYYYMMDD",
    "Mexico": "YYYYMMDD",  # Assuming this format for Mexico, is untested
    "USA": "MMDDYYYY"}


class Date(datetime.date):
    @classmethod
    def parse_country_date(cls, date:str, country:str) -> Date:
        date_format = COUNTRY_FORMAT[country]
        year_index = date_format.index("YYYY")
        month_index = date_format.index("MM")
        day_index = date_format.index("DD")
        year = int(date[year_index:year_index + 4])
        month = int(date[month_index:month_index + 2])
        day = int(date[day_index:day_index + 2])
        return Date(year, month, day)
    
    def unparse_country_date(self, country: str) -> str:
        return COUNTRY_FORMAT[country] \
            .replace("YYYY", str(self.year).rjust(4, "0")) \
            .replace("MM", str(self.month).rjust(2, "0")) \
            .replace("DD", str(self.day).rjust(2, "0"))
