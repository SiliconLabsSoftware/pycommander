"""External SPI flash commands: erase, read, write."""

from pycommander.commands._base import BaseCommand


class ExtflashCommand(BaseCommand):
  """Commands to interact with an external SPI flash."""

  def _get_general_args(self) -> list[str]:
    args = []
    args += self._get_adapter_connection_args()
    args += self._get_device_args()
    args += self._get_debug_args()
    args += self._get_flags()
    return args

  def erase(self,
            ranges: list[tuple[int, int]] = [],
            board_id: str | None = None,
            verify: bool = True) -> dict:
    """Erase external flash.

    Args:
      ranges (list[tuple[int,int]]): Memory ranges to erase (start, end); format start:end or start:+length.
      board_id (str): Board ID for series 2 when default flashloader does not work.
      verify (bool): If True, verify contents after erase.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args()
    if ranges:
      args += self._get_ranges(ranges)
    if board_id is not None:
      args += ["--board-id", board_id]
    if not verify:
      args += ["--noverify"]
    return self._run("extflash", "erase", *args).output

  def read(self,
           outfile: str | None = None,
           ranges: list[tuple[int, int]] = [],
           board_id: str | None = None) -> dict:
    """Read from external flash.

    Args:
      outfile (str): Output file (bin, hex, s37 by extension). If not given, data is printed.
      ranges (list[tuple[int,int]]): Memory ranges to read (start, end).
      board_id (str): Board ID for series 2 when default flashloader does not work.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args()
    if outfile is not None:
      args += ["--outfile", outfile]
    if ranges:
      args += self._get_ranges(ranges)
    if board_id is not None:
      args += ["--board-id", board_id]
    return self._run("extflash", "read", *args).output

  def write(self,
            filename: str,
            address: int | None = None,
            board_id: str | None = None,
            verify: bool = True) -> dict:
    """Write to external flash.

    Args:
      filename (str): File to flash.
      address (int): Memory address. Required for binary; not for hex/s37.
      board_id (str): Board ID for series 2 when default flashloader does not work.
      verify (bool): If True, verify contents after write.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args()
    if address is not None:
      args += ["--address", self._get_address_string(address)]
    if board_id is not None:
      args += ["--board-id", board_id]
    if not verify:
      args += ["--noverify"]
    return self._run("extflash", "write", filename, *args).output
