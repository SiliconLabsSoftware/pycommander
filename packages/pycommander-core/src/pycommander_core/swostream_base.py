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


class SwoStreamBase:
  """High-level interface for continuous SWO (Serial Wire Output) captures.

  SWO is available on adapters that expose a debug connection (Silicon Labs
  adapters and generic J-Link probes). The stream yields decoded data
  from the target as it arrives, or hexadecimal strings when ``hex_output``
  is enabled.
  """

  # Status and error messages are intertwined with the actual data output,
  # so we filter them out.
  _STATUS_LINE_PREFIXES = (
    "CTRL+C entered, terminating SWO connection",
    "SWO connection terminated.",
    "Timeout: No SWO output",
    "End marker '",
    "SWO capture resumed.",
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
               swospeed_hz: int | None = None,
               timeout_s: float | None = None,
               endmarker: str | None = None,
               hex_output: bool = False,
               noreset: bool = False,
               channel: int | None = None,
               monitorall: bool = False):

    self._commander : CommanderBase = commander
    self._runner : Runner = self._commander._runner
    self._process : subprocess.Popen | None = None

    self._args : list[str] = [
      "swo", "read"
    ]

    self._args += self._commander._get_serial_number_option()
    self._args += self._commander._get_ip_address_option()
    self._args += self._commander._get_serial_port_option()
    self._args += self._commander._get_device_option()
    self._args += self._commander._get_debug_speed_option()
    self._args += self._commander._get_debug_tif_option()
    self._args += self._commander._get_debug_irpre_option()
    self._args += self._commander._get_debug_drpre_option()

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

  def open(self) -> None:
    """
    Open the SwoStream. This will start the underlying SWO capture process.
    """
    if not self._process:
      self._process : subprocess.Popen = self._runner.open(*self._args)
    else:
      raise RuntimeError("SwoStream was already opened. Call close() first, or, ideally, use the context manager syntax.")

  def close(self) -> None:
    """
    Close the SwoStream. This will gracefully stop the underlying SWO capture process.
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
      raise RuntimeError("SwoStream not open. Call open() first, or, ideally, use the context manager syntax.")

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
