from enum import Enum

import turbo.exceptions
import turbo.format_functions


class PrintFormats(Enum):
    TABLE = "table"
    RAW = "raw"

    def get_format_function(self):
        if self.name == "table":
            return turbo.format_functions.get_lines
        if self.name == "raw":
            return turbo.format_functions.raw_pprint
        raise turbo.exceptions.NotFound()


def initialize_format_from_string(format_str):
    try:
        return PrintFormats[
            format_str.lower()
        ]  # Convert to lowercase for case-insensitive matching
    except KeyError:
        raise turbo.exceptions.MissingConfig("format not found")
