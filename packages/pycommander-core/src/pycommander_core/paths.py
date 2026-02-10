import sys

from pathlib import Path

ARCHIVE_DIR         = Path(__file__).parent / "_archive"
PYCOMMANDER_DIR     = Path.home() / ".silabs" / "pycommander"
STAMP_FILE_PATH     = PYCOMMANDER_DIR / ".stamp"
EXECUTABLE_ROOT_DIR = PYCOMMANDER_DIR / "bin"

EXECUTABLE_PATH_CLI = ""
EXECUTABLE_PATH_GUI = ""
if sys.platform == "win32":
  EXECUTABLE_PATH_CLI = EXECUTABLE_ROOT_DIR / "Simplicity Commander CLI" / "commander-cli.exe"
  EXECUTABLE_PATH_GUI = EXECUTABLE_ROOT_DIR / "Simplicity Commander"     / "commander.exe"
elif sys.platform == "darwin":
  EXECUTABLE_PATH_CLI = EXECUTABLE_ROOT_DIR / "Commander-cli.app" / "Contents" / "MacOS" / "commander-cli"
  EXECUTABLE_PATH_GUI = EXECUTABLE_ROOT_DIR / "Commander.app"     / "Contents" / "MacOS" / "commander"
elif sys.platform == "linux":
  EXECUTABLE_PATH_CLI = EXECUTABLE_ROOT_DIR / "commander-cli" / "commander-cli"
  EXECUTABLE_PATH_GUI = EXECUTABLE_ROOT_DIR / "commander"     / "commander"
