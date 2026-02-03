from pycommander.commands._base import BaseCommand

class ConvertCommand(BaseCommand):

  def _get_general_args(self) -> list[str]:
    args = []
    args += self._get_device_args()
    args += self._get_flags()
    return args

  def convert(self,
              infiles: list[str],
              outfile: str | None = None,
              address: int | None = None,
              patches: list[str] = [],
              ranges: list[tuple[int, int]] = [],
              token: list[str] | None = None,
              tokenfile: str | None = None,
              tokengroup: str | None = None,
              tokendefs: str | None = None,
              secureboot: bool = False,
              keyfile: str | None = None,
              crc: bool = False,
              certificate: str | None = None,
              aeskey: str | None = None,
              include_sections: list[str] = [],
              exclude_sections: list[str] = [],
              extsign: bool = False,
              signature: str | None = None,
              verify_key: str | None = None) -> dict:
    args = list(infiles) + self._get_general_args()
    if outfile is not None:
      args += ["--outfile", outfile]
    if address is not None:
      args += ["--address", self._get_address(address)]
    if patches:
      for p in patches:
        args += ["--patch", p]
    if ranges:
      args += self._get_ranges(ranges)
    if token:
      for t in token:
        args += ["--token", t]
    if tokenfile is not None:
      args += ["--tokenfile", tokenfile]
    if tokengroup is not None:
      args += ["--tokengroup", tokengroup]
    if tokendefs is not None:
      args += ["--tokendefs", tokendefs]
    if secureboot:
      args += ["--secureboot"]
    if keyfile is not None:
      args += ["--keyfile", keyfile]
    if crc:
      args += ["--crc"]
    if certificate is not None:
      args += ["--certificate", certificate]
    if aeskey is not None:
      args += ["--aeskey", aeskey]
    if include_sections:
      args += self._get_include_sections(include_sections)
    if exclude_sections:
      args += self._get_exclude_sections(exclude_sections)
    if extsign:
      args += ["--extsign"]
    if signature is not None:
      args += ["--signature", signature]
    if verify_key is not None:
      args += ["--verify", verify_key]
    return self._run("convert", *args).output
