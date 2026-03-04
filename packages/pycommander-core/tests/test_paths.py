import unittest
import sys

from pathlib import Path

from pycommander_core.paths import EXECUTABLE_PATH_CLI, EXECUTABLE_PATH_GUI

class TestPaths(unittest.TestCase):
  def test_paths_executable_path_cli(self):    
    if sys.platform == "win32":
      self.assertEqual(EXECUTABLE_PATH_CLI, Path("Simplicity Commander CLI/commander-cli.exe"))
    elif sys.platform == "darwin":
      self.assertEqual(EXECUTABLE_PATH_CLI, Path("Commander-cli.app/Contents/MacOS/commander-cli"))
    elif sys.platform == "linux":
      self.assertEqual(EXECUTABLE_PATH_CLI, Path("commander-cli/commander-cli"))
    else:
      self.fail(f"Unsupported platform: {sys.platform}")

  def test_paths_executable_path_gui(self):
    if sys.platform == "win32":
      self.assertEqual(EXECUTABLE_PATH_GUI, Path("Simplicity Commander/commander.exe"))
    elif sys.platform == "darwin":
      self.assertEqual(EXECUTABLE_PATH_GUI, Path("Commander.app/Contents/MacOS/commander"))
    elif sys.platform == "linux":
      self.assertEqual(EXECUTABLE_PATH_GUI, Path("commander/commander"))
    else:
      self.fail(f"Unsupported platform: {sys.platform}")