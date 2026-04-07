"""
License
Copyright 2026 Silicon Laboratories Inc. www.silabs.com
*******************************************************************************
The licensor of this software is Silicon Laboratories Inc. Your use of this
software is governed by the terms of Silicon Labs Master Software License
Agreement (MSLA) available at
www.silabs.com/about-us/legal/master-software-license-agreement. This
software is distributed to you in Source Code format and is governed by the
sections of the MSLA applicable to Source Code.
*******************************************************************************
"""

"""Tokens commands: createheader, erase, read, write."""

from typing import Any

from pycommander_core.commands._base import BaseCommand


class TokensCommand(BaseCommand):
  """Commands for handling manufacturing tokens."""

  def _get_general_args(self, **kwargs: Any) -> list[str]:
    args = []
    args += self._get_adapter_connection_args()
    args += self._get_debug_args()
    args += self._get_kwargs(**kwargs)
    return args

  def createheader(self,
                   filename: str,
                   tokengroup: str | None = None,
                   tokendefs: str | None = None,
                   **kwargs: Any) -> dict:
    """Create token header file.

    Args:
      filename (str): Output header file path.
      tokengroup (str): Token set: common, zigbee, or znet.
      tokendefs (str): Path to JSON token definitions.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if tokengroup:
      args += ["--tokengroup", tokengroup]
    if tokendefs:
      args += ["--tokendefs", tokendefs]
    return self._run("tokens", "createheader", filename, *args).output

  def erase(self,
            securerange: tuple[int | str, int | str] | None = None,
            type: str | None = None,
            tokens: list[str] = [],
            tokengroup: str | None = None,
            tokendefs: str | None = None,
            **kwargs: Any) -> dict:
    """Erase tokens (on device or in secure range).

    Args:
      securerange (tuple[int | str, int | str]): Memory range for secure tokens.
      type (str): secure or device (static tokens only).
      tokens (list[str]): Token names to erase.
      tokengroup (str): common, zigbee, or znet.
      tokendefs (str): Path to JSON token definitions.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if securerange is not None:
      args += self._get_secureranges([securerange])
    if type:
      args += ["--type", type]
    if tokens:
      args += self._get_token_names(tokens)
    if tokengroup:
      args += ["--tokengroup", tokengroup]
    if tokendefs:
      args += ["--tokendefs", tokendefs]
    return self._run("tokens", "erase", *args).output

  def read(self,
           filenames: list[str] | None = None,
           outfile: str | None = None,
           showoverrides: bool = False,
           tokens: list[str] = [],
           securerange: tuple[int | str, int | str] | None = None,
           tokengroup: str | None = None,
           tokendefs: str | None = None,
           range: tuple[int | str, int | str] | None = None,
           type: str | None = None,
           includeall: bool = False,
           address: int | None = None,
           **kwargs: Any) -> dict:
    """Read tokens from device or from file(s).

    Args:
      filenames (list[str]): Input file(s); if given, read from files instead of device.
      outfile (str): Output file; if not given, printed to stdout.
      showoverrides (bool): Show NVM3 overrides (static tokens only).
      tokens (list[str]): Limit output to these token names.
      securerange (tuple[int | str, int | str]): Range for static secure tokens.
      tokengroup (str): common, zigbee, or znet.
      tokendefs (str): Path to JSON token definitions.
      range (tuple[int | str, int | str]): NVM3 area range (start, end).
      type (str): secure or device (static tokens only).
      includeall (bool): Show all tokens in group (static only).
      address (int): Memory address.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if filenames:
      args = list(filenames) + args
    if outfile:
      args += ["--outfile", outfile]
    if tokens:
      args += self._get_token_names(tokens)
    if tokengroup:
      args += ["--tokengroup", tokengroup]
    if tokendefs:
      args += ["--tokendefs", tokendefs]
    if range is not None:
      args += self._get_ranges([range])
    if showoverrides:
      args += ["--showoverrides"]
    if securerange is not None:
      args += self._get_secureranges([securerange])
    if type:
      args += ["--type", type]
    if includeall:
      args += ["--includeall"]
    if address is not None:
      args += ["--address", self._get_address_string(address)]
    return self._run("tokens", "read", *filenames, *args).output

  def write(self,
            tokenfiles: list[str] = [],
            tokens: list[tuple[str, str]] = [],
            tokengroup: str | None = None,
            tokendefs: str | None = None,
            securerange: tuple[int | str, int | str] | None = None,
            **kwargs: Any) -> dict:
    """Write tokens to device.

    Args:
      tokenfiles (list[str]): Files describing tokens to write.
      tokens (list[tuple[str, str]]): Token overrides as (TOKEN_NAME, value (hex string)).
      tokengroup (str): common, zigbee, or znet.
      tokendefs (str): Path to JSON token definitions.
      securerange (tuple[int | str, int | str]): Range for secure tokens.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if tokenfiles:
      args += self._get_tokenfiles(tokenfiles)
    if tokens:
      args += self._get_tokens(tokens)
    if tokengroup:
      args += ["--tokengroup", tokengroup]
    if tokendefs:
      args += ["--tokendefs", tokendefs]
    if securerange is not None:
      args += self._get_secureranges([securerange])
    return self._run("tokens", "write", *args).output
