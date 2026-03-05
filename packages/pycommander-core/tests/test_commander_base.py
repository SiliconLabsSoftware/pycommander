import unittest
import shutil

from pathlib import Path

from .mock_commander import MockCommander

from pycommander_core.commander_base import CommanderBase, CommanderResult
from pycommander_core.types import CommanderVersionInfo
from pycommander_core.runner import RunnerResult

class TestCommanderBase(unittest.TestCase):

  def test_commander_base_executable_path_and_cli_true(self):
    command = shutil.which("echo")
    if command is None:
      self.fail("echo command not found")
    commander = CommanderBase(executable_path=Path(command), cli=True)
    self.assertEqual(commander._executable_path, Path(command))

  def test_commander_base_executable_path_and_cli_false(self):
    command = shutil.which("echo")
    if command is None:
      self.fail("echo command not found")
    commander = CommanderBase(executable_path=Path(command), cli=False)
    self.assertEqual(commander._executable_path, Path(command))

  def test_commander_base_nonstring_executable_path(self):
    command = shutil.which("echo")
    if command is None:
      self.fail("echo command not found")
    commander = CommanderBase(executable_path=str(Path(command)))
    self.assertEqual(commander._executable_path, Path(command))

  def test_commander_base_nonexistent_executable_path(self):
    with self.assertRaisesRegex(FileNotFoundError, f"Executable not found: {str(Path('mock'))}"):
      CommanderBase(executable_path=Path("mock"))

  def test_commander_base_no_executable_path_and_missing_cli(self):
    with self.assertRaisesRegex(ValueError, "cli must be provided if executable_path is not provided"):
      CommanderBase(cli=None)

  def test_commander_base_getVersion(self):
    commander = MockCommander()

    commander._runner.queue_result(RunnerResult(0, 
"""
{
  "result": {
    "version": {
      "emdll_version": "7v8p9b1011",
      "jlink_dll_version": "8.94",
      "mbed_tls_version": "0.0.0",
      "qt_version": "5.15.2",
      "simplicity_commander_version": "1v2p3b456"
    }
  },
  "success": true
}
"""
    ))

    expected_version_info = CommanderVersionInfo(
      simplicity_commander_version="1v2p3b456",
      jlink_dll_version="8.94",
      emdll_version="7v8p9b1011",
      mbed_tls_version="0.0.0",
      qt_version="5.15.2",
    )

    self.assertEqual(commander.getVersion(), expected_version_info)
    self.assertEqual(commander._runner.logged_commands, [["mock", "--version", "--json"]])

  def test_commander_base_getVersion_failed(self):
    commander = MockCommander()
    commander._runner.queue_result(RunnerResult(1, ""))
    self.assertEqual(commander.getVersion(), None)
    self.assertEqual(commander._runner.logged_commands, [["mock", "--version", "--json"]])

  def test_commander_base_getVersion_missing_result(self):
    commander = MockCommander()
    commander._runner.queue_result(RunnerResult(0, '{"success": true}'))
    self.assertEqual(commander.getVersion(), None)
    self.assertEqual(commander._runner.logged_commands, [["mock", "--version", "--json"]])

  def test_commander_base_getVersion_missing_version(self):
    commander = MockCommander()
    commander._runner.queue_result(RunnerResult(0, '{"result": ""}'))
    self.assertEqual(commander.getVersion(), None)
    self.assertEqual(commander._runner.logged_commands, [["mock", "--version", "--json"]])

  def test_commander_base_runCommand(self):
    commander = MockCommander()
    self.assertEqual(commander.runCommand("command", "arg1", "arg2"), {"result": {}})
    self.assertEqual(commander._runner.logged_commands, [["mock", "command", "arg1", "arg2", "--json"]])

  def test_commander_base_runCommand_empty_args(self):
    commander = MockCommander()
    self.assertEqual(commander.runCommand("command", "", "arg2"), {"result": {}})
    self.assertEqual(commander._runner.logged_commands, [["mock", "command", "arg2", "--json"]])

  def test_commander_base_runCommand_none_args(self):
    commander = MockCommander()
    self.assertEqual(commander.runCommand("command", "arg1", None, "arg3"), {"result": {}})
    self.assertEqual(commander._runner.logged_commands, [["mock", "command", "arg1", "arg3", "--json"]])

  def test_commander_base_runCommand_whitespace_args(self):
    commander = MockCommander()
    self.assertEqual(commander.runCommand("command", "arg 1", "arg 2"), {"result": {}})
    self.assertEqual(commander._runner.logged_commands, [["mock", "command", "arg 1", "arg 2", "--json"]])

  def test_commander_base_runCommand_json_formatted_output_false(self):
    commander = MockCommander()
    self.assertEqual(commander.runCommand("command", "arg1", "arg2", json_formatted_output=False), CommanderResult(0, ""))
    self.assertEqual(commander._runner.logged_commands, [["mock", "command", "arg1", "arg2"]])

  def test_commander_base_runCommand_json_formatted_output_true(self):
    commander = MockCommander()
    self.assertEqual(commander.runCommand("command", "arg1", "arg2", json_formatted_output=True), {"result": {}})
    self.assertEqual(commander._runner.logged_commands, [["mock", "command", "arg1", "arg2", "--json"]])
    commander._runner.logged_commands.clear()
