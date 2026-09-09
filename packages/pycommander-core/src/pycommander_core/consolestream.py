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

import queue
import subprocess
import threading
from abc import ABC

from .commander_base import CommanderBase
from .consoleoutfile import ConsoleOutfile
from .runner import Runner


class ConsoleStream(ABC):
  """Common base for read-only Commander console streams (SWO, RTT, VCOM, VUART, ...).

  Subclasses set ``_STREAM_NAME`` and ``_COMMAND``, then append
  command-specific options after ``super().__init__()``.

  Device bytes are written to a dedicated ``--outfile`` sink. Commander
  status stays on stdout; ``ERROR:`` lines raise ``RuntimeError``.
  """

  _STREAM_NAME = "ConsoleStream"
  _COMMAND : tuple[str, ...] = ()
  _INCLUDE_CONNECTION_OPTIONS = True
  _INCLUDE_DEBUG_OPTIONS = True

  _ERROR_LINE_PREFIXES = (
    "ERROR:",
  )

  def __init__(self, commander: CommanderBase):
    self._commander : CommanderBase = commander
    self._runner : Runner = self._commander._runner
    self._process : subprocess.Popen | None = None
    self._outfile : ConsoleOutfile | None = None
    self._status_queue : queue.Queue[str] | None = None
    self._status_thread : threading.Thread | None = None

    self._args : list[str] = list(self._COMMAND)

    if self._INCLUDE_CONNECTION_OPTIONS:
      self._args += self._commander._get_serial_number_option()
      self._args += self._commander._get_ip_address_option()
      self._args += self._commander._get_serial_port_option()
      self._args += self._commander._get_device_option()

    if self._INCLUDE_DEBUG_OPTIONS:
      self._args += self._commander._get_debug_speed_option()
      self._args += self._commander._get_debug_tif_option()
      self._args += self._commander._get_debug_irpre_option()
      self._args += self._commander._get_debug_drpre_option()

  def open(self) -> None:
    """
    Open the stream. This will start the underlying Commander capture process.
    """
    if self._process is not None or self._outfile is not None:
      raise RuntimeError(f"{self._STREAM_NAME} was already opened. Call close() first, or, ideally, use the context manager syntax.")

    outfile = ConsoleOutfile.create()
    process = None
    try:
      args = [*self._args, "--outfile", outfile.path]
      process = self._runner.open(*args, pass_fds=outfile.pass_fds)
      outfile.after_spawn()
    except Exception:
      if process is not None:
        self._runner.close(process)
      outfile.close()
      raise

    self._outfile = outfile
    self._process = process
    self._start_status_watcher()

  def close(self) -> None:
    """
    Close the stream. This will gracefully stop the underlying Commander capture process.
    """
    if self._process is not None:
      self._runner.close(self._process)
      self._process = None
    self._join_status_watcher()
    if self._outfile is not None:
      self._outfile.close()
      self._outfile = None

  def _is_error_line(self, line: str) -> bool:
    stripped = line.strip()
    return any(stripped.startswith(prefix) for prefix in self._ERROR_LINE_PREFIXES)

  def _raise_if_error_line(self, line: str) -> None:
    if self._is_error_line(line):
      raise RuntimeError(line.strip())

  def _start_status_watcher(self) -> None:
    stdout = getattr(self._process, "stdout", None)
    if stdout is None:
      return

    self._status_queue = queue.Queue()

    def watch() -> None:
      try:
        while True:
          line = stdout.readline()
          if not line:
            break
          self._status_queue.put(line)
      except Exception:
        pass

    self._status_thread = threading.Thread(target=watch, daemon=True)
    self._status_thread.start()

  def _join_status_watcher(self) -> None:
    if self._status_thread is not None:
      self._status_thread.join(timeout=1.0)
      self._status_thread = None

  def _consume_status(self) -> None:
    if self._status_queue is not None:
      while True:
        try:
          line = self._status_queue.get_nowait()
        except queue.Empty:
          break
        self._raise_if_error_line(line)
      return

    stdout = getattr(self._process, "stdout", None)
    if stdout is None:
      return

    readline = getattr(stdout, "readline", None)
    if readline is None:
      return

    while True:
      line = readline()
      if not line:
        break
      self._raise_if_error_line(line)

  def __iter__(self):
    return self

  def __next__(self) -> str:
    if self._process is None or self._outfile is None:
      raise RuntimeError(f"{self._STREAM_NAME} not open. Call open() first, or, ideally, use the context manager syntax.")

    self._consume_status()
    self._outfile.connect(lambda: not self._runner.isAlive(self._process))
    raw = self._outfile.read(4096)
    if self._status_thread is not None and not raw:
      self._join_status_watcher()
    self._consume_status()
    if not raw:
      raise StopIteration
    return raw.decode("latin-1")

  def __enter__(self):
    self.open()
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    self.close()
