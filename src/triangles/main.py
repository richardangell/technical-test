"""Module bringing together reading, accumulation and writing tasks into one
class and providing command line entry point function to package."""

import argparse
import sys

from .accumulate import Accumulator
from .read import Reader
from .write import Writer


class TriangleAccumulator:
    def __init__(self, input: str, output: str) -> None:

        self.reader = Reader(input)
        self.writer = Writer(output)
        self.input = input
        self.output = output

    def process(self):

        incremental_data = self.reader.read()

        self.accumulator = Accumulator("na", incremental_data)
        accumulated_data = self.accumulator.accumulate()

        self.writer.write(accumulated_data)


def accumulate_incremental_data(input: str, output: str):

    traingale_accumulator = TriangleAccumulator(input, output)

    traingale_accumulator.process()


def main(argv=sys.argv):

    parser = argparse.ArgumentParser(description="Accumulate reserving payment data.")

    parser.add_argument(
        "input", type=str, help="input text file to read containing incremental data."
    )
    parser.add_argument(
        "output", type=str, help="output text file to save accumulated data to."
    )

    args = parser.parse_args(argv[1:])

    accumulate_incremental_data(args.input, args.output)
