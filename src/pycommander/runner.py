import sys
import subprocess
import json

from collections import namedtuple
from pathlib import Path

from .errors import PyCommanderError, PyCommanderInputError, PyCommanderRuntimeError

RunnerResult = namedtuple("RunnerResult", ["returncode", "output"])

class Runner:
  def __init__(self, executable: Path, timeout_s: int = 60):
    self.executable : Path = executable
    self.timeout_s  : int  = timeout_s

    self.subprocess_flags : int = 0

    if sys.platform == "Windows":
      self.subprocess_flags |= subprocess.CREATE_NO_WINDOW

      # Don't display the Windows GPF dialog if commander crashes
      import ctypes
      SEM_NOGPFAULTERRORBOX = 0x0002 # From MSDN
      ctypes.windll.kernel32.SetErrorMode(SEM_NOGPFAULTERRORBOX)

  def run(self, *args: str) -> RunnerResult:
    try:
      result = subprocess.run(
        [str(self.executable), *args],
        stdout = subprocess.PIPE,
        stderr = subprocess.STDOUT,
        creationflags = self.subprocess_flags,
        timeout = self.timeout_s,
        check = True,
        text = True,
        universal_newlines = True,
      )

      returncode = result.returncode
      output     = result.stdout
      return RunnerResult(returncode, output)

    except subprocess.TimeoutExpired:
      raise TimeoutError("Command timed out")

    except subprocess.CalledProcessError as e:
      json_output = json.loads(e.output)
      error_string = "\n".join(json_output.get("error", ""))
      error_message = f"Command failed with return code {e.returncode}: {error_string}"
      if e.returncode == -1 or e.returncode == 255:
        raise PyCommanderInputError(error_message)
      elif e.returncode == -2 or e.returncode == 254:
        raise PyCommanderRuntimeError(error_message)
      else:
        raise PyCommanderError(error_message)
