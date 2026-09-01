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
from abc import ABC

from .commander_base import CommanderBase
from .runner import Runner


class ConsoleStream(ABC):
  """Common base for read-only Commander console streams (SWO, RTT, ...).

  Subclasses set ``_STREAM_NAME``, ``_COMMAND``, and any extra status
  prefixes, then append command-specific options after ``super().__init__()``.
  """

  _STREAM_NAME = "ConsoleStream"
  _COMMAND : tuple[str, ...] = ()

  _STATUS_LINE_PREFIXES = (
    "End marker '",
    "DONE",
  )

  _WARNING_LINE_PREFIXES = (
    "WARNING:",
  )

  _ERROR_LINE_PREFIXES = (
    "ERROR:",
  )

  def __init__(self, commander: CommanderBase):
    self._commander : CommanderBase = commander
    self._runner : Runner = self._commander._runner
    self._process : subprocess.Popen | None = None

    self._args : list[str] = list(self._COMMAND)
    self._args += self._commander._get_serial_number_option()
    self._args += self._commander._get_ip_address_option()
    self._args += self._commander._get_serial_port_option()
    self._args += self._commander._get_device_option()
    self._args += self._commander._get_debug_speed_option()
    self._args += self._commander._get_debug_tif_option()
    self._args += self._commander._get_debug_irpre_option()
    self._args += self._commander._get_debug_drpre_option()

  def open(self) -> None:
    """
    Open the stream. This will start the underlying Commander capture process.
    """
    if not self._process:
      self._process : subprocess.Popen = self._runner.open(*self._args)
    else:
      raise RuntimeError(f"{self._STREAM_NAME} was already opened. Call close() first, or, ideally, use the context manager syntax.")

  def close(self) -> None:
    """
    Close the stream. This will gracefully stop the underlying Commander capture process.
    """
    if self._process:
      self._runner.close(self._process)
      self._process = None

  def _is_status_line(self, line: str) -> bool:
    stripped = line.strip()
    if not stripped:
      return True
    return any(stripped.startswith(prefix) for prefix in self._STATUS_LINE_PREFIXES)

  def _is_warning_line(self, line: str) -> bool:
    stripped = line.strip()
    return any(stripped.startswith(prefix) for prefix in self._WARNING_LINE_PREFIXES)

  def _is_error_line(self, line: str) -> bool:
    stripped = line.strip()
    return any(stripped.startswith(prefix) for prefix in self._ERROR_LINE_PREFIXES)

  def _filter_commander_messages(self, text: str) -> str:
    output = []
    for part in text.splitlines(keepends=True):
      complete = part.endswith(("\n", "\r"))
      body = part.rstrip("\r\n") if complete else part
      if self._is_error_line(body):
        raise RuntimeError(body.strip())
      if complete and (self._is_status_line(body) or self._is_warning_line(body)):
        continue
      output.append(part)
    return "".join(output)

  def __iter__(self):
    return self

  def __next__(self) -> str:
    if not self._process:
      raise RuntimeError(f"{self._STREAM_NAME} not open. Call open() first, or, ideally, use the context manager syntax.")

    while True:
      raw = self._process.stdout.buffer.read1(4096)
      if not raw:
        if self._runner.isAlive(self._process):
          # Wait for more data
          continue
        else:
          # We're done
          raise StopIteration

      payload = self._filter_commander_messages(raw.decode("latin-1"))
      if payload:
        return payload

  def __enter__(self):
    self.open()
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    self.close()
