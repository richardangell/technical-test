"""Module for writing the accumulated output to text file."""

from pathlib import Path

from .accumulate import AccumulatedData
from .checks import check_condition, check_type


class Writer:
    def __init__(self, filename: str):

        check_type(filename, str, "filename")

        file = Path(filename)
        file_extension = file.suffixes

        check_condition(len(file_extension) == 1, "filename has one extension")
        check_condition(file_extension[0] == ".txt", "filename has .txt extension")
        check_condition(not file.exists(), f"{filename} does not already exist")

        self.filename = filename

    def write(self, accumulated_data: AccumulatedData) -> None:

        processed_accumulated_data = (
            accumulated_data.process_accumulated_data_to_output_format()
        )

        with open(self.filename, "w") as f:
            for row in processed_accumulated_data:
                f.write(row + "\n")
