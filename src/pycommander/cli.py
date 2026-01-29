import sys
import subprocess

from .paths import EXECUTABLE_PATH

def main(args: list[str] | None = None) -> int:
  if args is None:
    args = sys.argv[1:]  # Skip the script name
  else:
    args = args

  try:
    result = subprocess.run([EXECUTABLE_PATH, *args])
    return result.returncode
  except KeyboardInterrupt:
    return 0


if __name__ == "__main__":
  from ._ensure_commander import ensure_commander
  if not ensure_commander():
    sys.exit(1)

  sys.exit(main())
