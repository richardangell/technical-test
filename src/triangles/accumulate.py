"""Module dealing with accumulating incremental payment values."""

import pandas as pd
from dataclasses import dataclass

from typing import Union

from .checks import check_type


@dataclass
class AccumulatedData:
    """Class to hold accumulated payment data.

    Parameters
    ----------
    min_origin_year : int
        The minimum origin year that all the accumulated data starts from.

    n_development_years : int
        The number of development years, from the origin year in the data.

    accumulated_data : dict[str, list[Union[int, float]]]
        Accumulated data for each product. Keys of the dict give the name
        of the product. Each corresponding item in the dict is a list
        of numeric values giving the accumulated payment data. So for
        example values [0, 50, 100, 20, 55.5, 99] for key "x" and
        min_origin_year = 2000 and n_development_years = 3 would indicate
        that for product "x" the cumulative payments for claims in 2000
        where 0 in year 2000, 50 in 2001 and 100 in 2002, for claims in 2001
        the cumulative payments were 20 in 2001 and 55.5 in 2002 and finally
        for claims in 2002 the cumulative payments were 99 in 2002.

    """

    min_origin_year: int
    n_development_years: int
    accumulated_data: dict[str, list[Union[int, float]]]

    def process_accumulated_data_to_output_format(self) -> list[str]:
        """Process the accumulated data into output format.

        Returns
        list[str]
            The output format is a list of strings where the first string is
            the min_origin_year and n_development_years separated by a comma.
            Subsequent rows contain a comma separated list for a specific
            product of accumulated payment data. The first value in the list
            gives the name of the product.

        """

        processed_list = [self._create_first_output_row()]

        for product, product_accumulated_list in self.accumulated_data.items():

            processed_list.append(
                self._convert_accumulated_list_to_str(product, product_accumulated_list)
            )

        return processed_list

    def _create_first_output_row(self) -> str:
        """Create the first row for the output format.

        Returns
        -------
        str
            Comma separated minimum origin year and number of development year
            values.

        """

        return f"""{self.min_origin_year},{self.n_development_years}"""

    def _convert_accumulated_list_to_str(
        self, product: str, accumulated_list: list[Union[int, float]]
    ) -> str:
        """Convert accumulated payment values to strings and concatenate with
        comma as separater into a single string.

        Returns
        -------
        str
            The output string is prepended with the name of the product,
            separated with a comma.

        """

        numeric_values_concatenated = ",".join(str(value) for value in accumulated_list)

        return f"{product},{numeric_values_concatenated}"


class Accumulator:
    """Class to accumulate incremental data.

    Parameters
    ----------
    incremental_data : pd.DataFrame
        Incremental data across all products.

    Raises
    ------
    TypeError
        If product is not a str.

    TypeError
        If incremental_data is not a pd.DataFrame.

    ValueError
        If the maximum origin and development years in the input DataFrame are
        not equal.

    """

    def __init__(self, incremental_data: pd.DataFrame) -> None:

        check_type(incremental_data, pd.DataFrame, "incremental_data")

        self.incremental_data = incremental_data
        self.min_origin_year = incremental_data["Origin Year"].min()
        self.max_development_year = incremental_data["Development Year"].max()

    def accumulate(self) -> AccumulatedData:
        """Accumulate incremental payment values and return all info required
        to be written to the output file.

        Returns
        -------
        AccumulatedData
            Accumulated payment data for all products.

        """

        return AccumulatedData(
            min_origin_year=self.min_origin_year,
            n_development_years=self._get_n_development_years(),
            accumulated_data=self._accumulate_products(),
        )

    def _get_n_development_years(self) -> int:
        """Calculate the maximum number of development years in the data."""

        return self.max_development_year - self.min_origin_year + 1

    def _accumulate_products(self) -> dict[str, list[Union[int, float]]]:
        """Accumulate incremental values for all products.

        Returns
        -------
        dict[str, list[Union[int, float]]]
            Dict of key, value pairs corresponding to a product name and the
            accumulated payment data for that product. See _accumulate_product
            method for the structure of the accumulated data.

        """

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
        """Accumulate the incremental payment values for a single product.

        Parameters
        ----------
        product_incremental_data : pd.DataFrame
            Incremental payment data for a single product. Each row gives the
            payments made in the development year for claims occuring in the
            origin year.

        Returns
        -------
        list[Union[int, float]]
            List of numeric accumulated payment values. The first value is the
            accumulated payments for the claims in the first origin year made
            in the same year. Then the next value is accumulated payments for
            claims in the first origin year but made in the second development
            year and so on. Once the maximum development year has been reached
            the next value in the list is accumulated payments for claims in
            the second origin year made in the same year and so on.

        """

        accumulated_values_list: list[Union[int, float]] = []

        for origin_year in range(self.min_origin_year, self.max_development_year + 1):

            accumulated_value = 0.0

            for development_year in range(origin_year, self.max_development_year + 1):

                incremental_value = product_incremental_data.loc[
                    (product_incremental_data["Origin Year"] == origin_year)
                    & (
                        product_incremental_data["Development Year"] == development_year
                    ),
                    "Incremental Value",
                ].sum()

                accumulated_value = round(accumulated_value + incremental_value, 2)

                accumulated_values_list.append(accumulated_value)

        return accumulated_values_list

    def _split_incremental_data(self, df: pd.DataFrame) -> dict[str, pd.DataFrame]:
        """Method to split incremental data by product.

        Returns
        -------
        dict[str, pd.DataFrame]
            Dictionary where each key, value pair is a product name and the
            corresponding rows from df that contain payment data for this
            product.

        """

        products = df["Product"].unique().tolist()

        df_split = {
            product: df.loc[df["Product"] == product].copy() for product in products
        }

        return df_split
