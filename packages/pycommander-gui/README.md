# Silicon Labs PyCommander (GUI version)

## Introduction

This Python package wraps Simplicity Commander functionality and exposes a native Python API for interacting with Commander in your scripts.

## Requirements

This package was developed using Python 3.10. Required PyPI packages are:

- pyyaml

Additionally, Simplicity Commander requires the SEGGER J-Link drivers to be installed on your system.

Note that this package only contains the GUI version of Simplicity Commander. The CLI version is available in the `silabs-pycommander-cli` package.

## Installation

```bash
pip install silabs-pycommander-gui
```

## Usage

More details about Simplicity Commander and its Command Line Interface can be found in the [official documentation for Simplicity Commander](https://docs.silabs.com/simplicity-commander/latest/simplicity-commander-start/). The documentation is also helpful when using the Python API, as the command names and available options are the same.

### Launching the GUI

The GUI can be launched using the `pycommander-gui` command from the terminal.

```bash
pycommander-gui
```

### Command Line Interface

From the command line, `pycommander-gui` is a razor-thin wrapper around the Simplicity Commander CLI; it behaves exactly like the Simplicity Commander CLI.

```bash
pycommander-gui --help
pycommander-gui --version
pycommander-gui <command> [<options>]
pycommander-gui <command> <subcommand> [<options>]
```

### Python API

At the lowest level, the `Commander` class provides all the CLI commands as methods to the class. These methods return a dictionary containing the command output, similarly to what the Simplicity Commander CLI does when the `--json` flag is used.

```python
from pycommander_gui import Commander

commander = Commander(serial_number="44055955")
print(commander.device.info(device="EFR32MG24"))
print(commander.util.appinfo(filename="firmware.hex"))
print(commander.flash.flash(filenames=["firmware.hex"], address=0x08000000))
```

pycommander-gui also exposes several convenience methods for common tasks related to the adapter (using the `Adapter` class) and the target device (using the `Target` class). These methods return different data types depending on the command. The types are available in the `pycommander_core.types` module.

- Locking/unlocking the device for debug access
- Setting the CTUNE value
- Setting the adapter's VCOM configuration
- Configuring the target device's voltage
- Flashing firmware to the device
- Erasing the device's flash
- Configuring code regions (Series 3 only)
- +++

```python
from pycommander_gui import Adapter, Target
from pycommander_core.types import AdapterInfo, AdapterVoltageInfo, VcomHandshake, CtuneValue

adapter = Adapter(serial_number="44055955", target_device="EFR32MG24")

adapter_info: AdapterInfo = adapter.info()
voltage_info: dict[int, AdapterVoltageInfo] = adapter.getVoltage()
adapter.setVcomConfig(115200, VcomHandshake.RTSCTS, True)

ctune_value: CtuneValue = adapter.target.getCTUNE()
adapter.target.setCTUNE(ctune_value.board)
```
