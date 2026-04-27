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

"""Verify command: compare device flash with input files."""

from typing import Any

from pycommander_core.commands._base import BaseCommand


class VerifyCommand(BaseCommand):
  """Compare the contents in the device flash with the given input files and options."""

  def _get_general_args(self, **kwargs: Any) -> list[str]:
    args = self._get_adapter_connection_args()
    args += self._get_debug_args()
    args += super()._get_general_args(**kwargs)
    return args

  def verify(self,
             filenames: list[str] | None = None,
             address: int | None = None,
             patches: list[tuple[int | str, int | str, int | str | None]] = [],
             tokens: list[tuple[str, str]] = [],
             tokenfiles: list[str] = [],
             tokengroup: str | None = None,
             tokendefs: str | None = None,
             blank: bool = False,
             reset: bool = True,
             regions: list[str] = [],
             binary: bool = False,
             **kwargs: Any) -> dict:
    """Compare device flash with given files and options.

    Args:
      filenames (list[str]): File(s) to verify against. Omit with blank=True to check blank.
      address (int): Address for .bin comparison; not for hex/s37.
      patches (list[tuple[int | str, int | str, int | str | None]]): Patch memory; each entry (address, data[, length (up to 8 bytes)]).
      tokens (list[tuple[str, str]]): Token overrides as (TOKEN_NAME, value).
      tokenfiles (list[str]): Files describing tokens.
      tokengroup (str): Token set: common, zigbee, or znet.
      tokendefs (str): Path to JSON token definitions.
      blank (bool): Check that main flash (or regions) is blank; no file.
      reset (bool): Reset device before verifying.
      regions (list[str]): With --blank, regions to check if blank (@region).
      binary (bool): Treat all files as flat binaries.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if filenames:
      args = list(filenames) + args
    if address is not None:
      args += ["--address", self._get_address_string(address)]
    if patches:
      args += self._get_patches(patches)
    if tokens:
      args += self._get_tokens(tokens)
    if tokenfiles:
      args += self._get_tokenfiles(tokenfiles)
    if tokengroup:
      args += ["--tokengroup", tokengroup]
    if tokendefs:
      args += ["--tokendefs", tokendefs]
    if blank:
      args += ["--blank"]
    if not reset:
      args += ["--noreset"]
    if regions:
      args += self._get_regions(regions)
    if binary:
      args += ["--binary"]
    return self._run("verify", *args).output
