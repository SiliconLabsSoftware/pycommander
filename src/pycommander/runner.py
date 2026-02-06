import sys
import subprocess
import json
import datetime

from collections import namedtuple
from pathlib import Path

from .errors import PyCommanderError, PyCommanderInputError, PyCommanderRuntimeError

RunnerResult = namedtuple("RunnerResult", ["returncode", "output"])

class Runner:
  def __init__(self, executable: Path, log_file_path: Path | None = None, timeout_s: int = 300):

    self._executable       : Path = executable
    self._log_file_path    : Path | None = log_file_path
    self._timeout_s        : int  = timeout_s

    self._subprocess_flags : int = 0

    if sys.platform == "Windows":
      self._subprocess_flags |= subprocess.CREATE_NO_WINDOW

      # Don't display the Windows GPF dialog if commander crashes
      import ctypes
      SEM_NOGPFAULTERRORBOX = 0x0002 # From MSDN
      ctypes.windll.kernel32.SetErrorMode(SEM_NOGPFAULTERRORBOX)

  def run(self, *args: str) -> RunnerResult:
    if not self._executable.exists():
      raise FileNotFoundError(f"Commander executable not found: {self._executable}")

    if not self._executable.is_file():
      raise FileNotFoundError(f"Commander executable is not a file: {self._executable}")

    json_formatted_output : bool = "--json" in args

    try:
      self._write_log_file(f"{self._executable} {' '.join(args)}")

      result = subprocess.run(
        [str(self._executable), *args],
        stdout = subprocess.PIPE,
        stderr = subprocess.STDOUT,
        creationflags = self._subprocess_flags,
        timeout = self._timeout_s,
        check = True,
        text = True,
        universal_newlines = True,
      )

      returncode = result.returncode
      output     = result.stdout
      return RunnerResult(returncode, output)

    except subprocess.TimeoutExpired as e:
      self._write_log_file(f"Command timed out: {e.cmd} {e.timeout}s")
      raise TimeoutError(f"Command timed out: {e.cmd} {e.timeout}s")

    except subprocess.CalledProcessError as e:
      self._write_log_file(f"Command failed with return code {e.returncode}: {e.output}")
      if json_formatted_output:
        command_output = json.loads(e.output)
        error_string = "\n".join(command_output.get("error", ""))
      
      else:
        command_output = e.output
        error_string = "\n".join([line for line in command_output.split("\n") if line.startswith("ERROR:")])
      
      error_message = f"Command failed with return code {e.returncode}: {error_string}"
      if e.returncode == -1 or e.returncode == 255:
        raise PyCommanderInputError(error_message)
      elif e.returncode == -2 or e.returncode == 254:
        raise PyCommanderRuntimeError(error_message)
      else:
        raise PyCommanderError(error_message)

  def _write_log_file(self, entry: str) -> None:
    if self._log_file_path is None:
      return

    try: 
      timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
      with open(self._log_file_path, "a") as f:
        f.write(f"[{timestamp}] {entry}\n")
    except Exception as e:
      print(f"Error writing log file: {e}")
