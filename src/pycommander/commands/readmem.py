from pycommander.commands._base import BaseCommand

class ReadmemCommand(BaseCommand):

  def _get_general_args(self) -> list[str]:
    args = []
    args += self._get_adapter_connection_args()
    args += self._get_device_args()
    args += self._get_debug_args()
    args += self._get_flags()
    return args

  def readmem(self,
              outfile: str | None = None,
              ranges: list[tuple[int, int]] = [],
              regions: list[str] = []) -> dict:
    args = self._get_general_args()
    if outfile is not None:
      args += ["--outfile", outfile]
    if ranges:
      args += self._get_ranges(ranges)
    if regions:
      args += self._get_regions(regions)
    return self._run("readmem", *args).output
