from pycommander.commands._base import BaseCommand

class ExtflashCommand(BaseCommand):

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
    args = self._get_general_args()
    if address is not None:
      args += ["--address", self._get_address_string(address)]
    if board_id is not None:
      args += ["--board-id", board_id]
    if not verify:
      args += ["--noverify"]
    return self._run("extflash", "write", filename, *args).output
