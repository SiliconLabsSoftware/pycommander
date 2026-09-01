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

from .commander_base import CommanderBase
from .consolestream import ConsoleStream


class VuartStreamBase(ConsoleStream):
  """High-level read-only interface for VUART captures.

  VUART is available only over IP. The stream yields decoded data from
  the target as it arrives. Incoming data is not required to contain
  line endings.

  Startup commands can be sent once after connect via ``command``; the
  stream itself does not accept further input.
  """

  _STREAM_NAME = "VuartStream"
  _COMMAND = ("vuart", "connect")
  _INCLUDE_CONNECTION_OPTIONS = False
  _INCLUDE_DEBUG_OPTIONS = False

  # Status and error messages are intertwined with the actual data output,
  # so we filter them out.
  _STATUS_LINE_PREFIXES = ConsoleStream._STATUS_LINE_PREFIXES + (
    "Connection established!",
    "Attempting to connect to IP",
    "Socket was disconnected.",
    "Connection terminated by user.",
    "Timeout: No data received",
  )

  def __init__(self,
               commander: CommanderBase,
               ip_address: str,
               timeout_s: float | None = None,
               endmarker: str | None = None,
               lineending: str | None = None,
               command: str | list[str] | None = None):
    if not ip_address:
      raise ValueError("ip_address is required")

    super().__init__(commander)
    self._args += [ip_address]

    if timeout_s:
      self._args += ["--timeout", str(timeout_s)]
    if endmarker:
      self._args += ["--endmarker", endmarker]
    if lineending:
      self._args += ["--lineending", lineending]
    if command is not None:
      commands = [command] if isinstance(command, str) else list(command)
      for item in commands:
        self._args += ["--command", item]
