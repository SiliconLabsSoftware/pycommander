# Silicon Labs PyCommander (CLI)

>The recommended way to install and use PyCommander is the [`silabs-pycommander` meta-package](../pycommander/README.md). That README is the guide for the `pycommander` command and the Python API. This page covers the CLI package only.

## Introduction

This package ships the Simplicity Commander CLI executable and the Python API. It does not ship the GUI executable.

## Requirements

This package requires Python 3.10 or newer. Required PyPI packages are:

- silabs-pycommander-core
- platformdirs
- pyyaml

Additionally, Simplicity Commander requires the SEGGER J-Link drivers to be installed on your system.

## Installation

This package can be explicitly installed:

```bash
pip install "silabs-pycommander-cli"
```

## Usage

For the `pycommander` command and the full Python API guide, use the [silabs-pycommander README](../pycommander/README.md).

More details about Simplicity Commander and its Command Line Interface can be found in the [official documentation for Simplicity Commander](https://docs.silabs.com/simplicity-commander/latest/simplicity-commander-start/). The documentation is also helpful when using the Python API, as the command names and available options are the same.

### Command Line Interface

This package does not install the `pycommander` command. `python -m pycommander_cli` runs the CLI executable, including when the GUI package is also installed. Arguments are forwarded to that executable:

```bash
python -m pycommander_cli --help
python -m pycommander_cli --version
python -m pycommander_cli <command> [options]
python -m pycommander_cli <command> <subcommand> [options]
```

### Python API

This package provides the Python API. The guide, with examples that import from `pycommander`, is in the [silabs-pycommander README](../pycommander/README.md). To use this package explicitly, replace those imports with `pycommander_cli`.
