import re
import pytest

import triangles
import triangles.write as write


class TestWriterInit:
    """Tests for the Writer.__init__ method."""

    def test_successful_call(self, tmp_path):
        """Show a successful initialisation of the Writer class."""

        output_path = str(tmp_path / "non_existing_file.txt")

        write.Writer(output_path)

    def test_exception_filename_not_str(self):
        """Test a TypeError is raised if filename is not a str."""

        with pytest.raises(
            TypeError,
            match="filename is not in expected types <class 'str'>, got <class 'bool'>",
        ):

            write.Writer(True)

    @pytest.mark.parametrize("extension", [".txt.gz.zip", ".gz.zip", "", ".txt.txt"])
    def test_exception_filename_not_one_extension(self, extension):
        """Test a ValueError is raised if filename does not have a single extension."""

        with pytest.raises(
            ValueError,
            match=re.escape("condition: [filename has one extension] not met"),
        ):

            write.Writer(f"file_wrong_extensions{extension}")

    @pytest.mark.parametrize("extension", [".zip", ".gz", ".aaa"])
    def test_exception_filename_not_txt_extension(self, extension):
        """Test a ValueError is raised if filename does not the .txt extension."""

        with pytest.raises(
            ValueError,
            match=re.escape("condition: [filename has .txt extension] not met"),
        ):

            write.Writer(f"file_wrong_extension{extension}")

    def test_exception_filename_does_exist(self, tmp_path):
        """Test a ValueError is raised if filename exists already."""

        existing_output_file = tmp_path / "existing_file.txt"
        existing_output_filename = str(existing_output_file)
        existing_output_file.write_text("....")

        with pytest.raises(
            ValueError,
            match=re.escape(
                f"condition: [{existing_output_filename} does not already exist] not met"
            ),
        ):

            write.Writer(str(existing_output_file))

    def test_filename_attribute_set(self, tmp_path):
        """Test the filename arg is set to an attribute with the same name."""

        temp_text_file = tmp_path / "hello.txt"

        temp_text_filename = str(temp_text_file)

        writer = write.Writer(temp_text_filename)

        assert (
            writer.filename == temp_text_filename
        ), "filename not set correctly when initialising Writer"


class TestWriterWrite:
    """Tests for the Writer.write method."""

    def test_successful_call(self, tmp_path, accumulate_example_file):
        """Show a successful call of the Write.write method."""

        output_path = str(tmp_path / "non_existing_file.txt")

        writer = write.Writer(output_path)

        writer.write(accumulate_example_file)

    def test_output_file_contents(self, tmp_path, mocker, accumulate_example_file):
        """Test that the output from the AccumulatedData.process_accumulated_data_to_output_format method is written to the file."""

        pre_set_return_value = ["a", "b", "c"]

        mocker.patch.object(
            triangles.accumulate.AccumulatedData,
            "process_accumulated_data_to_output_format",
            return_value=pre_set_return_value,
        )

        output_path = str(tmp_path / "non_existing_file.txt")

        writer = write.Writer(output_path)

        writer.write(accumulate_example_file)

        with open(output_path) as f:
            lines = f.readlines()

        # remove line breaks after reading file back in
        lines_cleaned = [line.replace("\n", "") for line in lines]

        assert (
            lines_cleaned == pre_set_return_value
        ), "output from AccumulatedData.process_accumulated_data_to_output_format not written to text file"
