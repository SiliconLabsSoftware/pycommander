import sys

from pathlib import Path

if sys.platform == "win32":
  EXECUTABLE_PATH_CLI = Path("Simplicity Commander CLI") / "commander-cli.exe"
  EXECUTABLE_PATH_GUI = Path("Simplicity Commander")     / "commander.exe"
elif sys.platform == "darwin":
  EXECUTABLE_PATH_CLI = Path("Commander-cli.app") / "Contents" / "MacOS" / "commander-cli"
  EXECUTABLE_PATH_GUI = Path("Commander.app")     / "Contents" / "MacOS" / "commander"
elif sys.platform == "linux":
  EXECUTABLE_PATH_CLI = Path("commander-cli") / "commander-cli"
  EXECUTABLE_PATH_GUI = Path("commander")     / "commander"
else:
  raise ValueError(f"Unsupported platform: {sys.platform}")
