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
pip install "silabs-pycommander-cli"
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

Please note that not all commands are available to the `Commander` class. Moreover, some commands in the `Commander` class have stricter requirements for the arguments than their CLI counterparts. For example, the `aem dump` command requires the `outfile` and `duration` arguments to be provided. For long-running captures, prefer the [stream classes](#stream-classes) below.

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

#### Stream classes

Long-running Commander captures are wrapped as iterable stream objects: `AemStream`, `SwoConsoleStream`, `RttConsoleStream`, `VcomConsoleStream` and `VuartConsoleStream`. They share the same lifecycle.

Entering a `with` block (or calling `open()`) starts Commander. Iterate the object to receive data as it arrives, and stop at any time. Leaving the `with` block, or calling `close()`, shuts Commander down cleanly.

`AemStream` yields `AemMeasurement` objects (timestamp, current, voltage, and calculated power). The console streams yield device output as it arrives. Commander status stays on its own stdout; error lines raise a `RuntimeError` exception.

Most streams accept `serial_number` or `ip_address` as connection parameters. `VuartConsoleStream` is IP-only and therefore requires `ip_address`. Options such as `timeout_s`, `endmarker`, `lineending`, `command` and `hex_output` are available where the underlying Commander command supports them.

##### `AemStream`

Advanced Energy Monitor measurements from a Silicon Labs adapter. Configure the data rate, an optional duration, and simple start triggers.

```python
from pycommander_cli import AemStream

with AemStream(serial_number="440055955", datarate_hz=100, duration_s=10) as aem_stream:
  for measurement in aem_stream:
    print(measurement)
```

```python
from pycommander_cli import AemStream

aem_stream = AemStream(serial_number="440055955", datarate_hz=100)
aem_stream.open()
for measurement in aem_stream:
  print(measurement)
aem_stream.close()
```

##### `SwoConsoleStream`

Serial Wire Output (SWO) from the target device. Supports SWO speed, ITM channel, idle timeout, end marker, monitoring all channels for end conditions, hexadecimal output, and skipping the target reset.

```python
from pycommander_cli import SwoConsoleStream

with SwoConsoleStream(serial_number="440055955", timeout_s=5, endmarker="--finished--") as swo_stream:
  for line in swo_stream:
    print(line, end="", flush=True)
```

```python
from pycommander_cli import SwoConsoleStream

swo_stream = SwoConsoleStream(serial_number="440055955", swospeed_hz=875000)
swo_stream.open()
for line in swo_stream:
  print(line, end="", flush=True)
swo_stream.close()
```

##### `RttConsoleStream`

Segger Real Time Transfer (RTT) from the target device. Supports control-block address, read and write buffers, virtual terminal, idle timeout, end marker, line endings, skipping the target reset, and one-shot startup commands.

```python
from pycommander_cli import RttConsoleStream

with RttConsoleStream(serial_number="440055955", timeout_s=5, endmarker="DONE", command="status") as rtt_stream:
  for line in rtt_stream:
    print(line, end="", flush=True)
```

```python
from pycommander_cli import RttConsoleStream

rtt_stream = RttConsoleStream(serial_number="440055955")
rtt_stream.open()
for line in rtt_stream:
  print(line, end="", flush=True)
rtt_stream.close()
```

##### `VcomConsoleStream`

Virtual COM port on Silicon Labs adapters. Supports hexadecimal output, restarting the target in ISP mode, line endings, and one-shot startup commands. Configure baudrate and handshake separately with `Commander.vcom.config` or `Adapter.setVcomConfig`.

```python
from pycommander_cli import VcomConsoleStream

with VcomConsoleStream(serial_number="440055955", command="status") as vcom_stream:
  for line in vcom_stream:
    print(line, end="", flush=True)
```

```python
from pycommander_cli import VcomConsoleStream

vcom_stream = VcomConsoleStream(serial_number="440055955")
vcom_stream.open()
for line in vcom_stream:
  print(line, end="", flush=True)
vcom_stream.close()
```

##### `VuartConsoleStream`

Virtual UART (VUART) over IP (requires `ip_address`). Supports idle timeout, end marker, line endings, and one-shot startup commands.

```python
from pycommander_cli import VuartConsoleStream

with VuartConsoleStream(ip_address="192.168.1.100", timeout_s=5, endmarker="DONE", command="status") as vuart_stream:
  for line in vuart_stream:
    print(line, end="", flush=True)
```

```python
from pycommander_cli import VuartConsoleStream

vuart_stream = VuartConsoleStream(ip_address="192.168.1.100")
vuart_stream.open()
for line in vuart_stream:
  print(line, end="", flush=True)
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
