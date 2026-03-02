"""Readmem command: read from target memory."""

from typing import Any

from pycommander_core.commands._base import BaseCommand


class ReadmemCommand(BaseCommand):
  """Read from target memory."""

  def _get_general_args(self, **kwargs: Any) -> list[str]:
    args = []
    args += self._get_adapter_connection_args()
    args += self._get_debug_args()
    args += self._get_kwargs(**kwargs)
    return args

  def readmem(self,
              outfile: str | None = None,
              ranges: list[tuple[int | str, int | str]] = [],
              regions: list[str] = [],
              **kwargs: Any) -> dict:
    """Read from target memory.

    Args:
      outfile (str): Output file (bin, hex, s37 by extension). If not given, data is printed.
      ranges (list[tuple[int | str, int | str]]): Memory ranges to read (start, end).
      regions (list[str]): Named memory regions (@region) to read.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if outfile:
      args += ["--outfile", outfile]
    if ranges:
      args += self._get_ranges(ranges)
    if regions:
      args += self._get_regions(regions)
    return self._run("readmem", *args).output
