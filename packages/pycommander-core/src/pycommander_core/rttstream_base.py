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

import subprocess

from .commander_base import CommanderBase
from .runner import Runner


class RttStreamBase:
  """High-level read-only interface for RTT (Real Time Transfer) captures.

  RTT is available on adapters that expose a debug connection (Silicon Labs
  adapters and generic J-Link probes). The stream yields decoded data from
  the target as it arrives. Incoming data is not required to contain line
  endings.

  Startup commands can be sent once after connect via ``command``; the
  stream itself does not accept further input.
  """

  # Status and error messages are intertwined with the actual data output,
  # so we filter them out.
  _STATUS_LINE_PREFIXES = (
    "RTT successfully initialized.",
    "RTT block address:",
    "RTT status:",
    "Read buffers:",
    "Write buffers:",
    "RTT read buffer",
    "RTT write buffer",
    "RTT console connected",
    "Connection terminated by user.",
    "End marker '",
    "Timeout: No data received",
    "DONE",
  )

  _WARNING_LINE_PREFIXES = (
    "WARNING:",
  )

  _ERROR_LINE_PREFIXES = (
    "ERROR:",
  )

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

    self._commander : CommanderBase = commander
    self._runner : Runner = self._commander._runner
    self._process : subprocess.Popen | None = None

    self._args : list[str] = [
      "rtt", "connect"
    ]

    self._args += self._commander._get_serial_number_option()
    self._args += self._commander._get_ip_address_option()
    self._args += self._commander._get_serial_port_option()
    self._args += self._commander._get_device_option()
    self._args += self._commander._get_debug_speed_option()
    self._args += self._commander._get_debug_tif_option()
    self._args += self._commander._get_debug_irpre_option()
    self._args += self._commander._get_debug_drpre_option()

    if timeout_s:
      self._args += ["--timeout", str(timeout_s)]
    if endmarker:
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
    if lineending:
      self._args += ["--lineending", lineending]
    if command is not None:
      commands = [command] if isinstance(command, str) else list(command)
      for item in commands:
        self._args += ["--command", item]

  def open(self) -> None:
    """
    Open the RttStream. This will start the underlying RTT capture process.
    """
    if not self._process:
      self._process : subprocess.Popen = self._runner.open(*self._args)
    else:
      raise RuntimeError("RttStream was already opened. Call close() first, or, ideally, use the context manager syntax.")

  def close(self) -> None:
    """
    Close the RttStream. This will gracefully stop the underlying RTT capture process.
    """
    if self._process:
      self._runner.close(self._process)
      self._process = None

  def __is_status_line(self, line: str) -> bool:
    stripped = line.strip()
    if not stripped:
      return True
    return any(stripped.startswith(prefix) for prefix in self._STATUS_LINE_PREFIXES)

  def __is_warning_line(self, line: str) -> bool:
    stripped = line.strip()
    return any(stripped.startswith(prefix) for prefix in self._WARNING_LINE_PREFIXES)

  def __is_error_line(self, line: str) -> bool:
    stripped = line.strip()
    return any(stripped.startswith(prefix) for prefix in self._ERROR_LINE_PREFIXES)

  def __filter_commander_messages(self, text: str) -> str:
    output = []
    for part in text.splitlines(keepends=True):
      complete = part.endswith(("\n", "\r"))
      body = part.rstrip("\r\n") if complete else part
      if self.__is_error_line(body):
        raise RuntimeError(body.strip())
      if complete and (self.__is_status_line(body) or self.__is_warning_line(body)):
        continue
      output.append(part)
    return "".join(output)

  def __iter__(self):
    return self

  def __next__(self) -> str:
    if not self._process:
      raise RuntimeError("RttStream not open. Call open() first, or, ideally, use the context manager syntax.")

    while True:
      raw = self._process.stdout.buffer.read1(4096)
      if not raw:
        if self._runner.isAlive(self._process):
          # Wait for more data
          continue
        else:
          # We're done
          raise StopIteration

      payload = self.__filter_commander_messages(raw.decode("latin-1"))
      if payload:
        return payload

  def __enter__(self):
    self.open()
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    self.close()
