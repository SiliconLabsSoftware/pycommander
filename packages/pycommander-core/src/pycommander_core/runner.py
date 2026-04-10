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

import sys
import subprocess
import datetime
import signal

from collections import namedtuple
from pathlib import Path

from .errors import PyCommanderError, PyCommanderInputError, PyCommanderRuntimeError

RunnerResult = namedtuple("RunnerResult", ["returncode", "output"])

class Runner:
  def __init__(self, executable: Path, log_file_path: Path | None = None, timeout_s: int = 300):

    self._common_subprocess_kwargs = {
      "stdout": subprocess.PIPE,
      "stderr": subprocess.STDOUT,
      "text": True,
    }

    self._executable       : str = str(executable)
    self._log_file_path    : Path | None = log_file_path
    self._timeout_s        : int = timeout_s

    if sys.platform == "win32":
      self._common_subprocess_kwargs["creationflags"] = self._common_subprocess_kwargs.get("creationflags", 0) | subprocess.CREATE_NO_WINDOW

      # Don't display the Windows GPF dialog if commander crashes
      import ctypes
      SEM_NOGPFAULTERRORBOX = 0x0002 # From MSDN
      ctypes.windll.kernel32.SetErrorMode(SEM_NOGPFAULTERRORBOX)

    if not Path(self._executable).exists():
      raise FileNotFoundError(f"Commander executable not found: {self._executable}")

    if not Path(self._executable).is_file():
      raise ValueError(f"Commander executable is not a file: {self._executable}")

  def run(self, *args: str, json_format: bool = True) -> RunnerResult:
    """
    Run the command synchronously.

    Args:
      args: Arguments to pass to the command
      json_format: Whether to return the output as JSON

    Returns:
      RunnerResult: The result of the command
    """
    run_kwargs = {
      "check": True,
      "timeout": self._timeout_s,
      **self._common_subprocess_kwargs,
    }

    if json_format:
      args += ("--json",)

    try:
      self._write_log_file(f"{self._executable} {' '.join(args)}")

      result = subprocess.run([str(self._executable), *args], **run_kwargs)

      returncode = result.returncode
      output     = result.stdout
      return RunnerResult(returncode, output)

    except subprocess.TimeoutExpired as e:
      self._write_log_file(f"Command timed out: {e.cmd}")
      raise TimeoutError(f"Command timed out: {e.cmd}")

    except subprocess.CalledProcessError as e:
      self._write_log_file(f"Command failed with return code {e.returncode}: {e.output}")

      if e.returncode == -1 or e.returncode == 255:
        raise PyCommanderInputError(e.output)
      elif e.returncode == -2 or e.returncode == 254:
        raise PyCommanderRuntimeError(e.output)
      else:
        raise PyCommanderError(e.output)

  def open(self, *args: str) -> subprocess.Popen:
    """
    Open the command asynchronously.

    Args:
      args: Arguments to pass to the command

    Returns:
      subprocess.Popen: The subprocess object
    """
    popen_kwargs = {
      **self._common_subprocess_kwargs,
    }

    if sys.platform == "win32":
      popen_kwargs["creationflags"] = popen_kwargs.get("creationflags", 0) | subprocess.CREATE_NEW_PROCESS_GROUP
    else:
      popen_kwargs["start_new_session"] = True

    self._write_log_file(f"{self._executable} {' '.join(args)}")

    return subprocess.Popen([str(self._executable), *args], **popen_kwargs)

  def isAlive(self, process: subprocess.Popen) -> bool:
    return process is not None and process.poll() is None

  def sendCtrlC(self, process: subprocess.Popen) -> None:
    if not self.isAlive(process):
      return

    if sys.platform == "win32":
      process.send_signal(signal.CTRL_BREAK_EVENT)
    else:
      process.send_signal(signal.SIGINT)

  def terminate(self, process: subprocess.Popen) -> None:
    if not self.isAlive(process):
      return

    process.terminate()

  def kill(self, process: subprocess.Popen) -> None:
    if not self.isAlive(process):
      return

    process.kill()

  def wait(self, process: subprocess.Popen, timeout_s: int | None = None) -> int:
    if not self.isAlive(process):
      return process.returncode

    return process.wait(timeout=timeout_s)

  def close(self, process: subprocess.Popen) -> None:
    if not self.isAlive(process):
      return

    # Try exiting gracefully first
    self.sendCtrlC(process)
    try:
      self.wait(process, timeout_s=1)
      return
    except subprocess.TimeoutExpired:
      pass

    # No joy, terminate
    self.terminate(process)
    try:
      self.wait(process, timeout_s=1)
      return
    except subprocess.TimeoutExpired:
      pass

    # No mercy, kill
    self.kill(process)
    self.wait(process)

  def _write_log_file(self, entry: str) -> None:
    if self._log_file_path is None:
      return

    try: 
      timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
      with open(self._log_file_path, "a") as f:
        f.write(f"[{timestamp}] {entry}\n")
    except Exception as e:
      raise Exception(f"Error writing log file {self._log_file_path}: {e}")
