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

"""Writemem command: write to target memory."""

from typing import Any

from pycommander_core.commands._base import BaseCommand


class WritememCommand(BaseCommand):
  """Write to target memory."""

  def _get_general_args(self, **kwargs: Any) -> list[str]:
    args = self._get_adapter_connection_args()
    args += self._get_debug_args()
    args += super()._get_general_args(**kwargs)
    return args

  def writemem(self,
               filename: str | None = None,
               address: int | None = None,
               halt: bool = False,
               patches: list[tuple[int | str, int | str, int | str | None]] = [],
               binary: bool = False,
               **kwargs: Any) -> dict:
    """Write one file, or one or more patches, to target memory.

    Args:
      filename (str): File to write. Omit when writing only via patches.
      address (int): Address to write to; not applicable for hex/s37.
      halt (bool): Leave the target halted after writing.
      patches (list[tuple[int | str, int | str, int | str | None]]): Patch memory; each entry (address, data[, length (up to 8 bytes)]).
      binary (bool): Treat the file as a flat binary (no s37/hex parsing). Requires address.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if filename:
      args = [filename] + args
    if address is not None:
      args += ["--address", self._get_address_string(address)]
    if halt:
      args += ["--halt"]
    if patches:
      args += self._get_patches(patches)
    if binary:
      args += ["--binary"]
    return self._run("writemem", *args).output
