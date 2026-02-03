from pycommander.commands._base import BaseCommand

class FlashCommand(BaseCommand):

  def _get_general_args(self) -> list[str]:
    args = []
    args += self._get_adapter_connection_args()
    args += self._get_device_args()
    args += self._get_debug_args()
    args += self._get_flags()
    return args

  def flash(self,
            filenames: list[str],
            address: int | None = None,
            halt: bool = False,
            masserase: bool = False,
            reset: bool = True,
            close: bool = True,
            verify: bool = True,
            patches: list[str] = [],
            tokens: list[str] = [],
            tokenfile: str | None = None,
            tokengroup: str | None = None,
            tokendefs: str | None = None,
            binary: bool = False,
            include_sections: list[str] = [],
            exclude_sections: list[str] = [],
            vtor: int | None = None) -> dict:
    args = self._get_general_args()
    if address is not None:
      args += ["--address", self._get_address(address)]
    if halt:
      args += ["--halt"]
    if masserase:
      args += ["--masserase"]
    if not reset:
      args += ["--noreset"]
    if not close:
      args += ["--noclose"]
    if not verify:
      args += ["--noverify"]
    if patches:
      for p in patches:
        args += ["--patch", p]
    if tokens:
      for t in tokens:
        args += ["--token", t]
    if tokenfile is not None:
      args += ["--tokenfile", tokenfile]
    if tokengroup is not None:
      args += ["--tokengroup", tokengroup]
    if tokendefs is not None:
      args += ["--tokendefs", tokendefs]
    if binary:
      args += ["--binary"]
    if include_sections:
      args += self._get_include_sections(include_sections)
    if exclude_sections:
      args += self._get_exclude_sections(exclude_sections)
    if vtor is not None:
      args += ["--vtor", self._get_address(vtor)]
    return self._run("flash", *filenames, *args).output
