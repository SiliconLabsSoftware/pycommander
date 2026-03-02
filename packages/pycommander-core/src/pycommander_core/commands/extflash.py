"""External SPI flash commands: erase, read, write."""

from typing import Any

from pycommander_core.commands._base import BaseCommand


class ExtflashCommand(BaseCommand):
  """Commands to interact with an external SPI flash."""

  def _get_general_args(self, **kwargs: Any) -> list[str]:
    args = []
    args += self._get_adapter_connection_args()
    args += self._get_debug_args()
    args += self._get_kwargs(**kwargs)
    return args

  def erase(self,
            ranges: list[tuple[int | str, int | str]] = [],
            board_id: str | None = None,
            verify: bool = True,
            **kwargs: Any) -> dict:
    """Erase external flash.

    Args:
      ranges (list[tuple[int | str, int | str]]): Memory ranges to erase (start, end); format start:end or start:+length.
      board_id (str): Board ID for series 2 when default flashloader does not work.
      verify (bool): If True, verify contents after erase.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if ranges:
      args += self._get_ranges(ranges)
    if board_id:
      args += ["--board-id", board_id]
    if not verify:
      args += ["--noverify"]
    return self._run("extflash", "erase", *args).output

  def read(self,
           outfile: str | None = None,
           ranges: list[tuple[int | str, int | str]] = [],
           board_id: str | None = None,
           **kwargs: Any) -> dict:
    """Read from external flash.

    Args:
      outfile (str): Output file (bin, hex, s37 by extension). If not given, data is printed.
      ranges (list[tuple[int | str, int | str]]): Memory ranges to read (start, end).
      board_id (str): Board ID for series 2 when default flashloader does not work.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if outfile:
      args += ["--outfile", outfile]
    if ranges:
      args += self._get_ranges(ranges)
    if board_id:
      args += ["--board-id", board_id]
    return self._run("extflash", "read", *args).output

  def write(self,
            filename: str,
            address: int | None = None,
            board_id: str | None = None,
            verify: bool = True,
            **kwargs: Any) -> dict:
    """Write to external flash.

    Args:
      filename (str): File to flash.
      address (int): Memory address. Required for binary; not for hex/s37.
      board_id (str): Board ID for series 2 when default flashloader does not work.
      verify (bool): If True, verify contents after write.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if address is not None:
      args += ["--address", self._get_address_string(address)]
    if board_id:
      args += ["--board-id", board_id]
    if not verify:
      args += ["--noverify"]
    return self._run("extflash", "write", filename, *args).output
