# Silicon Labs PyCommander (GUI)

>The recommended way to install and use PyCommander is the [`silabs-pycommander` meta-package](../pycommander/README.md). That README is the guide for the `pycommander` command and the Python API. This page covers the GUI package only.

## Introduction

This package ships the Simplicity Commander GUI executable. It does not ship the CLI executable, and it does not in itself provide the Python API.

## Requirements

This package requires Python 3.10 or newer. Required PyPI packages are:

- silabs-pycommander-core
- platformdirs
- pyyaml

Additionally, Simplicity Commander requires the SEGGER J-Link drivers to be installed on your system.

## Installation

This package can be explicitly installed:

```bash
pip install "silabs-pycommander-gui"
```

## Usage

### Launching the GUI

This package does not install the `pycommander` command. `python -m pycommander_gui` runs the GUI executable. Arguments are forwarded to it:

```bash
python -m pycommander_gui <command> [options]
```

### Python API

Imports from `pycommander_gui`, including submodule imports such as `pycommander_gui.commander`, still resolve to the Python API in `silabs-pycommander-cli`. They emit a `DeprecationWarning` and will be removed in a future release. Install [`silabs-pycommander`](../pycommander/README.md) and import from `pycommander` instead. A GUI-only install does not include that API.
