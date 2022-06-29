import pandas as pd
import re
import pytest

import triangles.read as read


class TestReaderInit:
    """Tests for the Reader.__init__ method."""

    def test_successful_call(self, tmp_path):
        """Show a successful initialisation of the Reader class."""

        temp_text_file = tmp_path / "hello.txt"
        temp_text_file.write_text("....content")

        temp_text_filename = str(temp_text_file)

        read.Reader(temp_text_filename)

    def test_exception_filename_not_str(self):
        """Test a TypeError is raised if filename is not a str."""

        with pytest.raises(
            TypeError,
            match="filename is not in expected types <class 'str'>, got <class 'int'>",
        ):

            read.Reader(123)

    @pytest.mark.parametrize("extension", [".txt.gz.zip", ".gz.zip", "", ".txt.txt"])
    def test_exception_filename_not_one_extension(self, extension):
        """Test a ValueError is raised if filename does not have a single extension."""

        with pytest.raises(
            ValueError,
            match=re.escape("condition: [filename has one extension] not met"),
        ):

            read.Reader(f"file_wrong_extensions{extension}")

    @pytest.mark.parametrize("extension", [".zip", ".gz", ".aaa"])
    def test_exception_filename_not_txt_extension(self, extension):
        """Test a ValueError is raised if filename does not the .txt extension."""

        with pytest.raises(
            ValueError,
            match=re.escape("condition: [filename has .txt extension] not met"),
        ):

            read.Reader(f"file_wrong_extension{extension}")

    def test_exception_filename_does_not_exist(self):
        """Test a ValueError is raised if filename does not exist."""

        with pytest.raises(
            ValueError,
            match=re.escape("condition: [does_not_exist.txt exists] not met"),
        ):

            read.Reader("does_not_exist.txt")

    def test_filename_attribute_set(self, tmp_path):
        """Test the filename arg is set to an attribute with the same name."""

        temp_text_file = tmp_path / "hello.txt"
        temp_text_file.write_text("....content")

        temp_text_filename = str(temp_text_file)

        reader = read.Reader(temp_text_filename)

        assert (
            reader.filename == temp_text_filename
        ), "filename not set correctly when initialising Reader"


class TestReaderRead:
    """Tests for the Reader.read method."""

    def test_successful_call(self):
        """Test a successful call to read."""

        reader = read.Reader("tests/data/example.txt")

        reader.read()

    def test_dataframe_returned(self):
        """Test a pd.DataFrame is returned from the method."""

        reader = read.Reader("tests/data/example.txt")

        incremental_data = reader.read()

        assert (
            type(incremental_data) is pd.DataFrame
        ), "incorrect type returned from Reader.read"

    def test_output_sorted(self, not_sorted_example_file):
        """Test that the output from the method is sorted by product, origin
        year and development year."""

        non_sorted_original = pd.read_csv(not_sorted_example_file)
        non_sorted_now_sorted = non_sorted_original.sort_values(
            by=["Product", "Origin Year", "Development Year"]
        )

        reader = read.Reader(not_sorted_example_file)
        incremental_data = reader.read()

        pd.testing.assert_frame_equal(non_sorted_now_sorted, incremental_data)

    @pytest.mark.parametrize(
        "filename",
        ["example_file", "not_sorted_example_file", "extra_columns_example_file"],
    )
    def test_correct_columns_in_output(self, request, filename):
        """Test that the only columns in the output are product, origin year,
        development year and incremental value."""

        # requesting fixture value
        reader = read.Reader(request.getfixturevalue(filename))
        incremental_data = reader.read()

        assert incremental_data.shape[1] == 4, "output data does not have 4 columns"

        for column in [
            "Product",
            "Origin Year",
            "Development Year",
            "Incremental Value",
        ]:

            assert column in incremental_data.columns, f"{column} column not in output"

    def test_exception_raised_missing_columns(
        self, missing_column_example_file, request
    ):
        """Test that a ValueError is raised if one of the 4 required columns is
        missing.

        Note, this exception comes from pandas.read_csv usecols argument.
        """

        filename, missing_column = missing_column_example_file

        reader = read.Reader(filename)

        with pytest.raises(
            ValueError,
            match=re.escape(
                f"Usecols do not match columns, columns expected but not found: ['{missing_column}']"
            ),
        ):

            reader.read()
