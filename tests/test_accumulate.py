import pandas as pd
import pytest

import triangles.accumulate as accumulate


@pytest.fixture
def accumulated_data():
    """Return AccumulatedData object with some limited data."""

    return accumulate.AccumulatedData(1990, 2, {"x": [0, 100.5, 200, 3000]})


class TestAccumulatedDataInit:
    """Tests for the AccumulatedData.__init__ method."""

    def test_successful_call(self):
        """Show a successful initialisation of the AccumulatedData class."""

        accumulate.AccumulatedData(1990, 2, {"x": [0, 100.5, 200, 3000]})

    @pytest.mark.parametrize(
        "min_origin_year, n_development_years, accumulated_data",
        [(1990, 5, {"x": [0, 100.5, 200, 3000]})],
    )
    def test_attributes_set(
        self, min_origin_year, n_development_years, accumulated_data
    ):
        """Test input arguments are set as attributes."""

        accumulated = accumulate.AccumulatedData(
            min_origin_year, n_development_years, accumulated_data
        )

        assert (
            accumulated.min_origin_year == min_origin_year
        ), "min_origin_year not set on AccumulatedData"

        assert (
            accumulated.n_development_years == n_development_years
        ), "n_development_years not set on AccumulatedData"

        assert (
            accumulated.accumulated_data == accumulated_data
        ), "accumulated_data not set on AccumulatedData"


class TestAccumulatedDataConvertAccumulatedListToStr:
    """Tests for the AccumulatedData._convert_accumulated_list_to_str method."""

    def test_successful_call(self, accumulated_data):
        """Show a successful call of the AccumulatedData._convert_accumulated_list_to_str method."""

        accumulated_data._convert_accumulated_list_to_str("x", [0, 100.5, 200, 3000])

    @pytest.mark.parametrize(
        "product, accumulated_list, expected_output",
        [
            ("x", [0, 50, 100], "x,0,50,100"),
            ("prod", [-494.2], "prod,-494.2"),
            ("abc", [], "abc,"),
            ("123", [0.0, 50.11, 10000000], "123,0.0,50.11,10000000"),
        ],
    )
    def test_output(self, product, accumulated_list, accumulated_data, expected_output):
        """Test output of the function is as expected."""

        result = accumulated_data._convert_accumulated_list_to_str(
            product, accumulated_list
        )

        assert (
            result == expected_output
        ), "output from _convert_accumulated_list_to_str method not correct"


class TestAccumulatedDataProcessAccumulatedDataToOutputFormat:
    """Tests for the AccumulatedData.process_accumulated_data_to_output_format method."""

    def test_successful_call(self, accumulated_data):
        """Show a successful call of the AccumulatedData.process_accumulated_data_to_output_format method."""

        accumulated_data.process_accumulated_data_to_output_format()

    @pytest.mark.parametrize(
        "min_origin_year, n_development_years, accumulated_data, expected_output",
        [
            (2010, 3, {"x": [0.0, 4, 5]}, ["2010,3", "x,0.0,4,5"]),
            (
                2015,
                1,
                {"a": [0.0, 4.2221, 500], "b": [200]},
                ["2015,1", "a,0.0,4.2221,500", "b,200"],
            ),
            (
                1,
                20,
                {
                    "z": [-4, 0, 1.5, 200000, 5000000],
                    "b4": [200, 400, 600, 800, 1000, 1111.1],
                },
                ["1,20", "z,-4,0,1.5,200000,5000000", "b4,200,400,600,800,1000,1111.1"],
            ),
        ],
    )
    def test_output(
        self, min_origin_year, n_development_years, accumulated_data, expected_output
    ):
        """Test the ouptut from process_accumulated_data_to_output_format is correct."""

        accumulated_data = accumulate.AccumulatedData(
            min_origin_year, n_development_years, accumulated_data
        )

        result = accumulated_data.process_accumulated_data_to_output_format()

        assert (
            result == expected_output
        ), "output from process_accumulated_data_to_output_format method not correct"


class TestAccumulatorInit:
    """Tests for the Accumulator.__init__ method."""

    def test_successful_call(self, load_example_file):
        """Show a successful initialisation of the Accumulator class."""

        accumulate.Accumulator(load_example_file)

    def test_exception_incremental_data_not_dataframe(self):
        """Test a TypeError is raised if incremental_data is not a DataFrame."""

        with pytest.raises(
            TypeError,
            match="incremental_data is not in expected types <class 'pandas.core.frame.DataFrame'>, got <class 'float'>",
        ):

            accumulate.Accumulator(123.321)

    @pytest.mark.parametrize(
        "input_data_fixture", ["load_example_file", "load_large_example_file"]
    )
    def test_attributes_set(self, input_data_fixture, request):
        """Test 5 attributes are set correctly during __init__."""

        input_data = request.getfixturevalue(input_data_fixture)

        accumulator = accumulate.Accumulator(input_data)

        pd.testing.assert_frame_equal(input_data, accumulator.incremental_data)

        assert accumulator.min_origin_year == input_data["Origin Year"].min()
        assert accumulator.max_development_year == input_data["Development Year"].max()


class TestAccumulatorAccumulate:
    """Tests for the Accumulator.accumulate method."""

    def test_successful_call(self, load_example_file):
        """Show a successful call of the Accumulator.accumulate method."""

        accumulator = accumulate.Accumulator(load_example_file)

        accumulator.accumulate()

    @pytest.mark.skip(reason="not implemented")
    def test_return_type(self):
        """Test that an object of type AccumulatedData is returned from accumulate."""

        pass

    @pytest.mark.skip(reason="not implemented")
    def test_returned_data_correct(self):
        """Test that the data in the return AccumulatedData object is as expected."""

        pass


class TestAccumulatorGetNDevelopmentYears:
    """Tests for the Accumulator._get_n_development_years method."""

    @pytest.mark.skip(reason="not implemented")
    def test_successful_call(self):
        """Show a successful call of the Accumulator._get_n_development_years method."""

        pass

    @pytest.mark.skip(reason="not implemented")
    def test_calculation(self):
        """Test _get_n_development_years calculates the correct value."""

        pass


class TestAccumulatorAccumulateProducts:
    """Tests for the Accumulator._accumulate_products method."""

    @pytest.mark.skip(reason="not implemented")
    def test_successful_call(self):
        """Show a successful call of the Accumulator._accumulate_products method."""

        pass

    @pytest.mark.skip(reason="not implemented")
    def test_function_calls(self):
        """Test calls to _split_incremental_data and _accumulate_product methods."""

        pass


class TestAccumulatorAccumulateProduct:
    """Tests for the Accumulator._accumulate_product method."""

    @pytest.mark.skip(reason="not implemented")
    def test_successful_call(self):
        """Show a successful call of the Accumulator._accumulate_product method."""

        pass

    @pytest.mark.skip(reason="not implemented")
    def test_calculation(self):
        """Test _accumulate_product calculates accumulated values correctly."""

        pass


class TestAccumulatorSplitIncrementalData:
    """Tests for the Accumulator._split_incremental_data method."""

    @pytest.mark.skip(reason="not implemented")
    def test_successful_call(self):
        """Show a successful call of the Accumulator._split_incremental_data method."""

        pass

    @pytest.mark.skip(reason="not implemented")
    def test_output(self):
        """Test _split_incremental_data returns the correct DataFrame splits."""

        pass
