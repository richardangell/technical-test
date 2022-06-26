"""Module for writing the accumulated output to text file."""

from pathlib import Path

from .checks import check_condition, check_type

from typing import Union


class Writer:
    def __init__(self, filename: str):

        check_type(filename, str, "filename")

        file = Path(filename)
        file_extension = file.suffixes

        check_condition(len(file_extension) == 1, "filename has one extension")
        check_condition(file_extension[0] == ".txt", "filename has .txt extension")
        check_condition(not file.exists(), f"{filename} does not already exist")

        self.filename = filename

    def write(
        self, accumulated_data: dict[str, Union[int, list[Union[int, float]]]]
    ) -> None:

        processed_accumulated_data = self._process_accumulated_values_to_output_format(
            accumulated_data
        )

        with open(self.filename, "w") as f:
            for row in processed_accumulated_data:
                f.write(row + "\n")

    def _process_accumulated_values_to_output_format(
        self, accumulated_data: dict[str, Union[int, list[Union[int, float]]]]
    ) -> list[str]:

        processed_list = []

        processed_list.append(self._create_first_output_row(accumulated_data))

        for product, product_accumulated_list in accumulated_data.items():

            if product not in ["min_origin_year", "n_development_years"]:

                processed_list.append(
                    self._convert_accumulated_list_to_str(
                        product, product_accumulated_list
                    )
                )

        return processed_list

    def _create_first_output_row(
        self, accumulated_data: dict[str, Union[int, list[Union[int, float]]]]
    ) -> str:

        return f"""{accumulated_data["min_origin_year"]},{accumulated_data["n_development_years"]}"""

    def _convert_accumulated_list_to_str(
        self, product: str, accumulated_list: list[Union[int, float]]
    ) -> str:
        """Convert accumulated payment values to strings and concatenate with
        comma as separater into one string.
        """

        numeric_values_concatenated = ",".join(str(value) for value in accumulated_list)

        return f"{product},{numeric_values_concatenated}"
