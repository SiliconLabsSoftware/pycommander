import unittest

from tests.mock_commander import MockCommander


class TestExtflash(unittest.TestCase):
  def test_extflash_erase_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.extflash.erase(ranges=[(0x0, 0x10000)], board_id="brd123", verify=False)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "extflash", "erase",
      "--serialno", "123456789",
      "--range", "0x00000000:0x00010000", "--board-id", "brd123", "--noverify",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_extflash_read_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.extflash.read(outfile="out.bin", ranges=[(0x0, 0x8000)], board_id="brd1")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "extflash", "read",
      "--serialno", "123456789",
      "--outfile", "out.bin", "--range", "0x00000000:0x00008000", "--board-id", "brd1",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_extflash_write_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.extflash.write("data.bin", address=0x1000, board_id="brd1", verify=False)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "extflash", "write", "data.bin",
      "--serialno", "123456789",
      "--address", "0x00001000", "--board-id", "brd1", "--noverify",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)
