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
commander = Commander(serial_number="440055955")

# Perform the 'commander device info' command
print(commander.device.info(target_device="EFR32MG24"))

# Perform the 'commander util appinfo' command
print(commander.util.appinfo(filename="firmware.hex"))

# Perform the 'commander flash' command
print(commander.flash.flash(filenames=["firmware.hex"], address=0x08000000))
```

The `Commander` class also exposes a few standalone helpers; for example, `getVersion()` returns the embedded Simplicity Commander, J-Link, EMDLL and other component versions as a `CommanderVersionInfo` object:

```python
from pycommander_cli import Commander

commander = Commander()

# Get the version of the embedded Simplicity Commander, J-Link, EMDLL and other components
print(commander.getVersion())
```

`listAvailableAdapters()` is a helper method that can be used to (unintrusively) scan for available adapters. This method returns a list of `BasicAdapterInfo` objects, each carrying `jlink_serial_number`, `ip_address` and `nickname` (any of which may be `None`):

```python
from pycommander_cli import Commander

commander = Commander()

# List USB adapters
adapters = commander.listAvailableAdapters(list_usb_adapters=True)
for adapter in adapters:
  print(adapter.jlink_serial_number, adapter.nickname)

# List network adapters
adapters = commander.listAvailableAdapters(list_network_adapters=True)
for adapter in adapters:
  print(adapter.ip_address, adapter.nickname)
```

Please note that not all commands are available to the `Commander` class. Moreover, some commands in the `Commander` class have stricter requirements for the arguments than their CLI counterparts. For example, the `aem dump` command requires the `outfile` and `duration` arguments to be provided. For a more flexible approach to streaming AEM data, please see the `AemStream` class below. For streaming SWO data, please see the `SwoStream` class below. For streaming RTT data, please see the `RttStream` class below. For streaming VCOM data, please see the `VcomStream` class below. For streaming VUART data, please see the `VuartStream` class below.

For ad-hoc invocations of commands that are not exposed by the typed API, you can fall back to `Commander.runCommand(...)`, which forwards arguments directly to the underlying Simplicity Commander CLI:

```python
# Run a raw Commander CLI command and capture its output
result = commander.runCommand("rtt", "--help", json_formatted_output=False)
print(result.stdout)
print(result.stderr)
```

#### The `Adapter` and `Target` classes

pycommander-cli exposes several convenience methods for common tasks, split across two classes. These methods return different data types depending on the command. The types are available in the `pycommander_core.types` module.

The `Adapter` class handles tasks related to the adapter itself. These methods are only available on Silicon Labs adapters, and are not functional when using a generic J-Link adapter:

- Reading adapter and kit information
- Upgrading the adapter's firmware
- Resetting the adapter
- Configuring the target device's supply voltage
- Setting the adapter's VCOM configuration
- Analyzing the target device's energy usage
- +++

The `Target` class handles tasks related to the target device (a Silicon Labs MCU), and works with any supported debug adapter:

- Locking/unlocking the device for debug access
- Setting the CTUNE value
- Flashing firmware to the device
- Erasing the device's flash
- Configuring code regions (Series 3 only)
- +++

When instantiating the `Adapter` class, a `Commander` class instance is created and made available as an attribute of the `Adapter` class. If a `target_device` is provided to the `Adapter` class, a `Target` class instance is created and made available as an attribute of the `Adapter` class as well.

An `Adapter` class instance (with a potential `Target` class instance) should be used to represent a connection to a single Silicon Labs adapter (with an attached target device). Multiple `Adapter` class instances can be used to represent multiple adapters (with or without their respective target devices):

```python
from pycommander_cli import Adapter

serial_numbers = ["440055955", "440055956", "440055957"]
adapters = [Adapter(serial_number=sn, target_device="EFR32MG24") for sn in serial_numbers]
for adapter in adapters:
  print(adapter.info())
```

A typical session against a single adapter may look like this:

```python
from pycommander_cli import Adapter
from pycommander_core.types import AdapterInfo, AdapterVoltageInfo, VcomHandshake, CtuneValue

# Instantiate the Adapter class with a serial number and target device
adapter = Adapter(serial_number="440055955", target_device="EFR32MG24")

# Ensure we're running the latest firmware on the adapter
adapter.upgradeFirmware()

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

