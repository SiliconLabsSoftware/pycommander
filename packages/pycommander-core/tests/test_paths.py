import unittest
import sys

from pathlib import Path

from pycommander_core.paths import ROOT_DIR_CLI, ROOT_DIR_GUI, EXECUTABLE_PATH_CLI, EXECUTABLE_PATH_GUI

class TestPaths(unittest.TestCase):
  def test_paths_executable_path_cli(self):
    executable_relative_to_root = Path(EXECUTABLE_PATH_CLI).relative_to(ROOT_DIR_CLI)
    
    if sys.platform == "win32":
      self.assertEqual(executable_relative_to_root, Path("Simplicity Commander CLI/commander-cli.exe"))
    elif sys.platform == "darwin":
      self.assertEqual(executable_relative_to_root, Path("Commander-cli.app/Contents/MacOS/commander-cli"))
    elif sys.platform == "linux":
      self.assertEqual(executable_relative_to_root, Path("commander-cli/commander-cli"))
    else:
      self.fail(f"Unsupported platform: {sys.platform}")

  def test_paths_executable_path_gui(self):
    executable_relative_to_root = Path(EXECUTABLE_PATH_GUI).relative_to(ROOT_DIR_GUI)
    
    if sys.platform == "win32":
      self.assertEqual(executable_relative_to_root, Path("Simplicity Commander/commander.exe"))
    elif sys.platform == "darwin":
      self.assertEqual(executable_relative_to_root, Path("Commander.app/Contents/MacOS/commander"))
    elif sys.platform == "linux":
      self.assertEqual(executable_relative_to_root, Path("commander/commander"))
    else:
      self.fail(f"Unsupported platform: {sys.platform}")