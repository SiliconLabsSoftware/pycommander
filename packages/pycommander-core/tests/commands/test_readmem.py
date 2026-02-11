import unittest

from tests.mock_commander import MockCommander


class TestReadmem(unittest.TestCase):
  def test_readmem_minimal(self):
    commander = MockCommander(serial_number="123456789")
    commander.readmem.readmem()
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "readmem", "--serialno", "123456789", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_readmem_with_options(self):
    commander = MockCommander(serial_number="123456789")
    commander.readmem.readmem(
      outfile="mem.bin",
      ranges=[(0x08000000, 0x08010000)],
      regions=["@main"],
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "readmem",
      "--serialno", "123456789",
      "--outfile", "mem.bin", "--range", "0x08000000:0x08010000", "--region", "@main",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)
