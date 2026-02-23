import sys

from pycommander_core.cli import PyCommanderCLI
from pycommander_core.paths import EXECUTABLE_PATH_CLI, EXECUTABLE_PATH_GUI

try:
  from pycommander_gui import Commander
  CLI = False

except ImportError:
  try:
    from pycommander_cli import Commander
    CLI = True

  except ImportError:
    raise ImportError(
      "No version of Simplicity Commander is installed.\n\n"
      "Install one of:\n"
      "  pip install silabs-pycommander[cli]\n"
      "  pip install silabs-pycommander[gui]\n"
    )

def main() -> int:
  cli = PyCommanderCLI(cli=CLI, executable_path=EXECUTABLE_PATH_CLI if CLI else EXECUTABLE_PATH_GUI)
  args = sys.argv[1:]  # Skip the script name
  return cli.run(*args)

if __name__ == "__main__":
  raise SystemExit(main())
