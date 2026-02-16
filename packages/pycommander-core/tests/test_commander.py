import unittest

from .mock_commander import MockCommander
from pycommander_core.commander_base import CommanderResult

class TestCommander(unittest.TestCase):
  
  def test_commander_getVersion(self):
    commander = MockCommander()
    self.assertEqual(commander.getVersion(), "0.0.0")
    self.assertEqual(commander._runner.logged_commands, [["mock", "--version", "--json"]])

  def test_commander_runCommand(self):
    commander = MockCommander()
    self.assertEqual(commander.runCommand("command", "arg1", "arg2"), {"result": {}})
    self.assertEqual(commander._runner.logged_commands, [["mock", "command", "arg1", "arg2", "--json"]])
    commander._runner.logged_commands.clear()

    self.assertEqual(commander.runCommand("command", "", "arg2"), {"result": {}})
    self.assertEqual(commander._runner.logged_commands, [["mock", "command", "arg2", "--json"]])
    commander._runner.logged_commands.clear()

    self.assertEqual(commander.runCommand("command", "arg1", None, "arg3"), {"result": {}})
    self.assertEqual(commander._runner.logged_commands, [["mock", "command", "arg1", "arg3", "--json"]])
    commander._runner.logged_commands.clear()

    self.assertEqual(commander.runCommand("command", "arg1", "arg2", json_formatted_output=False), CommanderResult(0, ""))
    self.assertEqual(commander._runner.logged_commands, [["mock", "command", "arg1", "arg2"]])
    commander._runner.logged_commands.clear()

    self.assertEqual(commander.runCommand("command", "arg1", "arg2", json_formatted_output=True), {"result": {}})
    self.assertEqual(commander._runner.logged_commands, [["mock", "command", "arg1", "arg2", "--json"]])
    commander._runner.logged_commands.clear()
