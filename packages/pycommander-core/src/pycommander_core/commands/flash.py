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

"""Flash command: write files to target flash."""

from typing import Any

from pycommander_core.commands._base import BaseCommand


class FlashCommand(BaseCommand):
  """Write one or more files to the target flash."""

  def _get_general_args(self, **kwargs: Any) -> list[str]:
    args = self._get_adapter_connection_args()
    args += self._get_debug_args()
    args += super()._get_general_args(**kwargs)
    return args

  def flash(self,
            filenames: list[str] = [],
            address: int | None = None,
            halt: bool = False,
            masserase: bool = False,
            reset: bool = True,
            close: bool = True,
            verify: bool = True,
            patches: list[tuple[int | str, int | str, int | str | None]] = [],
            tokens: list[tuple[str, str]] = [],
            tokenfiles: list[str] = [],
            tokengroup: str | None = None,
            tokendefs: str | None = None,
            binary: bool = False,
            include_sections: list[str] = [],
            exclude_sections: list[str] = [],
            vtor: int | None = None,
            **kwargs: Any) -> dict:
    """Write one or more files to the target flash.

    Args:
      filenames (list[str]): File(s) to flash.
      address (int): Address to flash to; not applicable for hex/s37.
      halt (bool): Leave target halted after flashing (PC/SP from vector table).
      masserase (bool): Mass erase entire main flash before flashing.
      reset (bool): Reset device after flashing (use noreset to skip).
      close (bool): Close code regions after flashing on applicable devices.
      verify (bool): Verify contents written to flash.
      patches (list[tuple[int | str, int | str, int | str | None]]): Patch memory; each entry (address, data[, length (up to 8 bytes)]).
      tokens (list[tuple[str, str]]): Token overrides as (TOKEN_NAME, value).
      tokenfiles (list[str]): Files describing tokens to write.
      tokengroup (str): Token set: common, zigbee, or znet.
      tokendefs (str): Path to JSON file defining token set.
      binary (bool): Treat all files as flat binaries (no GBL/s37/hex parsing).
      include_sections (list[str]): ELF sections to include.
      exclude_sections (list[str]): ELF sections to exclude.
      vtor (int): Vector table address (with --halt or RAM code).

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if address is not None:
      args += ["--address", self._get_address_string(address)]
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
      args += self._get_patches(patches)
    if tokens:
      args += self._get_tokens(tokens)
    if tokenfiles:
      args += self._get_tokenfiles(tokenfiles)
    if tokengroup:
      args += ["--tokengroup", tokengroup]
    if tokendefs:
      args += ["--tokendefs", tokendefs]
    if binary:
      args += ["--binary"]
    if include_sections:
      args += self._get_include_sections(include_sections)
    if exclude_sections:
      args += self._get_exclude_sections(exclude_sections)
    if vtor is not None:
      args += ["--vtor", self._get_address_string(vtor)]
    return self._run("flash", *filenames, *args).output
