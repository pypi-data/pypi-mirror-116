# sqlite-explain

[![PyPI](https://img.shields.io/pypi/v/sqlite-explain.svg)](https://pypi.org/project/sqlite-explain/)
[![Changelog](https://img.shields.io/github/v/release/simonw/sqlite-explain?include_prereleases&label=changelog)](https://github.com/simonw/sqlite-explain/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/sqlite-explain/blob/main/LICENSE)

Derive information about a SQLite query using EXPLAIN

## Installation

Install this library using `pip`:

    $ pip install sqlite-explain

## Usage

This library is an early alpha, do not use it yet!

## Development

To contribute to this library, first checkout the code. Then create a new virtual environment:

    cd sqlite-explain
    python -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
