import sys
import subprocess
import datetime

from collections import namedtuple
from pathlib import Path

from .errors import PyCommanderError, PyCommanderInputError, PyCommanderRuntimeError

RunnerResult = namedtuple("RunnerResult", ["returncode", "output"])

class Runner:
  def __init__(self, executable: Path, log_file_path: Path | None = None, timeout_s: int = 300):

    self._subprocess_kwargs = {
      "stdout": subprocess.PIPE,
      "stderr": subprocess.STDOUT,
      "timeout": timeout_s,
      "text": True,
    }

    self._executable       : str = str(executable)
    self._log_file_path    : Path | None = log_file_path

    if sys.platform == "win32":
      self._subprocess_kwargs["creationflags"] = self._subprocess_kwargs.get("creationflags", 0) | subprocess.CREATE_NO_WINDOW

      # Don't display the Windows GPF dialog if commander crashes
      import ctypes
      SEM_NOGPFAULTERRORBOX = 0x0002 # From MSDN
      ctypes.windll.kernel32.SetErrorMode(SEM_NOGPFAULTERRORBOX)

    if not Path(self._executable).exists():
      raise FileNotFoundError(f"Commander executable not found: {self._executable}")

    if not Path(self._executable).is_file():
      raise ValueError(f"Commander executable is not a file: {self._executable}")

  def run(self, *args: str, json_format: bool = True) -> RunnerResult:
    # Run the command (synchronous)
    run_kwargs = {
      "check": True,
      **self._subprocess_kwargs,
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

  def _write_log_file(self, entry: str) -> None:
    if self._log_file_path is None:
      return

    try: 
      timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
      with open(self._log_file_path, "a") as f:
        f.write(f"[{timestamp}] {entry}\n")
    except Exception as e:
      raise Exception(f"Error writing log file {self._log_file_path}: {e}")
