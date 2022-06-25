"""Module containing class to deal with reading input files."""

import pandas as pd
from pathlib import Path
from pandas.api.types import is_object_dtype
from pandas.api.types import is_integer_dtype
from pandas.api.types import is_numeric_dtype

from .checks import check_condition, check_type


class Reader:
    """Class to read comma separated text file containing .

    Parameters
    ----------
    filename: str
        Filename including path and extension of text file to read.

    """

    INCREMENTAL_DATA_COLUMNS = [
        "Product",
        "Origin Year",
        "Development Year",
        "Incremental Value",
    ]

    def __init__(self, filename: str) -> None:

        check_type(filename, str, "filename")

        file = Path(filename)
        file_extension = file.suffixes

        check_condition(len(file_extension) == 1, "filename has one extension")
        check_condition(file_extension[0] == ".txt", "filename has .txt extension")
        check_condition(file.exists(), f"{filename} exists")

        self.filename = filename

    def read(self) -> dict[str, pd.DataFrame]:
        """Read text file and return a dictionary of DataFrames where each
        DataFrame is the input data subset to a specific product."""

        incremental_data = pd.read_csv(
            self.filename, usecols=self.INCREMENTAL_DATA_COLUMNS
        )

        self._check_read_file(incremental_data)

        incremental_data_sorted = self._sort_incremental_data(incremental_data)
        incremental_data_split = self._split_incremental_data(incremental_data_sorted)

        return incremental_data_split

    def _sort_incremental_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Method to sort incremental data by origin year and then development
        year, in ascending order.
        """

        return df.sort_values(
            by=[self.INCREMENTAL_DATA_COLUMNS[1], self.INCREMENTAL_DATA_COLUMNS[2]],
            ascending=True,
        )

    def _check_read_file(self, df: pd.DataFrame):
        """Method to do checks on incemental data"""

        check_condition(df.shape[0] > 0, "incremental data has rows")

        check_condition(
            is_object_dtype(df[self.INCREMENTAL_DATA_COLUMNS[0]]),
            f"{self.INCREMENTAL_DATA_COLUMNS[0]} column is object type",
        )
        check_condition(
            is_integer_dtype(df[self.INCREMENTAL_DATA_COLUMNS[1]]),
            f"{self.INCREMENTAL_DATA_COLUMNS[1]} column is integer type",
        )
        check_condition(
            is_integer_dtype(df[self.INCREMENTAL_DATA_COLUMNS[2]]),
            f"{self.INCREMENTAL_DATA_COLUMNS[2]} column is integer type",
        )
        check_condition(
            is_numeric_dtype(df[self.INCREMENTAL_DATA_COLUMNS[3]]),
            f"{self.INCREMENTAL_DATA_COLUMNS[3]} column is numeric type",
        )

    def _split_incremental_data(self, df: pd.DataFrame) -> dict[str, pd.DataFrame]:
        """Method to split incremental data by product."""

        products = df["Product"].unique().tolist()

        df_split = {
            product: df.loc[df["Product"] == product].copy() for product in products
        }

        return df_split
