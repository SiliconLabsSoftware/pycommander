import sys

from pycommander_core.cli import PyCommanderCLI
from pycommander_core.paths import EXECUTABLE_PATH_CLI

def main() -> int:
  cli = PyCommanderCLI(cli=True, executable_path=EXECUTABLE_PATH_CLI)
  args = sys.argv[1:]  # Skip the script name
  return cli.run(*args)


if __name__ == "__main__":
  raise SystemExit(main())
