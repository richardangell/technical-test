# technical-test

Solution to WTW software engineering technical test.

## How to run

Clone the code;

`git clone https://github.com/richardangell/technical-test.git`

Create the python environment using [pipenv](https://pipenv.pypa.io/en/latest/) (you may need [pyenv](https://github.com/pyenv/pyenv) or [pyenv-win](https://github.com/pyenv-win/pyenv-win) if you don't have a suitable version of python installed);

`pipenv install`

Then package can be run from the command line;

`triangles tests/data/example.txt example_output.txt`

or from within a Python session;

```
import triangles
triangles.accumulate_incremental_data("tests/data/example.txt", "example_output.txt")
```

both these methods will load the example input file in the `tests/data` folder, accumulate the incremental data and write the output to the specified file.
