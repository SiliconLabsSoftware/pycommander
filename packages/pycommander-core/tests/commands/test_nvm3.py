import unittest

from tests.mock_commander import MockCommander


class TestNvm3(unittest.TestCase):
  def test_nvm3_delete_command(self):
    commander = MockCommander()
    commander.nvm3.delete("in.nvm3", "out.nvm3", object_keys=["key1"], delete_all=True, address=0x08000000)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "nvm3", "delete", "in.nvm3",
      "--key", "key1", "--all", "--address", "0x08000000", "--outfile", "out.nvm3",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_nvm3_deletedevice_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.nvm3.deletedevice(object_keys=["k1"], range=(0x0, 0x1000))
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "nvm3", "deletedevice",
      "--serialno", "123456789", "--key", "k1", "--range", "0x00000000:0x00001000",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_nvm3_dump_command(self):
    commander = MockCommander()
    commander.nvm3.dump("out.nvm3", range=(0x0, 0x2000))
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "nvm3", "dump", "--outfile", "out.nvm3", "--range", "0x00000000:0x00002000", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_nvm3_initfile_command(self):
    commander = MockCommander()
    commander.nvm3.initfile("out.nvm3", 4096, "EFR32MG12", address=0x08000000)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "nvm3", "initfile",
      "--outfile", "out.nvm3", "--size", "4096", "--device", "EFR32MG12", "--address", "0x08000000",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_nvm3_parse_command(self):
    commander = MockCommander()
    commander.nvm3.parse("f.nvm3", object_keys=["k1"], nvm3file="out.nvm3", address=0x08000000)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "nvm3", "parse", "f.nvm3",
      "--key", "k1", "--nvm3file", "out.nvm3", "--address", "0x08000000",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_nvm3_readdevice_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.nvm3.readdevice(object_keys=["k1"], nvm3file="out.nvm3", range=(0x0, 0x1000))
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "nvm3", "readdevice",
      "--serialno", "123456789", "--key", "k1", "--nvm3file", "out.nvm3", "--range", "0x00000000:0x00001000",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_nvm3_set_command(self):
    commander = MockCommander()
    commander.nvm3.set("in.nvm3", "out.nvm3", objects=[(0x12, b"data1")], counters=[(0x56789, 123)], nvm3file="data.nvm3")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "nvm3", "set", "in.nvm3",
      "--outfile", "out.nvm3", "--object", "0x00012:6461746131", "--counter", "0x56789:123", "--nvm3file", "data.nvm3",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_nvm3_writedevice_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.nvm3.writedevice(range=(0x0, 0x1000), objects=[(0x12, b"data1")], counters=[(0x56789, 123)], nvm3file="d.nvm3")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "nvm3", "writedevice",
      "--serialno", "123456789",
      "--range", "0x00000000:0x00001000", "--object", "0x00012:6461746131", "--counter", "0x56789:123", "--nvm3file", "d.nvm3",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)
