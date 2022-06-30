import pandas as pd
import pytest
from typing import Any

from triangles.read import Reader
from triangles.accumulate import AccumulatedData, Accumulator


EXAMPLE_FILE = "tests/data/example.txt"
EXAMPLE_OUTPUT_FiLE = "tests/data/example_output.txt"
LARGE_EXAMPLE_FILE = "tests/data/large_example.txt"
LARGE_EXAMPLE_OUTPUT_FiLE = "tests/data/large_example_output.txt"


@pytest.fixture
def load_example_file() -> pd.DataFrame:
    """Load example input file - not using read.Reader class."""

    return pd.read_csv(EXAMPLE_FILE)


@pytest.fixture
def load_large_example_file() -> pd.DataFrame:
    """Load the larger example file - not using read.Reader class."""

    return pd.read_csv(LARGE_EXAMPLE_FILE)


@pytest.fixture
def example_file() -> str:
    """Return the example file name."""

    return EXAMPLE_FILE


@pytest.fixture
def example_output_file() -> str:
    """Return the example output file name."""

    return EXAMPLE_OUTPUT_FiLE


@pytest.fixture
def large_example_file() -> str:
    """Return the large example file name."""

    return LARGE_EXAMPLE_FILE


@pytest.fixture
def large_example_output_file() -> str:
    """Return the large example output file name."""

    return LARGE_EXAMPLE_OUTPUT_FiLE


@pytest.fixture
def accumulate_example_file(example_file) -> AccumulatedData:
    """Load the example file and return it's accumulated data, using only
    methods from triangles."""

    reader = Reader(example_file)
    incremental_data = reader.read()

    accumulator = Accumulator(incremental_data)
    return accumulator.accumulate()


@pytest.fixture
def not_sorted_example_file(load_example_file, tmp_path) -> str:
    """Write a non-sorted version of the example file in a temporary directory
    and return the filename."""

    df_reordered = load_example_file.sample(frac=1, replace=False, random_state=1)

    file = tmp_path / "manipulated_example.txt"

    df_reordered.to_csv(file, index=False)

    return str(file)


@pytest.fixture
def extra_columns_example_file(load_example_file, tmp_path) -> str:
    """Write a version of the example file in a temporary directory with extra
    columns and return the filename."""

    df_extra = load_example_file.copy()
    df_extra["extra_1"] = 1
    df_extra["extra_2"] = 2

    file = tmp_path / "manipulated_example.txt"

    df_extra.to_csv(file, index=False)

    return str(file)


@pytest.fixture(
    params=["Product", "Origin Year", "Development Year", "Incremental Value"]
)
def missing_column_example_file(
    load_example_file, request, tmp_path
) -> tuple[str, Any]:
    """Write a version of the example file in a temporary directory with some
    columns missing and return the filename."""

    df_missing = load_example_file.copy()
    del df_missing[request.param]

    file = tmp_path / "manipulated_example.txt"

    df_missing.to_csv(file, index=False)

    return str(file), request.param
