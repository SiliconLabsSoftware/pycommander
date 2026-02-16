import subprocess

from pathlib import Path

from ._ensure_commander import ensure_commander
from ._version import __version__

class PyCommanderCLI:
  def __init__(self, cli: bool, executable_path: Path):
    self.executable_path = executable_path
    self.version = __version__
    self.cli = cli

    ensure_commander(cli=cli)

  def run(self, *args: str) -> int:
    if "-v" in args or "--version" in args:
      print(f"PyCommander ({'CLI' if self.cli else 'GUI'}) {self.version}")

    try:
      result = subprocess.run([self.executable_path, *args])
      return result.returncode
    except KeyboardInterrupt:
      return 128 + 2 # 128 + SIGINT
