# Silicon Labs PyCommander

[![Unit tests](https://github.com/SiliconLabsSoftware/pycommander/actions/workflows/unittest.yml/badge.svg)](https://github.com/SiliconLabsSoftware/pycommander/actions/workflows/unittest.yml)

## Introduction

This Python package wraps Simplicity Commander functionality and exposes a native Python API for interacting with Commander in your scripts.

## Requirements

This package was developed using Python 3.10. Required PyPI packages are:

- ...
- ...

Additionally, Simplicity Commander requires the SEGGER J-Link drivers to be installed on your system.

## Installation

```bash
pip install silabs-pycommander
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

At the lowest level, the `PyCommander` class provides all the CLI commands as methods to the `Commander` class. These methods return a dictionary containing the command output, similarly to what the Simplicity Commander CLI does when the `--json` flag is used.

```python
from pycommander import Commander

commander = Commander(serial_number="44055955")
print(commander.device.info(device="EFR32MG24"))
print(commander.util.appinfo(filename="firmware.hex"))
print(commander.flash.flash(filenames=["firmware.hex"], address=0x08000000))
```

`PyCommander` also exposes several convenience methods for common tasks related to the adapter (using the `Adapter` class) and the target device (using the `Target` class). These methods return different data types depending on the command. The types are available in the `pycommander_core.types` module.

- Locking/unlocking the device for debug access
- Setting the CTUNE value
- Setting the adapter's VCOM configuration
- Configuring the target device's voltage
- Flashing firmware to the device
- Erasing the device's flash
- Configuring code regions (Series 3 only)
- +++

```python
from pycommander import Adapter, Target
from pycommander_core.types import AdapterInfo, AdapterVoltageInfo, VcomHandshake, CtuneValue

adapter = Adapter(serial_number="44055955", target_device="EFR32MG24")

adapter_info: AdapterInfo = adapter.info()
voltage_info: dict[int, AdapterVoltageInfo] = adapter.getVoltage()
adapter.setVcomConfig(115200, VcomHandshake.RTSCTS, True)

ctune_value: CtuneValue = adapter.target.getCTUNE()
adapter.target.setCTUNE(ctune_value.board)
```