A common high-level task is flashing application firmware to the target device. `Target.flashApplication()` accepts one or more files (`.hex`, `.s37`, `.bin`, `.gbl` or `.rps`) and handles the underlying flash, verify and reset steps:

```python
from pathlib import Path
from pycommander_cli import Adapter

adapter = Adapter(serial_number="440055955", target_device="EFR32MG24")

success: bool = adapter.target.flashApplication(filenames=[Path("firmware.hex")])
```

#### The `AemStream` class

The `AemStream` class provides a pythonic way of streaming AEM measurements from a Silicon Labs adapter. The measurements are returned as `AemMeasurement` objects, which contain the timestamp, current, voltage, and the calculated power. An `AemStream` object is suitable for streaming AEM measurements from a Silicon Labs adapter, and there is no limitation to the duration of the streaming. The stream may be stopped at any time.

Like the underlying Simplicity Commander CLI, the `AemStream` class supports a variety of options for configuring the AEM data capture process, like setting up simple triggers to start the data capture process and specifying the data output rate.

##### Context Manager Syntax

When using the context manager syntax, the `AemStream` object is opened automatically when the context manager is entered, and a connection to the adapter is established. The connection is cleanly closed when the context manager is exited.

```python
from pycommander_cli import AemStream
from pycommander_core.types import AemMeasurement

# Instantiate a 10 second AEM stream with a data output rate of 100 Hz
with AemStream(serial_number="440055955", datarate_hz=100, duration_s=10) as aem_stream:
  for measurement in aem_stream:
    print(measurement)
```

##### Manual Syntax

The `AemStream` class can also be instantiated without using the context manager syntax. In this case, the `open()` method must be called to open the connection to the adapter and start the data capture process, and the `close()` method must be called to gracefully stop the data capture process and close the connection.

```python
from pycommander_cli import AemStream
from pycommander_core.types import AemMeasurement

# Instantiate the AemStream class with a serial number and a set data rate
aem_stream : AemStream = AemStream(serial_number="440055955", datarate_hz=100)

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

#### The `SwoStream` class

The `SwoStream` class provides a pythonic way of streaming Serial Wire Output (SWO) data from a target device. Each iteration yields a line of text written by the target application. The stream may be stopped at any time; exiting the context manager (or calling `close()`) sends a clean shutdown to Commander.

Like the underlying Simplicity Commander `swo read` command, `SwoStream` supports configuring the SWO speed, ITM channel, an idle timeout, an end marker, monitoring all channels for end conditions, hexadecimal output, and skipping the target reset that is otherwise performed when the capture starts.

##### Context Manager Syntax

When using the context manager syntax, the `SwoStream` object is opened automatically when the context manager is entered, and a connection to the adapter is established. The connection is cleanly closed when the context manager is exited.

```python
from pycommander_cli import SwoStream

# Read SWO until the target prints --finished--, or 5 seconds pass with no data
with SwoStream(serial_number="440055955", timeout_s=5, endmarker="--finished--") as swo_stream:
  for line in swo_stream:
    print(line, end="", flush=True)
```

##### Manual Syntax

The `SwoStream` class can also be instantiated without using the context manager syntax. In this case, the `open()` method must be called to open the connection to the adapter and start the capture, and the `close()` method must be called to gracefully stop the capture and close the connection.

```python
from pycommander_cli import SwoStream

# Instantiate the SwoStream class with a serial number and SWO speed
swo_stream : SwoStream = SwoStream(serial_number="440055955", swospeed_hz=875000)

# Open the SWO stream
swo_stream.open()


some_condition : bool = False
# Read the SWO output
for line in swo_stream:
  # Do something
  # ...

  if some_condition:
    break

# Close the SWO stream
swo_stream.close()
```

#### The `RttStream` class

The `RttStream` class provides a pythonic, read-only way of streaming Real Time Transfer (RTT) data from a target device. Each iteration yields data written by the target application. The stream may be stopped at any time; exiting the context manager (or calling `close()`) sends a clean shutdown to Commander.

Like the underlying Simplicity Commander `rtt connect` command, `RttStream` supports configuring the RTT control block address, read and write buffers, virtual terminal, an idle timeout, an end marker, line endings, skipping the target reset, and sending one-shot startup command(s) after connect.

##### Context Manager Syntax

When using the context manager syntax, the `RttStream` object is opened automatically when the context manager is entered, and a connection to the adapter is established. The connection is cleanly closed when the context manager is exited.

```python
from pycommander_cli import RttStream

