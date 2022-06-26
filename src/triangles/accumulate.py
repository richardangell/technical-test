"""Module dealing with accumulating incremental payment values."""

import pandas as pd
from dataclasses import dataclass

from typing import Union

from .checks import check_type


@dataclass
class AccumulatedData:

    min_origin_year: int
    n_development_years: int
    accumulated_data: dict[str, list[Union[int, float]]]

    def process_accumulated_data_to_output_format(self) -> list[str]:

        processed_list = [self._create_first_output_row()]

        for product, product_accumulated_list in self.accumulated_data.items():

            processed_list.append(
                self._convert_accumulated_list_to_str(product, product_accumulated_list)
            )

        return processed_list

    def _create_first_output_row(self) -> str:

        return f"""{self.min_origin_year},{self.n_development_years}"""

    def _convert_accumulated_list_to_str(
        self, product: str, accumulated_list: list[Union[int, float]]
    ) -> str:
        """Convert accumulated payment values to strings and concatenate with
        comma as separater into one string.
        """

        numeric_values_concatenated = ",".join(str(value) for value in accumulated_list)

        return f"{product},{numeric_values_concatenated}"


class Accumulator:
    """Class to accumulate incremental data."""

    def __init__(self, product: str, incremental_data: pd.DataFrame) -> None:

        check_type(product, str, "product")
        check_type(incremental_data, pd.DataFrame, "incremental_data")

        self.product = product
        self.incremental_data = incremental_data
        self.min_origin_year = incremental_data["Origin Year"].min()
        self.max_origin_year = incremental_data["Origin Year"].max()
        self.min_development_year = incremental_data["Development Year"].min()
        self.max_development_year = incremental_data["Development Year"].max()

        if self.max_origin_year != self.max_development_year:
            raise ValueError(
                f"expecting max origin and development years to be equal but got; {self.max_origin_year} and {self.max_development_year}"
            )

    def accumulate(self) -> AccumulatedData:
        """Accumulate incremental payment values and return all info to be
        written in the output file."""

        return AccumulatedData(
            min_origin_year=self.min_origin_year,
            n_development_years=self._get_n_development_years(),
            accumulated_data=self._accumulate_products(),
        )

    def _get_n_development_years(self) -> int:

        return self.max_origin_year - self.min_origin_year + 1

    def _accumulate_products(self) -> dict[str, list[Union[int, float]]]:
        """Accumulate incremental values for all products."""

        incremental_data_split = self._split_incremental_data(self.incremental_data)

        accumulated_product_data = {}

        for product, product_incremental_data in incremental_data_split.items():

            accumulated_product_data[product] = self._accumulate_product(
                product_incremental_data
            )

        return accumulated_product_data

    def _accumulate_product(
        self, product_incremental_data: pd.DataFrame
    ) -> list[Union[int, float]]:
        """Accumulate the incremental values for a single product over"""

        accumulated_values_list: list[Union[int, float]] = []

        for origin_year in range(self.min_origin_year, self.max_origin_year + 1):

            accumulated_value = 0.0

            for development_year in range(origin_year, self.max_origin_year + 1):

                incremental_value = product_incremental_data.loc[
                    (product_incremental_data["Origin Year"] == origin_year)
                    & (
                        product_incremental_data["Development Year"] == development_year
                    ),
                    "Incremental Value",
                ].sum()

                accumulated_value += incremental_value

                accumulated_values_list.append(accumulated_value)

        return accumulated_values_list

    def _split_incremental_data(self, df: pd.DataFrame) -> dict[str, pd.DataFrame]:
        """Method to split incremental data by product."""

        products = df["Product"].unique().tolist()

        df_split = {
            product: df.loc[df["Product"] == product].copy() for product in products
        }

        return df_split
