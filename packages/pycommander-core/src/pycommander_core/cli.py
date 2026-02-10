import sys
import subprocess

from .paths import EXECUTABLE_PATH_CLI
from ._ensure_commander import ensure_commander


def main(args: list[str] | None = None) -> int:
  if not ensure_commander():
    return 1

  if args is None:
    args = sys.argv[1:]  # Skip the script name
  else:
    args = args

  try:
    result = subprocess.run([EXECUTABLE_PATH_CLI, *args])
    return result.returncode
  except KeyboardInterrupt:
    return 128 + 2 # 128 + SIGINT


if __name__ == "__main__":
  raise SystemExit(main())
