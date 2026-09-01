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


class VcomStreamBase(ConsoleStream):
  """High-level read-only interface for VCOM (Virtual COM port) captures.

  VCOM is available on Silicon Labs adapters that expose a serial VCOM
  port. The stream yields decoded data from the target as it arrives, or
  hexadecimal strings when ``hex_output`` is enabled. Incoming data is
  not required to contain line endings.

  Startup commands can be sent once after connect via ``command``; the
  stream itself does not accept further input. Adapter VCOM baudrate and
  handshake are configured separately (for example via
  ``commander.vcom.config``).
  """

  _STREAM_NAME = "VcomStream"
  _COMMAND = ("vcom", "connect")
  _INCLUDE_DEBUG_OPTIONS = False

  # Status and error messages are intertwined with the actual data output,
  # so we filter them out.
  _STATUS_LINE_PREFIXES = ConsoleStream._STATUS_LINE_PREFIXES + (
    "Connection established!",
    "Attempting to connect to IP",
    "Opening serial port",
    "Socket was disconnected.",
    "Serial port was disconnected.",
    "Connection terminated by user.",
    "Target restarted in ISP mode.",
  )

  def __init__(self,
               commander: CommanderBase,
               hex_output: bool = False,
               restartinisp: bool = False,
               lineending: str | None = None,
               command: str | list[str] | None = None):
    super().__init__(commander)

    if hex_output:
      self._args += ["--hex"]
    if restartinisp:
      self._args += ["--restartinisp"]
    if lineending:
      self._args += ["--lineending", lineending]
    if command is not None:
      commands = [command] if isinstance(command, str) else list(command)
      for item in commands:
        self._args += ["--command", item]
