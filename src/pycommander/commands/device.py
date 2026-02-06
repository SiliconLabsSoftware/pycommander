"""Device commands: info, lock, unlock, masserase, pageerase, protect, recover, reset, zwave-qrcode."""

from typing import Any

from pycommander.commands._base import BaseCommand


class DeviceCommand(BaseCommand):
  """Commands that affect the target device."""

  def _get_general_args(self, **kwargs: Any) -> list[str]:
    args = []
    args += self._get_adapter_connection_args()
    args += self._get_debug_args()
    args += self._get_kwargs(**kwargs)
    return args

  def info(self, **kwargs: Any) -> dict:
    """Show information about the connected target device (MCU/radio/SoC).

    Returns:
      Command output as parsed JSON (dict).
    """
    return self._run("device", "info", *self._get_general_args(**kwargs)).output

  def lock(self, **kwargs: Any) -> dict:
    """Lock debug access.

    Returns:
      Command output as parsed JSON (dict).
    """
    return self._run("device", "lock", *self._get_general_args(**kwargs)).output

  def unlock(self, **kwargs: Any) -> dict:
    """Unlock debug access.

    Returns:
      Command output as parsed JSON (dict).
    """
    return self._run("device", "unlock", *self._get_general_args(**kwargs)).output

  def masserase(self, **kwargs: Any) -> dict:
    """Execute a device mass erase, clearing the main flash.

    Returns:
      Command output as parsed JSON (dict).
    """
    return self._run("device", "masserase", *self._get_general_args(**kwargs)).output

  def pageerase(self, ranges: list[tuple[int, int]] = [], regions: list[str] = [], **kwargs: Any) -> dict:
    """Erase selected flash pages.

    Args:
      ranges (list[tuple[int,int]]): Memory ranges to erase (start, end); extended to page boundaries.
      regions (list[str]): Named memory regions (@region).

    Returns:
      Command output as parsed JSON (dict).
    """
    args = []
    args += self._get_ranges(ranges)
    args += self._get_regions(regions)
    args += self._get_general_args(**kwargs)

    return self._run("device", "pageerase", *args).output

  def protect(self,
              read: bool = False,
              write: bool = False,
              disable: bool = False,
              ranges: list[tuple[int, int]] = [],
              regions: list[str] = [],
              **kwargs: Any) -> dict:
    """Protect flash or functionality (read/write protection).

    Args:
      read (bool): Enable/disable read protection.
      write (bool): Enable/disable write protection.
      disable (bool): Disable read/write protection; if not set, enable is implied.
      ranges (list[tuple[int,int]]): Memory ranges to protect (start, end).
      regions (list[str]): Named memory regions (@region).

    Returns:
      Command output as parsed JSON (dict).
    """
    args = []
    if read:
      args += ["--read"]
    if write:
      args += ["--write"]
    if disable:
      args += ["--disable"]

    args += self._get_ranges(ranges)
    args += self._get_regions(regions)
    args += self._get_general_args(**kwargs)

    return self._run("device", "protect", *args).output

  def recover(self, **kwargs: Any) -> dict:
    """Recover a bricked device.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = []
    args += self._get_adapter_connection_args()
    args += self._get_kwargs(**kwargs)

    args += self.__get_debug_speed_option()

    return self._run("device", "recover", *self._get_general_args(**kwargs)).output

  def reset(self, **kwargs: Any) -> dict:
    """Reset the target device.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = []
    args += self._get_adapter_connection_args()
    args += self._get_kwargs(**kwargs)

    return self._run("device", "reset", *args).output

  def zwave_qrcode(self, timeout_ms: int = 0) -> dict:
    """Get QR code from Z-Wave application.

    Args:
      timeout_ms (int): Milliseconds to wait for QR code to be initialized (default 5000).

    Returns:
      Command output as parsed JSON (dict).
    """
    args = []
    args += self._get_general_args()
    args += ["--timeout", str(timeout_ms)]

    return self._run("device", "zwave-qrcode", *args).output
