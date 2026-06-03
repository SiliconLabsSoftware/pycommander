# pycommander

[![Unit tests](https://github.com/SiliconLabsSoftware/pycommander/actions/workflows/unittest-and-coverage.yml/badge.svg)](https://github.com/SiliconLabsSoftware/pycommander/actions/workflows/unittest-and-coverage.yml)

## Introduction

This repository contains the source code for Silicon Labs PyCommander, which wraps Simplicity Commander into a pip-installable Python package. PyCommander gives you both a drop-in `pycommander` CLI and a native Python API for using Simplicity Commander in your automation scripts.

## Available packages

- [`silabs-pycommander-core`](packages/pycommander-core/README.md): The package that contains the core functionality, i.e. the Python framework for interacting with Simplicity Commander.
- [`silabs-pycommander-cli`](packages/pycommander-cli/README.md): The package that contains the CLI version of Simplicity Commander. This package depends on `pycommander-core`.
- [`silabs-pycommander-gui`](packages/pycommander-gui/README.md): The package that contains the GUI version of Simplicity Commander. This package depends on `pycommander-core`. It is currently not advertised, but it can be installed if needed. In that case, it should be installed instead of the CLI version, unless you want two versions of Simplicity Commander installed on your system.
- [`silabs-pycommander`](packages/pycommander/README.md): Meta-package for clean UX when installing either the CLI or GUI version of Simplicity Commander. This is the package that should be installed by end users.

## Requirements

- Python 3.10 or newer.
- The SEGGER J-Link drivers must be installed on your system (Simplicity Commander uses them to communicate with the adapter).

## Installation

To install `pycommander` on your system, you can use the following command:

```bash
pip install silabs-pycommander
```

By default this pulls in the CLI flavor of Simplicity Commander. To also install the GUI flavor, use the `gui` extra:

```bash
pip install silabs-pycommander[gui]
```

## Usage

The `pycommander` command is a drop-in replacement for the Simplicity Commander CLI:

```bash
pycommander --version
pycommander device info --device EFR32MG24 --serialno 44055955
```

The Python API mirrors the CLI surface and adds higher-level helpers for common automation tasks:

```python
from pathlib import Path
from pycommander import Adapter

adapter = Adapter(serial_number="44055955", target_device="EFR32MG24")
print(adapter.info())
adapter.target.flashApplication(filenames=[Path("firmware.hex")])
```

See the per-package READMEs linked above for the full quick-start, including error handling, logging, streaming AEM measurements, and the low-level `Commander` class. More details about Simplicity Commander and its Command Line Interface can be found in the [official documentation for Simplicity Commander](https://docs.silabs.com/simplicity-commander/latest/simplicity-commander-start/). The documentation is also helpful when using the Python API, as the command names and available options are the same.
