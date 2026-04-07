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

from pathlib import Path

from ._ensure_commander import ensure_commander
from ._version import __version__

class PyCommanderCLI:
  def __init__(self, cli: bool, executable_path: Path | None = None):
    if executable_path:
      if not executable_path.exists():
        raise FileNotFoundError(f"Executable not found: {executable_path}")
      self._executable_path = Path(executable_path)
    else:
      self._executable_path = Path(ensure_commander(cli=cli))
    self._cli = cli

    self.version = __version__

  def run(self, *args: str) -> int:
    if "-v" in args or "--version" in args:
      print(f"PyCommander ({'CLI' if self._cli else 'GUI'}) {self.version}")

    try:
      result = subprocess.run([self._executable_path, *args])
      return result.returncode
    except KeyboardInterrupt:
      return 128 + 2 # 128 + SIGINT
