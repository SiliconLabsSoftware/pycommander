# pycommander

[![Unit tests](https://github.com/SiliconLabsSoftware/pycommander/actions/workflows/unittest-and-coverage.yml/badge.svg)](https://github.com/SiliconLabsSoftware/pycommander/actions/workflows/unittest-and-coverage.yml)

## Introduction

This repository contains the source code for Silicon Labs PyCommander.

## Available packages

- `silabs-pycommander-core`: The package that contains the core functionality, i.e. the Python framework for interacting with Simplicity Commander.
- `silabs-pycommander-cli`: The package that contains the CLI version of Simplicity Commander. This package depends on `pycommander-core`.
- `silabs-pycommander-gui`: The package that contains the GUI version of Simplicity Commander. This package depends on `pycommander-core`.
- `silabs-pycommander`: Meta-package for clean UX when installing either the CLI or GUI version of Simplicity Commander. This is the package that should be installed by end users.

## Installation

To install `pycommander` on your system, you can use the following command:

```bash
pip install silabs-pycommander[cli]
pip install silabs-pycommander[gui]
```

Please note that the CLI and GUI versions of Simplicity Commander are mutually exclusive. You can only install one or the other. Also, you have to specify which version you want to install by using the `[cli]` or `[gui]` extra.

## Usage

More details about Simplicity Commander and its Command Line Interface can be found in the [official documentation for Simplicity Commander](https://docs.silabs.com/simplicity-commander/latest/simplicity-commander-start/). The documentation is also helpful when using the Python API, as the command names and available options are the same.
