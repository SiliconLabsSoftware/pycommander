import unittest

from ..mock_commander import MockCommander


class TestLittlefs(unittest.TestCase):
  def test_littlefs_add_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.littlefs.add("fs.bin", file_paths=["a.txt"], dir_paths=["dir"], address=0x08000000)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "littlefs", "add",
      "--serialno", "123456789",
      "--address", "0x08000000", "--file", "a.txt", "--dir", "dir", "--outfile", "fs.bin",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_littlefs_add_command_with_device(self):
    commander = MockCommander(serial_number="123456789")
    commander.littlefs.add("fs.bin", file_paths=["a.txt"], address=0x08000000, device="EFR32MG24")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "littlefs", "add",
      "--serialno", "123456789", "--device", "EFR32MG24",
      "--address", "0x08000000", "--file", "a.txt", "--outfile", "fs.bin",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_littlefs_dump_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.littlefs.dump("out.bin", address=0x08000000)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "littlefs", "dump",
      "--serialno", "123456789", "--address", "0x08000000", "--outfile", "out.bin",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_littlefs_extract_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.littlefs.extract(dest_dir="out/", file_paths=["f"], address=0x08000000)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "littlefs", "extract",
      "--serialno", "123456789", "--address", "0x08000000", "--file", "f", "--dest", "out/",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_littlefs_extract_command_with_zip_dirs_range_infile(self):
    commander = MockCommander(serial_number="123456789")
    commander.littlefs.extract(
      zip_dir="archive.zip",
      dir_paths=["mydir"],
      range=(0x08000000, 0x08010000),
      infile="fs.bin",
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "littlefs", "extract",
      "--serialno", "123456789",
      "--range", "0x08000000:0x08010000", "--infile", "fs.bin",
      "--dir", "mydir",
      "--zip", "archive.zip",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_littlefs_info_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.littlefs.info(address=0x08000000)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "littlefs", "info", "--serialno", "123456789", "--address", "0x08000000", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_littlefs_init_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.littlefs.init("fs.bin", "EFR32MG12", size=65536, address=0x08000000)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "littlefs", "init",
      "--serialno", "123456789",
      "--address", "0x08000000", "--size", "65536", "--device", "EFR32MG12", "--outfile", "fs.bin",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_littlefs_init_command_with_range(self):
    commander = MockCommander(serial_number="123456789")
    commander.littlefs.init("fs.bin", "EFR32MG12", range=(0x08000000, 0x08010000))
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "littlefs", "init",
      "--serialno", "123456789",
      "--range", "0x08000000:0x08010000", "--device", "EFR32MG12", "--outfile", "fs.bin",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_littlefs_list_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.littlefs.list_files(address=0x08000000)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "littlefs", "list", "--serialno", "123456789", "--address", "0x08000000", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_littlefs_remove_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.littlefs.remove(file_paths=["a"], dir_paths=["d"], address=0x08000000)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "littlefs", "remove",
      "--serialno", "123456789", "--address", "0x08000000", "--file", "a", "--dir", "d",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)
