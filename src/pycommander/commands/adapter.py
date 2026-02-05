"""Adapter commands: dbgmode, drivermode, fwupgrade, ip, list, nick, power, probe, reset, voltage."""

from pycommander.commands._base import BaseCommand


class AdapterCommand(BaseCommand):
  """Commands that affect a debug adapter (kit/debugger)."""

  def _get_general_args(self) -> list[str]:
    args = []
    args += self._get_adapter_connection_args()
    args += self._get_device_args()
    args += self._get_flags()
    return args

  def dbgmode(self, mode: str | None = None) -> dict:
    """Get or set the debug mode.

    Args:
      mode (str): Debug mode to set (MCU, IN, OUT, OFF). If not provided, gets current mode.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args()
    mode_string = mode if mode is not None else ""
    return self._run("adapter", "dbgmode", mode_string, *args).output

  def drivermode(self, mode: str | None = None) -> dict:
    """Select driver mode - WinUSB (driverless) or SEGGER (legacy).

    Args:
      mode (str): One of winusb or segger.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args()
    mode_string = mode if mode is not None else ""
    return self._run("adapter", "drivermode", mode_string, *args).output

  def fwupgrade(self, filename: str | None = None, check: bool = True) -> dict:
    """Upgrade the firmware of the selected kit or debug adapter.

    Args:
      filename (str): Firmware package to load (*.emz). If not provided, uses bundled.
      check (bool): If True, only install if bundled version is newer than installed.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args()
    filename_string = filename if filename is not None else ""
    if not check:
      args += ["--nocheck"]
    return self._run("adapter", "fwupgrade", filename_string, *args).output

  def fwupgradecheck(self) -> dict:
    """Check if a firmware upgrade is available for the selected kit or debug adapter.

    Returns:
      Command output as parsed JSON (dict).
    """
    return self._run("adapter", "fwupgradecheck", *self._get_general_args()).output

  def ip(self,
         dhcp: bool = False,
         addr: str | None = None,
         dns: str | None = None,
         gw: str | None = None) -> dict:
    """Get or set adapter IP configuration. If no options are given, current config is displayed.

    Args:
      dhcp (bool): Use DHCP to automatically configure IP settings.
      addr (str): Set IP address (CIDR notation).
      dns (str): Set DNS server address.
      gw (str): Set gateway address.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args()
    if dhcp:
      args += ["--dhcp"]
    if addr is not None:
      args += ["--addr", addr]
    if dns is not None:
      args += ["--dns", dns]
    if gw is not None:
      args += ["--gw", gw]
    return self._run("adapter", "ip", *args).output

  def list(self,
           net: bool = False,
           filter_regex: str | None = None,
           connect: bool = True) -> dict:
    """List all kits currently connected.

    Args:
      net (bool): Include network adapters.
      filter_regex (str): Filter results by regex.
      connect (bool): Connect to adapters when listing.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args()
    if net:
      args += ["--net"]
    if filter_regex is not None:
      args += ["--filter", filter_regex]
    if not connect:
      args += ["--noconnect"]    
    return self._run("adapter", "list", *args).output

  def nick(self, nickname: str | None = None, clear: bool = False) -> dict:
    """Get or set the nickname of the adapter.

    Args:
      nickname (str): Nickname to set. If not provided, gets nickname from adapter.
      clear (bool): Clear the nickname of the adapter.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args()
    nickname_string = nickname if nickname is not None else ""
    if clear:
      args += ["--clear"]
    return self._run("adapter", "nick", nickname_string, *args).output

  def power(self, state: str | None = None) -> dict:
    """Get or set the power state of the target device.

    Args:
      state (str): Set target power on or off. If not provided, gets current state.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args()
    state_string = state if state is not None else ""
    return self._run("adapter", "power", state_string, *args).output

  def probe(self,
            fw: bool = False,
            kit: bool = False,
            boards: bool = False) -> dict:
    """Retrieve information about the current kit or debug adapter.

    Args:
      fw (bool): Show information about the currently installed firmware.
      kit (bool): Show information about the kit.
      boards (bool): Show detailed list of mainboard and connected radio/expansion boards.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args()
    if fw:
      args += ["--fw"]
    if kit:
      args += ["--kit"]
    if boards:
      args += ["--boards"]
    return self._run("adapter", "probe", *args).output

  def reset(self) -> dict:
    """Reset the selected kit or debug adapter.

    Returns:
      Command output as parsed JSON (dict).
    """
    return self._run("adapter", "reset", *self._get_general_args()).output

  def voltage(self, voltage: str | None = None, calibrate: bool = True) -> dict:
    """Get or set the voltage of the target device.

    Args:
      voltage (str): Voltage to set. If not provided, gets current target voltage.
      calibrate (bool): If True, automatically calibrate if voltage has changed.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args()
    voltage_string = voltage if voltage is not None else ""
    if not calibrate:
      args += ["--nocalibrate"]
    return self._run("adapter", "voltage", voltage_string, *args).output
