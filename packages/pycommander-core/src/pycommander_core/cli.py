import sys
import subprocess

from pathlib import Path

from .paths import EXECUTABLE_PATH_CLI
from ._ensure_commander import ensure_commander
from ._version import __version__

class PyCommanderCLI:
  def __init__(self, executable_path: Path):
    self.executable_path = executable_path
    self.version = __version__

    ensure_commander()

  def run(self, *args: str) -> int:
    if "-v" in args or "--version" in args:
      print(f"PyCommander {self.version}")

    try:
      result = subprocess.run([self.executable_path, *args])
      return result.returncode
    except KeyboardInterrupt:
      return 128 + 2 # 128 + SIGINT


def main() -> int:
  cli = PyCommanderCLI(EXECUTABLE_PATH_CLI)
  args = sys.argv[1:]  # Skip the script name
  return cli.run(*args)


if __name__ == "__main__":
  raise SystemExit(main())
