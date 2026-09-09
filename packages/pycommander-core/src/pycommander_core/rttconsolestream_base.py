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


class RttConsoleStreamBase(ConsoleStream):
  """High-level read-only interface for RTT (Real Time Transfer) captures.

  RTT is available on adapters that expose a debug connection (Silicon Labs
  adapters and generic J-Link probes). The stream yields decoded data from
  the target as it arrives. Incoming data is not required to contain line
  endings.

  Startup commands can be sent once after connect via ``command``; the
  stream itself does not accept further input.
  """

  _STREAM_NAME = "RttConsoleStream"
  _COMMAND = ("rtt", "connect")

  def __init__(self,
               commander: CommanderBase,
               timeout_s: float | None = None,
               endmarker: str | None = None,
               blockaddress: int | str | None = None,
               readbuffer: int | str | None = None,
               writebuffer: int | str | None = None,
               terminal: int | None = None,
               noreset: bool = False,
               lineending: str | None = None,
               command: str | list[str] | None = None):
    super().__init__(commander)

    if timeout_s is not None:
      self._args += ["--timeout", str(timeout_s)]
    if endmarker is not None:
      self._args += ["--endmarker", endmarker]
    if blockaddress is not None:
      if isinstance(blockaddress, str) and blockaddress.lower().startswith("0x"):
        self._args += ["--blockaddress", blockaddress]
      else:
        self._args += ["--blockaddress", f"0x{int(blockaddress):08X}"]
    if readbuffer is not None:
      self._args += ["--readbuffer", str(readbuffer)]
    if writebuffer is not None:
      self._args += ["--writebuffer", str(writebuffer)]
    if terminal is not None:
      self._args += ["--terminal", str(terminal)]
    if noreset:
      self._args += ["--noreset"]
    if lineending is not None:
      self._args += ["--lineending", lineending]
    if command is not None:
      commands = [command] if isinstance(command, str) else list(command)
      for item in commands:
        self._args += ["--command", item]
