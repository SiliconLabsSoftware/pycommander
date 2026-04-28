# Silicon Labs PyCommander

[![Unit tests](https://github.com/SiliconLabsSoftware/pycommander/actions/workflows/unittest.yml/badge.svg)](https://github.com/SiliconLabsSoftware/pycommander/actions/workflows/unittest.yml)

## Introduction

This Python package wraps Simplicity Commander functionality and exposes a native Python API for interacting with Commander in your scripts.

## Requirements

This package was developed using Python 3.10. Required PyPI packages are:

- platformdirs
- pyyaml

Additionally, Simplicity Commander requires the SEGGER J-Link drivers to be installed on your system.

## Installation

```bash
pip install silabs-pycommander
```

## Usage

More details about Simplicity Commander and its Command Line Interface can be found in the [official documentation for Simplicity Commander](https://docs.silabs.com/simplicity-commander/latest/simplicity-commander-start/). The documentation is also helpful when using the Python API, as the command names and available options are the same.

### Command Line Interface

From the command line, `pycommander` is a razor-thin wrapper around the Simplicity Commander CLI; it behaves exactly like the Simplicity Commander CLI, except for the case when the options `-v` or `--version` are passed as arguments, in which case the version of the `pycommander` package is printed in addition to the normal version information from the Simplicity Commander CLI.

```bash
pycommander --help
pycommander --version
pycommander <command> [options]
pycommander <command> <subcommand> [options]
```

### Python API

At the lowest level, the `Commander` class provides all the CLI commands as methods to the class. These methods return a dictionary containing the command output, similarly to what the Simplicity Commander CLI does when the `--json` flag is used.

```python
from pycommander import Commander

# Instantiate the Commander class with a serial number
commander = Commander(serial_number="44055955")

# Perform the 'commander device info' command
print(commander.device.info(target_device="EFR32MG24"))

# Perform the 'commander util appinfo' command
print(commander.util.appinfo(filename="firmware.hex"))

# Perform the 'commander flash' command
print(commander.flash.flash(filenames=["firmware.hex"], address=0x08000000))
```

Please note that not all commands are available to the `Commander` class. These are typically commands that are intended for interative CLI sessions, and include command suites like `vcom`, `vuart`, `rtt` and `swo`. Moreover, some commands in the `Commander` class have stricter requirements for the arguments than their CLI counterparts, for the same reasons as mentioned above. For example, the `aem dump` command requires the `outfile` and `duration` arguments to be provided. For a more flexible approach to streaming AEM data, please see the `AemStream` class below.

#### The `Adapter` and `Target` classes

pycommander exposes several convenience methods for common tasks related to the adapter and the target device. These methods return different data types depending on the command. The types are available in the `pycommander_core.types` module, and the tasks include:

- Locking/unlocking the device for debug access
- Setting the CTUNE value
- Setting the adapter's VCOM configuration
- Configuring the target device's voltage
- Flashing firmware to the device
- Erasing the device's flash
- Configuring code regions (Series 3 only)
- +++

When instantiating the `Adapter` class, a `Commander` class instance is created and made available as an attribute of the `Adapter` class. If a `target_device` is provided to the `Adapter` class, a `Target` class instance is created and made available as an attribute of the `Adapter` class as well.

An `Adapter` class instance (with a potential `Target` class instance) should be used to represent a connection to a single adapter (with target device). Multiple `Adapter` class instances can be used to represent connections to multiple adapters (with or without their respective target devices).

```python
from pycommander import Adapter, Target
from pycommander_core.types import AdapterInfo, AdapterVoltageInfo, VcomHandshake, CtuneValue

# Instantiate the Adapter class with a serial number and target device
adapter = Adapter(serial_number="44055955", target_device="EFR32MG24")

# Get the adapter information
adapter_info: AdapterInfo = adapter.info()

# Get the voltage information
voltage_info: AdapterVoltageInfo | None = adapter.getVoltage()

# Set the VCOM configuration of the adapter
adapter.setVcomConfig(115200, VcomHandshake.RTSCTS, True)

# Get the CTUNE value of the target device
ctune_value: CtuneValue = adapter.target.getCTUNE()

# Set the CTUNE value of the target device
adapter.target.setCTUNE(ctune_value.board)
```

#### The `AemStream` class

The `AemStream` class provides a pythonic way of streaming AEM measurements from the device. The measurements are returned as `AemMeasurement` objects, which contain the timestamp, current, voltage, and the calculated power. An `AemStream` object is suitable for streaming AEM measurements from an adapter, and there is no limitation to the duration of the streaming. The stream may be stopped at any time.

Like the underlying Simplicity Commander CLI, the `AemStream` class supports a variety of options for configuring the AEM data capture process, like setting up simple triggers to start the data capture process and specifying the data output rate.

##### Context Manager Syntax

If using the context manager syntax, the `AemStream` object is opened automatically when the context manager is entered, and a connection to the adapter is established. The connection is cleanly closed when the context manager is exited.

```python
from pycommander import AemStream
from pycommander_core.types import AemMeasurement

# Instantiate a 10 second AEM stream with a data output rate of 100 Hz
with AemStream(serial_number="44055955", datarate_hz=100, duration_s=10) as aem_stream:
  for measurement in aem_stream:
    print(measurement)
```

##### Manual Syntax

The `AemStream` class can also be instantiated without using the context manager syntax. In this case, the `open()` method must be called to open the connection to the adapter and start the data capture process, and the `close()` method must be called to gracefully stop the data capture process and close the connection.

```python
from pycommander import AemStream
from pycommander_core.types import AemMeasurement

# Instantiate the AemStream class with a serial number and a set data rate
aem_stream : AemStream = AemStream(serial_number="44055955", datarate_hz=100)

# Open the AEM stream
aem_stream.open()


some_condition : bool = False
# Read the AEM measurements
for measurement in aem_stream:
  # Do something
  # ...

  if some_condition:
    break

# Close the AEM stream
aem_stream.close()
```
