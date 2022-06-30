import pytest
import subprocess  # nosec

import triangles
import triangles.main as main


class TestTriangleAccumulatorInit:
    """Tests for the TriangleAccumulator.__init__ method."""

    def test_successful_call(self, tmp_path):
        """Show a successful initialisation of the TriangleAccumulator class."""

        output_path = str(tmp_path / "non_existing_file.txt")

        input_file = tmp_path / "existing_file.txt"
        input_file.write_text("....content")

        input_path = str(input_file)

        main.TriangleAccumulator(input_path, output_path)

    def test_attributes_set(set, tmp_path):
        """Test 4 attributes are set during initialisation."""

        output_path = str(tmp_path / "non_existing_file.txt")

        input_file = tmp_path / "existing_file.txt"
        input_file.write_text("....content")

        input_path = str(input_file)

        triangle_accumulator = main.TriangleAccumulator(input_path, output_path)

        assert (
            triangle_accumulator.input == input_path
        ), "input attribute not set correctly on TriangleAccumulator"

        assert (
            triangle_accumulator.output == output_path
        ), "output attribute not set correctly on TriangleAccumulator"

        assert triangle_accumulator.reader == triangles.read.Reader(
            input_path
        ), "reader attribute not set correctly on TriangleAccumulator"

        assert triangle_accumulator.writer == triangles.write.Writer(
            output_path
        ), "writer attribute not set correctly on TriangleAccumulator"


class TestTriangleAccumulatorProcess:
    """Tests for the TriangleAccumulator.process method."""

    def test_successful_call(self, tmp_path, example_file):
        """Show a successful call of the TriangleAccumulator.process method."""

        output_path = str(tmp_path / "non_existing_file.txt")

        triangle_accumulator = main.TriangleAccumulator(example_file, output_path)

        triangle_accumulator.process()

    @pytest.mark.parametrize(
        "input_file_fixture, output_file_fixture",
        [
            ("example_file", "example_output_file"),
            ("large_example_file", "large_example_output_file"),
        ],
    )
    def test_output(self, input_file_fixture, output_file_fixture, tmp_path, request):
        """Test that the end to end processing produces the correct output file."""

        input_file = request.getfixturevalue(input_file_fixture)
        expected_output_file = request.getfixturevalue(output_file_fixture)

        output_path = str(tmp_path / "non_existing_file.txt")

        triangle_accumulator = main.TriangleAccumulator(input_file, output_path)

        triangle_accumulator.process()

        with open(output_path) as f:
            actual_results = f.readlines()

        with open(expected_output_file) as f:
            expected_results = f.readlines()

        assert (
            expected_results == actual_results
        ), "output from TriangleAccumulator.process not correct"


class TestAccumulateIncrementalData:
    """Tests for the main.accumulate_incremental_data function."""

    def test_successful_call(self, tmp_path, example_file):
        """Show a successful call of the accumulate_incremental_data function."""

        output_path = str(tmp_path / "non_existing_file.txt")

        main.accumulate_incremental_data(example_file, output_path)

    def test_function_calls(self, mocker, tmp_path, example_file):
        """Test the calls to TriangleAccumulator class."""

        mocked_init = mocker.spy(triangles.main.TriangleAccumulator, "__init__")
        mocked_process = mocker.spy(triangles.main.TriangleAccumulator, "process")

        output_path = str(tmp_path / "non_existing_file.txt")

        main.accumulate_incremental_data(example_file, output_path)

        assert (
            mocked_init.call_count == 1
        ), "TriangleAccumulator.__init__ not called once"

        init_call_args = mocked_init.call_args_list[0]

        # not testing self argument
        assert init_call_args[0][1:] == (
            example_file,
            output_path,
        ), "positional args in TriangleAccumulator.__init__ call not correct"

        assert (
            init_call_args[1] == {}
        ), "keyword args in TriangleAccumulator.__init__ call not correct"

        assert (
            mocked_process.call_count == 1
        ), "TriangleAccumulator.process not called once"

        process_call_args = mocked_process.call_args_list[0]

        assert (
            process_call_args[0][1:] == ()
        ), "positional args in TriangleAccumulator.process call not correct"

        assert (
            process_call_args[1] == {}
        ), "keyword args in TriangleAccumulator.process call not correct"


class TestMain:
    """Tests for the main.main function."""

    def test_successful_call(self, example_file, tmp_path):
        """Show a successful call of the main function."""

        output_path = str(tmp_path / "non_existing_file.txt")

        # create command line args with '' as running in interpreter
        sys_argv_replacement = ["", example_file, output_path]

        main.main(sys_argv_replacement)

    def test_accumulate_incremental_data_call(self, example_file, tmp_path, mocker):
        """Test the call to the accumulate_incremental_data function."""

        mocked = mocker.patch("triangles.main.accumulate_incremental_data")

        output_path = str(tmp_path / "non_existing_file.txt")

        sys_argv_replacement = ["", example_file, output_path]

        main.main(sys_argv_replacement)

        assert (
            mocked.call_count == 1
        ), "main.accumulate_incremental_data not called once"

        call_args = mocked.call_args_list[0]

        assert call_args[0] == (
            example_file,
            output_path,
        ), "positional args in accumulate_incremental_data call not correct"

        assert (
            call_args[1] == {}
        ), "keyword args in accumulate_incremental_data call not correct"


class TestTriangles:
    """Tests for the triangles command line entry point for the main.main function."""

    def test_successful_call(self, example_file, tmp_path):
        """Show a successful call of the main function."""

        output_path = str(tmp_path / "non_existing_file.txt")

        commands = ["triangles", example_file, output_path]
        subprocess.run(commands, shell=False)  # nosec

    @pytest.mark.parametrize(
        "input_file_fixture, output_file_fixture",
        [
            ("example_file", "example_output_file"),
            ("large_example_file", "large_example_output_file"),
        ],
    )
    def test_output(self, input_file_fixture, output_file_fixture, tmp_path, request):
        """Test that the end to end processing produces the correct output file."""

        input_file = request.getfixturevalue(input_file_fixture)
        expected_output_file = request.getfixturevalue(output_file_fixture)

        output_path = str(tmp_path / "non_existing_file.txt")

        commands = ["triangles", input_file, output_path]
        subprocess.run(commands, shell=False)  # nosec

        with open(output_path) as f:
            actual_results = f.readlines()

        with open(expected_output_file) as f:
            expected_results = f.readlines()

        assert (
            expected_results == actual_results
        ), "output from triangles command (from command line) not correct"
