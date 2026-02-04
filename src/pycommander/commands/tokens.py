from pycommander.commands._base import BaseCommand

class TokensCommand(BaseCommand):

  def _get_general_args(self) -> list[str]:
    args = []
    args += self._get_adapter_connection_args()
    args += self._get_device_args()
    args += self._get_debug_args()
    args += self._get_flags()
    return args

  def createheader(self,
                   filename: str,
                   tokengroup: str | None = None,
                   tokendefs: str | None = None) -> dict:
    args = self._get_general_args()
    if tokengroup is not None:
      args += ["--tokengroup", tokengroup]
    if tokendefs is not None:
      args += ["--tokendefs", tokendefs]
    return self._run("tokens", "createheader", filename, *args).output

  def erase(self,
            securerange: tuple[int, int] | None = None,
            type: str | None = None,
            tokens: list[str] = [],
            tokengroup: str | None = None,
            tokendefs: str | None = None) -> dict:
    args = self._get_general_args()
    if securerange is not None:
      args += self._get_secureranges([securerange])
    if type is not None:
      args += ["--type", type]
    if tokens:
      args += self._get_tokens(tokens)
    if tokengroup is not None:
      args += ["--tokengroup", tokengroup]
    if tokendefs is not None:
      args += ["--tokendefs", tokendefs]
    return self._run("tokens", "erase", *args).output

  def read(self,
           filenames: list[str] | None = None,
           outfile: str | None = None,
           showoverrides: bool = False,
           tokens: list[str] = [],
           securerange: tuple[int, int] | None = None,
           tokengroup: str | None = None,
           tokendefs: str | None = None,
           range: tuple[int, int] | None = None,
           type: str | None = None,
           includeall: bool = False,
           address: int | None = None) -> dict:
    args = self._get_general_args()
    if filenames:
      args = list(filenames) + args
    if outfile is not None:
      args += ["--outfile", outfile]
    if tokens:
      args += self._get_tokens(tokens)
    if tokengroup is not None:
      args += ["--tokengroup", tokengroup]
    if tokendefs is not None:
      args += ["--tokendefs", tokendefs]
    if range is not None:
      args += self._get_ranges([range])
    if showoverrides:
      args += ["--showoverrides"]
    if securerange is not None:
      args += self._get_secureranges([securerange])
    if type is not None:
      args += ["--type", type]
    if includeall:
      args += ["--includeall"]
    if address is not None:
      args += ["--address", self._get_address_string(address)]
    return self._run("tokens", "read", *filenames, *args).output

  def write(self,
            tokenfiles: list[str] = [],
            tokens: list[str] = [],
            tokengroup: str | None = None,
            tokendefs: str | None = None,
            securerange: tuple[int, int] | None = None) -> dict:
    args = self._get_general_args()
    if tokenfiles:
      args += self._get_tokenfiles(tokenfiles)
    if tokens:
      args += self._get_tokens(tokens)
    if tokengroup is not None:
      args += ["--tokengroup", tokengroup]
    if tokendefs is not None:
      args += ["--tokendefs", tokendefs]
    if securerange is not None:
      args += self._get_secureranges([securerange])
    return self._run("tokens", "write", *args).output
