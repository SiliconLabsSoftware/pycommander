# Silicon Labs PyCommander (CLI version)

## Introduction

This Python package wraps Simplicity Commander functionality and exposes a native Python API for interacting with Commander in your scripts.

## Requirements

This package requires Python 3.10 or newer. Required PyPI packages are:

- platformdirs
- pyyaml

Additionally, Simplicity Commander requires the SEGGER J-Link drivers to be installed on your system.

Note that this package only contains the CLI version of Simplicity Commander. The GUI version is available in the `silabs-pycommander-gui` package.

## Installation

```bash
pip install silabs-pycommander-cli
```

## Usage

More details about Simplicity Commander and its Command Line Interface can be found in the [official documentation for Simplicity Commander](https://docs.silabs.com/simplicity-commander/latest/simplicity-commander-start/). The documentation is also helpful when using the Python API, as the command names and available options are the same.

### Command Line Interface

From the command line, `pycommander-cli` is a razor-thin wrapper around the Simplicity Commander CLI; it behaves exactly like the Simplicity Commander CLI, except for the case when the options `-v` or `--version` are passed as arguments, in which case the version of the `pycommander-cli` package is printed in addition to the normal version information from the Simplicity Commander CLI.

```bash
pycommander-cli --help
pycommander-cli --version
pycommander-cli <command> [options]
pycommander-cli <command> <subcommand> [options]
```

### Python API

At the lowest level, the `Commander` class provides all the CLI commands as methods to the class. These methods return a dictionary containing the command output, similarly to what the Simplicity Commander CLI does when the `--json` flag is used.

```python
from pycommander_cli import Commander

# Instantiate the Commander class with a serial number
commander = Commander(serial_number="44055955")

# Perform the 'commander device info' command
print(commander.device.info(target_device="EFR32MG24"))

# Perform the 'commander util appinfo' command
print(commander.util.appinfo(filename="firmware.hex"))

# Perform the 'commander flash' command
print(commander.flash.flash(filenames=["firmware.hex"], address=0x08000000))
```

The `Commander` class also exposes a few standalone helpers; for example, `getVersion()` returns the embedded Simplicity Commander, J-Link, EMDLL and other component versions as a `CommanderVersionInfo` object:

```python
print(commander.getVersion())
```

Please note that not all commands are available to the `Commander` class. These are typically commands that are intended for interative CLI sessions, and include command suites like `vcom`, `vuart`, `rtt` and `swo`. Moreover, some commands in the `Commander` class have stricter requirements for the arguments than their CLI counterparts, for the same reasons as mentioned above. For example, the `aem dump` command requires the `outfile` and `duration` arguments to be provided. For a more flexible approach to streaming AEM data, please see the `AemStream` class below.

For ad-hoc invocations of commands that are not exposed by the typed API, you can fall back to `Commander.runCommand(...)`, which forwards arguments directly to the underlying Simplicity Commander CLI:

```python
# Run a raw Commander CLI command and capture its output
result = commander.runCommand("rtt", "--help", json_formatted_output=False)
print(result.output)
```

#### The `Adapter` and `Target` classes

pycommander-cli exposes several convenience methods for common tasks related to the adapter and the target device. These methods return different data types depending on the command. The types are available in the `pycommander_core.types` module, and the tasks include:

- Locking/unlocking the device for debug access
- Setting the CTUNE value
- Setting the adapter's VCOM configuration
- Configuring the target device's voltage
- Flashing firmware to the device
- Erasing the device's flash
- Configuring code regions (Series 3 only)
- +++

When instantiating the `Adapter` class, a `Commander` class instance is created and made available as an attribute of the `Adapter` class. If a `target_device` is provided to the `Adapter` class, a `Target` class instance is created and made available as an attribute of the `Adapter` class as well.

An `Adapter` class instance (with a potential `Target` class instance) should be used to represent a connection to a single adapter (with target device). Multiple `Adapter` class instances can be used to represent connections to multiple adapters (with or without their respective target devices):

```python
from pycommander_cli import Adapter

serial_numbers = ["44055955", "44055956", "44055957"]
adapters = [Adapter(serial_number=sn, target_device="EFR32MG24") for sn in serial_numbers]
for adapter in adapters:
  print(adapter.info())
```

The serial numbers above can be obtained by scanning for available adapters. `Commander.listAvailableAdapters()` does a non-intrusive scan and returns a list of `BasicAdapterInfo` objects, each carrying `jlink_serial_number`, `ip_address` and `nickname` (any of which may be `None`). Exactly one of `list_usb_adapters` or `list_network_adapters` must be set to `True`:

```python
from pycommander_cli import Commander

commander = Commander()

usb_adapters = commander.listAvailableAdapters(list_usb_adapters=True)
network_adapters = commander.listAvailableAdapters(list_network_adapters=True)

for adapter in usb_adapters or []:
  print(adapter.jlink_serial_number, adapter.nickname)
```

A typical session against a single adapter may look like this:

```python
from pycommander_cli import Adapter
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

A common high-level task is flashing firmware. `Target.flashApplication()` accepts one or more files (`.hex`, `.s37`, `.bin`, `.gbl` or `.rps`) and handles the underlying flash, verify and reset steps:

```python
from pathlib import Path
from pycommander_cli import Adapter

adapter = Adapter(serial_number="44055955", target_device="EFR32MG24")

success: bool = adapter.target.flashApplication(filenames=[Path("firmware.hex")])
```

#### The `AemStream` class

The `AemStream` class provides a pythonic way of streaming AEM measurements from the device. The measurements are returned as `AemMeasurement` objects, which contain the timestamp, current, voltage, and the calculated power. An `AemStream` object is suitable for streaming AEM measurements from an adapter, and there is no limitation to the duration of the streaming. The stream may be stopped at any time.

Like the underlying Simplicity Commander CLI, the `AemStream` class supports a variety of options for configuring the AEM data capture process, like setting up simple triggers to start the data capture process and specifying the data output rate.

##### Context Manager Syntax

If using the context manager syntax, the `AemStream` object is opened automatically when the context manager is entered, and a connection to the adapter is established. The connection is cleanly closed when the context manager is exited.

```python
from pycommander_cli import AemStream
from pycommander_core.types import AemMeasurement

# Instantiate a 10 second AEM stream with a data output rate of 100 Hz
with AemStream(serial_number="44055955", datarate_hz=100, duration_s=10) as aem_stream:
  for measurement in aem_stream:
    print(measurement)
```

##### Manual Syntax

The `AemStream` class can also be instantiated without using the context manager syntax. In this case, the `open()` method must be called to open the connection to the adapter and start the data capture process, and the `close()` method must be called to gracefully stop the data capture process and close the connection.

```python
from pycommander_cli import AemStream
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

#### Error handling

Failed Commander invocations raise typed exceptions, so your automation scripts can react to them in a structured way. Three exception classes are exposed from `pycommander_core.errors`:

- `PyCommanderInputError` — Commander rejected the arguments (return code -1 / 255).
- `PyCommanderRuntimeError` — Commander failed at runtime, e.g. the adapter could not be reached or the operation timed out (return code -2 / 254).
- `PyCommanderError` — base class for any other non-zero return code, and parent of the two above.

```python
from pathlib import Path
from pycommander_cli import Adapter
from pycommander_core.errors import PyCommanderError, PyCommanderRuntimeError

adapter = Adapter(serial_number="44055955", target_device="EFR32MG24")

try:
  adapter.target.flashApplication(filenames=[Path("firmware.hex")])
except PyCommanderRuntimeError as e:
  print(f"Commander failed at runtime: {e}")
except PyCommanderError as e:
  print(f"Other Commander error: {e}")
```

#### Logging

All Commander invocations can be logged to a file by passing the `log_file_path` argument to the `Commander` constructor. Each invocation is recorded with a timestamp, which is handy when diagnosing issues in long-running automations or production-test rigs.

```python
from pathlib import Path
from pycommander_cli import Adapter, Commander

# Build a Commander with logging enabled, then attach it to an Adapter
commander = Commander(serial_number="44055955", log_file_path=Path("pycommander.log"))
adapter = Adapter(commander=commander, target_device="EFR32MG24")
```
