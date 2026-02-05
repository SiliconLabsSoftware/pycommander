"""Tokens commands: createheader, erase, read, write."""

from pycommander.commands._base import BaseCommand


class TokensCommand(BaseCommand):
  """Commands for handling manufacturing tokens."""

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
    """Create token header file.

    Args:
      filename (str): Output header file path.
      tokengroup (str): Token set: common, zigbee, or znet.
      tokendefs (str): Path to JSON token definitions.

    Returns:
      Command output as parsed JSON (dict).
    """
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
    """Erase tokens (on device or in secure range).

    Args:
      securerange (tuple[int,int]): Memory range for secure tokens.
      type (str): secure or device (static tokens only).
      tokens (list[str]): Token names to erase (TOKEN_NAME:value format for overrides).
      tokengroup (str): common, zigbee, or znet.
      tokendefs (str): Path to JSON token definitions.

    Returns:
      Command output as parsed JSON (dict).
    """
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
    """Read tokens from device or from file(s).

    Args:
      filenames (list[str]): Input file(s); if given, read from files instead of device.
      outfile (str): Output file; if not given, printed to stdout.
      showoverrides (bool): Show NVM3 overrides (static tokens only).
      tokens (list[str]): Limit output to these token names.
      securerange (tuple[int,int]): Range for static secure tokens.
      tokengroup (str): common, zigbee, or znet.
      tokendefs (str): Path to JSON token definitions.
      range (tuple[int,int]): NVM3 area range (start, end).
      type (str): secure or device (static tokens only).
      includeall (bool): Show all tokens in group (static only).
      address (int): Memory address.

    Returns:
      Command output as parsed JSON (dict).
    """
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
    """Write tokens to device.

    Args:
      tokenfiles (list[str]): Files describing tokens to write.
      tokens (list[str]): Token overrides as TOKEN_NAME:value.
      tokengroup (str): common, zigbee, or znet.
      tokendefs (str): Path to JSON token definitions.
      securerange (tuple[int,int]): Range for secure tokens.

    Returns:
      Command output as parsed JSON (dict).
    """
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
