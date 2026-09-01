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


class SwoStreamBase(ConsoleStream):
  """High-level interface for continuous SWO (Serial Wire Output) captures.

  SWO is available on adapters that expose a debug connection (Silicon Labs
  adapters and generic J-Link probes). The stream yields decoded data
  from the target as it arrives, or hexadecimal strings when ``hex_output``
  is enabled.
  """

  _STREAM_NAME = "SwoStream"
  _COMMAND = ("swo", "read")

  # Status and error messages are intertwined with the actual data output,
  # so we filter them out.
  _STATUS_LINE_PREFIXES = ConsoleStream._STATUS_LINE_PREFIXES + (
    "CTRL+C entered, terminating SWO connection",
    "SWO connection terminated.",
    "Timeout: No SWO output",
    "SWO capture resumed.",
  )

  def __init__(self,
               commander: CommanderBase,
               swospeed_hz: int | None = None,
               timeout_s: float | None = None,
               endmarker: str | None = None,
               hex_output: bool = False,
               noreset: bool = False,
               channel: int | None = None,
               monitorall: bool = False):
    super().__init__(commander)

    if swospeed_hz:
      self._args += ["--swospeed", str(swospeed_hz)]
    if timeout_s:
      self._args += ["--timeout", str(timeout_s)]
    if endmarker:
      self._args += ["--endmarker", endmarker]
    if hex_output:
      self._args += ["--hex"]
    if noreset:
      self._args += ["--noreset"]
    if channel is not None:
      self._args += ["--channel", str(channel)]
    if monitorall:
      self._args += ["--monitorall"]
