"""Module bringing together reading, accumulation and writing tasks into one
class and providing command line entry point function to package."""

import argparse
import sys

from .accumulate import Accumulator
from .read import Reader
from .write import Writer


class TriangleAccumulator:
    """Class to read an input file, process it (i.e. accumulate the
    incremental payment data) and write the results to an output file.

    Parameters
    ----------
    input : str
        Filename including path and extenion of input file to process. Must be
        a text file.

    input : str
        Filename including path and extenion of file to save results to. Must be
        a text file.

    """

    def __init__(self, input: str, output: str) -> None:

        self.reader = Reader(input)
        self.writer = Writer(output)
        self.input = input
        self.output = output

    def process(self):
        """Method to read the input file, process and then write the results."""

        incremental_data = self.reader.read()

        self.accumulator = Accumulator(incremental_data)
        accumulated_data = self.accumulator.accumulate()

        self.writer.write(accumulated_data)


def accumulate_incremental_data(input: str, output: str):
    """Helper function to read an input file, process it (i.e. accumulate the
    incremental payment data) and write the results to an output file.

    Parameters
    ----------
    input : str
        Filename including path and extenion of input file to process. Must be
        a text file.

    input : str
        Filename including path and extenion of file to save results to. Must be
        a text file.

    """

    traingale_accumulator = TriangleAccumulator(input, output)

    traingale_accumulator.process()


def main(argv=sys.argv):
    """Command line entry point for the accumulate_incremental_data function.

    Command line options are input and output which should both be strings
    giving the input file to process and the output file to write to. Both the
    argumnets are positional arguments.

    Parameters
    ----------
    argv : sys.argv
        Command line arguments.

    """

    parser = argparse.ArgumentParser(description="Accumulate reserving payment data.")

    parser.add_argument(
        "input", type=str, help="input text file to read containing incremental data."
    )
    parser.add_argument(
        "output", type=str, help="output text file to save accumulated data to."
    )

    args = parser.parse_args(argv[1:])

    accumulate_incremental_data(args.input, args.output)
