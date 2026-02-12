import unittest

from tests.mock_commander import MockCommander


class TestCtune(unittest.TestCase):
  def test_ctune_autoset_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.ctune.autoset()
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "ctune", "autoset", "--serialno", "123456789", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_ctune_get_command(self):
    commander = MockCommander(serial_number="123456789", debug_speed=2000000)
    commander.ctune.get()
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "ctune", "get", "--serialno", "123456789", "--speed", "2000000", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_ctune_set_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.ctune.set("AABBCCDD")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "ctune", "set", "--serialno", "123456789", "--value", "AABBCCDD", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)
