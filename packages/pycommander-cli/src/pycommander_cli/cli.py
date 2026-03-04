import sys

from pycommander_core.cli import PyCommanderCLI

def main() -> int:
  cli = PyCommanderCLI(cli=True)
  args = sys.argv[1:]  # Skip the script name
  return cli.run(*args)


if __name__ == "__main__":
  raise SystemExit(main())
