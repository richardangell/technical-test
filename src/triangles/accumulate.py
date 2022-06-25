import pandas as pd

from typing import Union

from .checks import check_type


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

    def accumulate(self) -> dict[str, Union[int, list[Union[int, float]]]]:
        """Accumulate incremental payment values and return all info to be
        written in the output file."""

        development_years_info = self._get_development_years_info()

        accumulated_product_data = self._accumulate_products()

        return development_years_info | accumulated_product_data

    def _get_development_years_info(self) -> dict[str, int]:

        development_years_info = {
            "min_origin_year": self.min_origin_year,
            "n_development_year": self._get_n_development_years(),
        }

        return development_years_info

    def _get_n_development_years(self) -> int:

        return self.max_origin_year - self.min_origin_year

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
