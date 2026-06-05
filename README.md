# pycommander

[![Unit tests](https://github.com/SiliconLabsSoftware/pycommander/actions/workflows/unittest-and-coverage.yml/badge.svg)](https://github.com/SiliconLabsSoftware/pycommander/actions/workflows/unittest-and-coverage.yml)

## Introduction

This repository contains the source code for Silicon Labs PyCommander, which wraps Simplicity Commander into a pip-installable Python package. PyCommander gives you both a drop-in `pycommander` CLI and a native Python API for using Simplicity Commander in your automation scripts.

PyCommander can be used to interact with both Silicon Labs adapters (including the Wireless Starter Kit (WSTK), Wireless Pro Kit(WPK), and the Simplicity Link Debugger) as well as with generic J-Link adapters and probes. Using Silicon Labs adapters does however allow you to use a number of additional conveniences and tools, as will be described below.

## Available packages

- [`silabs-pycommander`](packages/pycommander/README.md): Meta-package for clean UX when installing either the CLI or GUI version of Simplicity Commander. This is the package that should be installed by end users!
- [`silabs-pycommander-cli`](packages/pycommander-cli/README.md): The package that contains the CLI version of Simplicity Commander. This package depends on `pycommander-core`.
- [`silabs-pycommander-gui`](packages/pycommander-gui/README.md): The package that contains the GUI version of Simplicity Commander. This package depends on `pycommander-core`. It is currently not advertised, but it can be installed if needed. In that case, it should be installed instead of the CLI version, unless you want two versions of Simplicity Commander installed on your system.
- [`silabs-pycommander-core`](packages/pycommander-core/README.md): The package that contains the core functionality, i.e. the Python framework for interacting with Simplicity Commander. Not functional on its own, please install one of the other packages instead.

## Requirements

- Python 3.10 or newer.
- The SEGGER J-Link drivers must be installed on your system (Simplicity Commander uses them to communicate with the adapter).

## Installation

To install `pycommander` on your system, you can use the following command:

```bash
pip install silabs-pycommander
```

By default this pulls in the CLI flavor of Simplicity Commander.

To install the GUI version of Simplicity Commander, use the `gui` extra:

```bash
pip install silabs-pycommander[gui]
```

This will install the GUI version of Simplicity Commander _in addition to_ the CLI version.

Both the CLI and GUI versions can coexist peacefully on the same system, but do note that when importing the `pycommander` package or when running the `pycommander` command from the terminal, the GUI version will be used over the CLI version. The flavor to use can be explicitly selected by importing the appropriate package, e.g. `import pycommander_cli` or `import pycommander_gui`, or by using the `pycommander-cli` or `pycommander-gui` commands from the terminal.

Installing PyCommander does not interfere with any existing installations of Simplicity Commander on your system, but do note that the different Commander instances will all share the same configuration file, i.e. the `commander.ini` file. For example, if command logging is enabled using one Commander instance, it will also be enabled for all the other Commander instances.

## Usage

The `pycommander` command is a drop-in replacement for the Simplicity Commander CLI. It can be used to perform all the same commands as the CLI, and the output is the same:

```bash
pycommander --version
pycommander device info --device EFR32MG24 --serialno 440055955
pycommander flash firmware.hex --device EFR32FG28 --serialno 440055956
```

The Python API adds three distinct abstraction layers:

- The `Commander` class, which simply mirrors the underlying Simplicity Commander CLI surface. The available methods take the same arguments as the underlying CLI commands, and return a dictionary containing the command output, similarly to what the Simplicity Commander CLI does when the `--json` flag is used.

  ```python
  from pathlib import Path
  from pycommander import Commander

  commander = Commander(serial_number="440055955")

  commander.device.info(target_device="EFR32MG24")
  commander.flash.flash(filenames=[Path("firmware.hex")])
  ```

- The `Adapter` class, which provides a higher-level API featuring convenience methods for common tasks for interfacing with _Silicon Labs adapters_. This includes setting up the adapter's VCOM configuration, configuring the target device's supply voltage, and more. An `Adapter` instance may have a `Target` instance (described below) associated with it, to represent a physical Silicon Labs kit (adapter with a target device (radio board) connected to it).

  ```python
  from pycommander import Adapter

  adapter = Adapter(serial_number="440055955")
  print(adapter.info())

  adapter.setVoltage(voltage=1.8)

  adapter.setVcomConfig(baudrate=115200, handshake=VcomHandshake.RTSCTS)

  result = adapter.analyzeEnergyUsage(duration_s=10, cluster_states=True, detect_period=True)
  print(result.clustering.unique_states)
  print(result.signal_characteristics.min_current_ma)
  print(result.signal_characteristics.max_current_ma)
  ```

- The `Target` class, which provides a higher-level API featuring convenience methods for common tasks for interfacing with the target device. This includes flashing firmware, erasing the device's flash, provisioning keys, configuring security, and more.

  ```python
  from pathlib import Path
  from pycommander import Commander, Target

  commander = Commander(serial_number="440055955")
  target = Target(part_number="EFR32MG24", commander=commander)
  print(target.info())

  target.setCTUNE(value=0xa8)

  target.flashApplication(filenames=[Path("firmware.hex")], masserase=True, verify=True)

  target.enableWriteProtection(ranges=[(0x00000000, 0x00008000), (0x0000A000, 0x0000C000)])
  ```

See the per-package READMEs linked above for the full quick-start, including error handling, logging, streaming AEM measurements, and the low-level `Commander` class. More details about Simplicity Commander and its underlying Command Line Interface can be found in the [official documentation for Simplicity Commander](https://docs.silabs.com/simplicity-commander/latest/simplicity-commander-start/). That documentation is also helpful when using the Python API, as the command names and available options mostly match the CLI commands.
