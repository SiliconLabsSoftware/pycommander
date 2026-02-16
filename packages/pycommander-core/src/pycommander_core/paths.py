import sys

from pathlib import Path

ARCHIVE_DIR           = Path(__file__).parent / "_archive"
PYCOMMANDER_DIR       = Path.home() / ".silabs" / "pycommander"
ROOT_DIR_CLI          = PYCOMMANDER_DIR / "cli"
ROOT_DIR_GUI          = PYCOMMANDER_DIR / "gui"
VERSION_FILE_PATH_CLI = ROOT_DIR_CLI / ".version"
VERSION_FILE_PATH_GUI = ROOT_DIR_GUI / ".version"
STAMP_FILE_PATH_CLI   = ROOT_DIR_CLI / ".stamp"
STAMP_FILE_PATH_GUI   = ROOT_DIR_GUI / ".stamp"
EXECUTABLE_PATH_CLI   = ""
EXECUTABLE_PATH_GUI   = ""

if sys.platform == "win32":
  EXECUTABLE_PATH_CLI = ROOT_DIR_CLI / "Simplicity Commander CLI" / "commander-cli.exe"
  EXECUTABLE_PATH_GUI = ROOT_DIR_GUI / "Simplicity Commander"     / "commander.exe"
elif sys.platform == "darwin":
  EXECUTABLE_PATH_CLI = ROOT_DIR_CLI / "Commander-cli.app" / "Contents" / "MacOS" / "commander-cli"
  EXECUTABLE_PATH_GUI = ROOT_DIR_GUI / "Commander.app"     / "Contents" / "MacOS" / "commander"
elif sys.platform == "linux":
  EXECUTABLE_PATH_CLI = ROOT_DIR_CLI / "commander-cli" / "commander-cli"
  EXECUTABLE_PATH_GUI = ROOT_DIR_GUI / "commander"     / "commander"
