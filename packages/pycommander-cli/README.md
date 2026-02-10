# Silicon Labs PyCommander (CLI version)

## Introduction

This Python package wraps Simplicity Commander functionality and exposes a native Python API for interacting with Commander in your scripts.

## Requirements

This package was developed using Python 3.10. Required PyPI packages are:

- ...
- ...

Additionally, Simplicity Commander requires the SEGGER J-Link drivers to be installed on your system.

Note that this package only contains the CLI version of Simplicity Commander. The GUI version is available in the `silabs-pycommander-gui` package.

## Installation

```bash
pip install silabs-pycommander-cli
```

## Usage

More details about Simplicity Commander and its Command Line Interface can be found in the [official documentation for Simplicity Commander](https://docs.silabs.com/simplicity-commander/latest/simplicity-commander-start/). The documentation is also helpful when using the Python API, as the command names and available options are the same.

### Command Line Interface

From the command line, `pycommander` is a razor-thin wrapper around the Simplicity Commander CLI; it behaves exactly like the Simplicity Commander CLI.

```bash
pycommander --help
pycommander --version
pycommander <command> [<options>]
pycommander <command> <subcommand> [<options>]
```

### Python API

At the lowest level, the `PyCommander` class provides all the CLI commands as methods. These methods return a dictionary containing the command output, similarly to what the Simplicity Commander CLI does when the `--json` flag is used.

`PyCommander` also exposes several convenience methods for common tasks. These tasks include:

- herp
- derp
- chirp

```python
import pycommander_cli

```
