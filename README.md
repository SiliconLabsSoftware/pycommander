# pycommander

[![Unit tests](https://github.com/SiliconLabsSoftware/pycommander/actions/workflows/unittest-and-coverage.yml/badge.svg)](https://github.com/SiliconLabsSoftware/pycommander/actions/workflows/unittest-and-coverage.yml)

## Introduction

This repository contains the source code for Silicon Labs PyCommander.

## Available packages

- `silabs-pycommander-core`: The package that contains the core functionality, i.e. the Python framework for interacting with Simplicity Commander.
- `silabs-pycommander-cli`: The package that contains the CLI version of Simplicity Commander. This package depends on `pycommander-core`.
- `silabs-pycommander-gui`: The package that contains the GUI version of Simplicity Commander. This package depends on `pycommander-core`. It is currently not advertised, but it can be installed if needed. In that case, it should be installed instead of the CLI version, unless you want two versions of Simplicity Commander installed on your system.
- `silabs-pycommander`: Meta-package for clean UX when installing either the CLI or GUI version of Simplicity Commander. This is the package that should be installed by end users.

## Installation

To install `pycommander` on your system, you can use the following command:

```bash
pip install silabs-pycommander
```

## Usage

More details about Simplicity Commander and its Command Line Interface can be found in the [official documentation for Simplicity Commander](https://docs.silabs.com/simplicity-commander/latest/simplicity-commander-start/). The documentation is also helpful when using the Python API, as the command names and available options are the same.
