import sys

from pycommander_core.cli import PyCommanderCLI
from pycommander_core.paths import EXECUTABLE_PATH_GUI

def main() -> int:
  cli = PyCommanderCLI(cli=False, executable_path=EXECUTABLE_PATH_GUI)
  args = sys.argv[1:]  # Skip the script name
  return cli.run(*args)


if __name__ == "__main__":
  raise SystemExit(main())
