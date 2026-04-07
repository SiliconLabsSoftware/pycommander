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

"""VCOM commands: configure adapter VCOM settings."""

from typing import Any

from pycommander_core.commands._base import BaseCommand


class VcomCommand(BaseCommand):
  """VCOM commands."""

  def _get_general_args(self, **kwargs: Any) -> list[str]:
    args = []
    args += self._get_adapter_connection_args()
    args += self._get_kwargs(**kwargs)
    return args

  def config(self,
             baudrate: int | None = None,
             handshake: str | None = None,
             store: bool = False,
             **kwargs: Any) -> dict:
    """Configure adapter board VCOM settings.

    Args:
      baudrate (int): VCOM baudrate.
      handshake (str): Handshake: none, rtscts, or aux.
      store (bool): Store adapter board VCOM settings.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if baudrate is not None:
      args += ["--baudrate", str(baudrate)]
    if handshake:
      args += ["--handshake", handshake]
    if store:
      args += ["--store"]
    return self._run("vcom", "config", *args).output