# Read RTT until the target prints DONE, or 5 seconds pass with no data
with RttStream(serial_number="440055955", timeout_s=5, endmarker="DONE", command="status") as rtt_stream:
  for line in rtt_stream:
    print(line, end="", flush=True)
```

##### Manual Syntax

The `RttStream` class can also be instantiated without using the context manager syntax. In this case, the `open()` method must be called to open the connection to the adapter and start the capture, and the `close()` method must be called to gracefully stop the capture and close the connection.

```python
from pycommander_cli import RttStream

# Instantiate the RttStream class with a serial number
rtt_stream : RttStream = RttStream(serial_number="440055955")

# Open the RTT stream
rtt_stream.open()


some_condition : bool = False
# Read the RTT output
for line in rtt_stream:
  # Do something
  # ...

  if some_condition:
    break

# Close the RTT stream
rtt_stream.close()
```

#### The `VcomStream` class

The `VcomStream` class provides a pythonic, read-only way of streaming Virtual COM port (VCOM) data from a target device. Each iteration yields data written by the target application. The stream may be stopped at any time; exiting the context manager (or calling `close()`) sends a clean shutdown to Commander.

Like the underlying Simplicity Commander `vcom connect` command, `VcomStream` supports hexadecimal output, restarting the target in ISP mode, line endings, and sending one-shot startup command(s) after connect. Adapter VCOM baudrate and handshake are configured separately, for example via `Commander.vcom.config`.

##### Context Manager Syntax

When using the context manager syntax, the `VcomStream` object is opened automatically when the context manager is entered, and a connection to the adapter is established. The connection is cleanly closed when the context manager is exited.

```python
from pycommander_cli import VcomStream

# Read VCOM after sending a one-shot startup command
with VcomStream(serial_number="440055955", command="status") as vcom_stream:
  for line in vcom_stream:
    print(line, end="", flush=True)
```

##### Manual Syntax

The `VcomStream` class can also be instantiated without using the context manager syntax. In this case, the `open()` method must be called to open the connection to the adapter and start the capture, and the `close()` method must be called to gracefully stop the capture and close the connection.

```python
from pycommander_cli import VcomStream

# Instantiate the VcomStream class with a serial number
vcom_stream : VcomStream = VcomStream(serial_number="440055955")

# Open the VCOM stream
vcom_stream.open()


some_condition : bool = False
# Read the VCOM output
for line in vcom_stream:
  # Do something
  # ...

  if some_condition:
    break

# Close the VCOM stream
vcom_stream.close()
```

#### The `VuartStream` class

The `VuartStream` class provides a pythonic, read-only way of streaming VUART data from a target device over IP. Each iteration yields data written by the target application. The stream may be stopped at any time; exiting the context manager (or calling `close()`) sends a clean shutdown to Commander.

Like the underlying Simplicity Commander `vuart connect` command, `VuartStream` requires an IP address and supports an idle timeout, an end marker, line endings, and sending one-shot startup command(s) after connect.

##### Context Manager Syntax

When using the context manager syntax, the `VuartStream` object is opened automatically when the context manager is entered, and a connection to the adapter is established. The connection is cleanly closed when the context manager is exited.

```python
from pycommander_cli import VuartStream

# Read VUART until the target prints DONE, or 5 seconds pass with no data
with VuartStream(ip_address="192.168.1.100", timeout_s=5, endmarker="DONE", command="status") as vuart_stream:
  for line in vuart_stream:
    print(line, end="", flush=True)
```

##### Manual Syntax

The `VuartStream` class can also be instantiated without using the context manager syntax. In this case, the `open()` method must be called to open the connection to the adapter and start the capture, and the `close()` method must be called to gracefully stop the capture and close the connection.

```python
from pycommander_cli import VuartStream

# Instantiate the VuartStream class with an IP address
vuart_stream : VuartStream = VuartStream(ip_address="192.168.1.100")

# Open the VUART stream
vuart_stream.open()


some_condition : bool = False
# Read the VUART output
for line in vuart_stream:
  # Do something
  # ...

  if some_condition:
    break

# Close the VUART stream
vuart_stream.close()
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

adapter = Adapter(serial_number="440055955", target_device="EFR32MG24")

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
commander = Commander(serial_number="440055955", log_file_path=Path("pycommander.log"))
adapter = Adapter(commander=commander, target_device="EFR32MG24")
```
