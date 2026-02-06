"""Convert/combine image files, set tokens, patch binary data."""

from typing import Any

from pycommander.commands._base import BaseCommand


class ConvertCommand(BaseCommand):
  """Conversion between image file formats; combine inputs, set tokens, patch data."""

  def _get_general_args(self, **kwargs: Any) -> list[str]:
    args = []
    args += self._get_kwargs(**kwargs)
    return args

  def convert(self,
              infiles: list[str],
              outfile: str | None = None,
              address: int | None = None,
              patches: list[str] = [],
              ranges: list[tuple[int, int]] = [],
              tokens: list[str] = [],
              tokenfiles: list[str] = [],
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
              verify_key: str | None = None,
              **kwargs: Any) -> dict:
    """Convert or combine input files to one output; set tokens and patch binary data.

    Args:
      infiles (list[str]): Input file(s) to convert or combine.
      outfile (str): Output file path.
      address (int): Start address when a .bin file is given as input.
      patches (list[str]): Patch memory; each entry address:data[:length] (up to 8 bytes).
      ranges (list[tuple[int,int]]): Limit output to these memory ranges (start, end).
      tokens (list[str]): Token overrides as TOKEN_NAME:value.
      tokenfiles (list[str]): Files describing tokens to write.
      tokengroup (str): Token set to use: common, zigbee, or znet.
      tokendefs (str): Path to JSON file defining the token set (alternative to tokengroup).
      secureboot (bool): Create Secure Boot image (requires keyfile, signature, or extsign).
      keyfile (str): ECC-P256 PEM private key for signing (e.g. from ebl keygen).
      crc (bool): Add CRC32 for bootloader integrity (cannot combine with secureboot).
      certificate (str): Certificate to append to Secure Boot application.
      aeskey (str): AES key file (util genkey --type aes-ccm) for bootloader app properties.
      include_sections (list[str]): ELF sections to include.
      exclude_sections (list[str]): ELF sections to exclude.
      extsign (bool): Output form suitable for external signature, insert later with --signature.
      signature (str): DER ECDSA signature file for signing (e.g. with extsign).
      verify_key (str): PEM public key to verify signed Secure Boot output.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = list(infiles) + self._get_general_args(**kwargs)
    if outfile is not None:
      args += ["--outfile", outfile]
    if address is not None:
      args += ["--address", self._get_address_string(address)]
    if patches:
      args += self._get_patches(patches)
    if ranges:
      args += self._get_ranges(ranges)
    if tokens:
      args += self._get_tokens(tokens)
    if tokenfiles:
      args += self._get_tokenfiles(tokenfiles)
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
