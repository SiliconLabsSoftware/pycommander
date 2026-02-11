import unittest

from pycommander_core.commands._base import BaseCommand, CommandResult
from tests.mock_commander import MockCommander

class TestBase(unittest.TestCase):

  def test_base_run(self):
    commander = MockCommander()
    base_command = BaseCommand(commander)
    self.assertEqual(base_command._run("command", "arg1", "arg2"), CommandResult(0, {"result": {}}))
    self.assertEqual(commander._runner.logged_commands, [["mock", "command", "arg1", "arg2", "--json"]])
    commander._runner.logged_commands.clear()

    self.assertEqual(base_command._run("command", "", "arg2"), CommandResult(0, {"result": {}}))
    self.assertEqual(commander._runner.logged_commands, [["mock", "command", "arg2", "--json"]])
    commander._runner.logged_commands.clear()

    self.assertEqual(base_command._run("command", "arg1", None, "arg3"), CommandResult(0, {"result": {}}))
    self.assertEqual(commander._runner.logged_commands, [["mock", "command", "arg1", "arg3", "--json"]])
    commander._runner.logged_commands.clear()

  def test_base_get_adapter_connection_args(self):
    commander = MockCommander(serial_number="123456789")
    base_command = BaseCommand(commander)
    self.assertEqual(base_command._get_adapter_connection_args(), ["--serialno", "123456789"])

    commander = MockCommander(ip_address="192.168.1.100")
    base_command = BaseCommand(commander)
    self.assertEqual(base_command._get_adapter_connection_args(), ["--ip", "192.168.1.100"])

    commander = MockCommander(serial_port="/dev/tty.usbmodem141101")
    base_command = BaseCommand(commander)
    self.assertEqual(base_command._get_adapter_connection_args(), ["--identifybyserialport", "/dev/tty.usbmodem141101"])

  def test_base_get_serial_number_option(self):
    commander = MockCommander(serial_number="123456789")
    base_command = BaseCommand(commander)
    self.assertEqual(base_command._get_serial_number_option(), ["--serialno", "123456789"])

    commander = MockCommander(serial_number=None)
    base_command = BaseCommand(commander)
    self.assertEqual(base_command._get_serial_number_option(), [])

    commander = MockCommander(serial_number="")
    base_command = BaseCommand(commander)
    self.assertEqual(base_command._get_serial_number_option(), [])

  def test_base_get_ip_address_option(self):
    commander = MockCommander(ip_address="192.168.1.100")
    base_command = BaseCommand(commander)
    self.assertEqual(base_command._get_ip_address_option(), ["--ip", "192.168.1.100"])

    commander = MockCommander(ip_address=None)
    base_command = BaseCommand(commander)
    self.assertEqual(base_command._get_ip_address_option(), [])

    commander = MockCommander(ip_address="")
    base_command = BaseCommand(commander)
    self.assertEqual(base_command._get_ip_address_option(), [])

  def test_base_get_serial_port_option(self):
    commander = MockCommander(serial_port="/dev/tty.usbmodem141101")
    base_command = BaseCommand(commander)
    self.assertEqual(base_command._get_serial_port_option(), ["--identifybyserialport", "/dev/tty.usbmodem141101"])

    commander = MockCommander(serial_port=None)
    base_command = BaseCommand(commander)
    self.assertEqual(base_command._get_serial_port_option(), [])

    commander = MockCommander(serial_port="")
    base_command = BaseCommand(commander)
    self.assertEqual(base_command._get_serial_port_option(), [])

  def test_base_get_debug_args(self):
    commander = MockCommander(debug_speed=1000000, debug_tif="SWD", debug_irpre=1000000, debug_drpre=1000000)
    base_command = BaseCommand(commander)
    self.assertEqual(base_command._get_debug_args(), ["--speed", "1000000", "--tif", "SWD", "--irpre", "1000000", "--drpre", "1000000"])

  def test_base_get_debug_speed_option(self):
    commander = MockCommander(debug_speed=1000000)
    base_command = BaseCommand(commander)
    self.assertEqual(base_command._get_debug_speed_option(), ["--speed", "1000000"])

    commander = MockCommander(debug_speed=None)
    base_command = BaseCommand(commander)
    self.assertEqual(base_command._get_debug_speed_option(), [])

    commander = MockCommander(debug_speed="")
    base_command = BaseCommand(commander)
    self.assertEqual(base_command._get_debug_speed_option(), [])

  def test_base_get_debug_tif_option(self):
    commander = MockCommander(debug_tif="SWD")
    base_command = BaseCommand(commander)
    self.assertEqual(base_command._get_debug_tif_option(), ["--tif", "SWD"])

    commander = MockCommander(debug_tif=None)
    base_command = BaseCommand(commander)
    self.assertEqual(base_command._get_debug_tif_option(), [])

    commander = MockCommander(debug_tif="")
    base_command = BaseCommand(commander)
    self.assertEqual(base_command._get_debug_tif_option(), [])

  def test_base_get_debug_irpre_option(self):
    commander = MockCommander(debug_irpre=1000000)
    base_command = BaseCommand(commander)
    self.assertEqual(base_command._get_debug_irpre_option(), ["--irpre", "1000000"])

    commander = MockCommander(debug_irpre=None)
    base_command = BaseCommand(commander)
    self.assertEqual(base_command._get_debug_irpre_option(), [])

    commander = MockCommander(debug_irpre="")
    base_command = BaseCommand(commander)
    self.assertEqual(base_command._get_debug_irpre_option(), [])

  def test_base_get_debug_drpre_option(self):
    commander = MockCommander(debug_drpre=1000000)
    base_command = BaseCommand(commander)
    self.assertEqual(base_command._get_debug_drpre_option(), ["--drpre", "1000000"])

    commander = MockCommander(debug_drpre=None)
    base_command = BaseCommand(commander)
    self.assertEqual(base_command._get_debug_drpre_option(), [])

    commander = MockCommander(debug_drpre="")
    base_command = BaseCommand(commander)
    self.assertEqual(base_command._get_debug_drpre_option(), [])

  def test_base_get_kwargs(self):
    base_command = BaseCommand(MockCommander())
    self.assertEqual(base_command._get_kwargs(), [])
    self.assertEqual(base_command._get_kwargs(device="123456789"), ["--device", "123456789"])
    self.assertEqual(base_command._get_kwargs(force=True), ["--force"])
    self.assertEqual(base_command._get_kwargs(device=None), [])
    self.assertEqual(base_command._get_kwargs(force=False), [])
    self.assertEqual(base_command._get_kwargs(device="123456789", force=True), ["--device", "123456789", "--force"])

  def test_base_get_address_string(self):
    base_command = BaseCommand(MockCommander())
    self.assertEqual(base_command._get_address_string(0x12345678), "0x12345678")
    self.assertEqual(base_command._get_address_string(0x0),        "0x00000000")
    self.assertEqual(base_command._get_address_string(0xFFFF),     "0x0000FFFF")
    self.assertEqual(base_command._get_address_string(123456789),  "0x075BCD15")

  def test_base_get_ranges(self):
    base_command = BaseCommand(MockCommander())

    with self.assertRaises(ValueError):
      base_command._get_ranges([(0x12345678)])

    with self.assertRaises(ValueError):
      base_command._get_ranges([(0x12345678, 0x12345679, 0x1234567A)])

    self.assertEqual(base_command._get_ranges([]), [])
    self.assertEqual(base_command._get_ranges([(123456789, 123456790)]), ["--range", "0x075BCD15:0x075BCD16"])
    self.assertEqual(base_command._get_ranges([(0x12345678, 0x12345679)]), ["--range", "0x12345678:0x12345679"])
    self.assertEqual(base_command._get_ranges([(0x0, 0xFFFFFFFF)]), ["--range", "0x00000000:0xFFFFFFFF"])
    self.assertEqual(base_command._get_ranges([(0x12345678, 0x12345679), (0x0, 0xFFFFFFFF)]), ["--range", "0x12345678:0x12345679", "--range", "0x00000000:0xFFFFFFFF"])
    self.assertEqual(base_command._get_ranges([(0x12345678, 0x12345679), (0x0, 0xFFFFFFFF), (123456789, 123456790)]), ["--range", "0x12345678:0x12345679", "--range", "0x00000000:0xFFFFFFFF", "--range", "0x075BCD15:0x075BCD16"])
    self.assertEqual(base_command._get_ranges([("0x12345678", "0x12345679")]), ["--range", "0x12345678:0x12345679"])
    self.assertEqual(base_command._get_ranges([(0x12345678, "+256")]), ["--range", "0x12345678:+256"])

  def test_base_get_secureranges(self):
    base_command = BaseCommand(MockCommander())

    with self.assertRaises(ValueError):
      base_command._get_secureranges([(0x12345678)])

    with self.assertRaises(ValueError):
      base_command._get_secureranges([(0x12345678, 0x12345679, 0x1234567A)])

    self.assertEqual(base_command._get_secureranges([]), [])
    self.assertEqual(base_command._get_secureranges([(123456789, 123456790)]), ["--securerange", "0x075BCD15:0x075BCD16"])
    self.assertEqual(base_command._get_secureranges([(0x12345678, 0x12345679)]), ["--securerange", "0x12345678:0x12345679"])
    self.assertEqual(base_command._get_secureranges([(0x0, 0xFFFFFFFF)]), ["--securerange", "0x00000000:0xFFFFFFFF"])
    self.assertEqual(base_command._get_secureranges([(0x12345678, 0x12345679), (0x0, 0xFFFFFFFF)]), ["--securerange", "0x12345678:0x12345679", "--securerange", "0x00000000:0xFFFFFFFF"])
    self.assertEqual(base_command._get_secureranges([(0x12345678, 0x12345679), (0x0, 0xFFFFFFFF), (123456789, 123456790)]), ["--securerange", "0x12345678:0x12345679", "--securerange", "0x00000000:0xFFFFFFFF", "--securerange", "0x075BCD15:0x075BCD16"])
    self.assertEqual(base_command._get_secureranges([("0x12345678", "0x12345679")]), ["--securerange", "0x12345678:0x12345679"])
    self.assertEqual(base_command._get_secureranges([(0x12345678, "+256")]), ["--securerange", "0x12345678:+256"])

  def test_base_get_regions(self):
    base_command = BaseCommand(MockCommander())
    self.assertEqual(base_command._get_regions([]), [])
    self.assertEqual(base_command._get_regions(["@mainflash"]), ["--region", "@mainflash"])
    self.assertEqual(base_command._get_regions(["@mainflash", "@sideflash"]), ["--region", "@mainflash", "--region", "@sideflash"])

  def test_base_get_patches(self):
    base_command = BaseCommand(MockCommander())

    with self.assertRaises(ValueError):
      base_command._get_patches([(0x12345678)])

    with self.assertRaises(ValueError):
      base_command._get_patches([(0x12345678, 0x12345679, 0x1234567A, 0x1234567B)])

    self.assertEqual(base_command._get_patches([]), [])
    self.assertEqual(base_command._get_patches([(0x12345678, 0x12345679)]), ["--patch", "0x12345678:0x12345679"])
    self.assertEqual(base_command._get_patches([(0x12345678, "0x12345679")]), ["--patch", "0x12345678:0x12345679"])
    self.assertEqual(base_command._get_patches([("0x12345678", 0x12345679)]), ["--patch", "0x12345678:0x12345679"])
    self.assertEqual(base_command._get_patches([("0x12345678", "0x12345679")]), ["--patch", "0x12345678:0x12345679"])
    self.assertEqual(base_command._get_patches([(0x12345678, 0x12345679, None)]), ["--patch", "0x12345678:0x12345679"])
    self.assertEqual(base_command._get_patches([(0x12345678, 0x12345679, 4)]), ["--patch", "0x12345678:0x12345679:4"])
    self.assertEqual(base_command._get_patches([("0x12345678", "0x12345679", "4")]), ["--patch", "0x12345678:0x12345679:4"])

  def test_base_get_tokens(self):
    base_command = BaseCommand(MockCommander())
    self.assertEqual(base_command._get_tokens([]), [])
    self.assertEqual(base_command._get_tokens(["TOKEN_NAME:value"]), ["--token", "TOKEN_NAME:value"])
    self.assertEqual(base_command._get_tokens(["TOKEN_NAME:value", "TOKEN_NAME2:value2"]), ["--token", "TOKEN_NAME:value", "--token", "TOKEN_NAME2:value2"])

  def test_base_get_tokenfiles(self):
    base_command = BaseCommand(MockCommander())
    self.assertEqual(base_command._get_tokenfiles([]), [])
    self.assertEqual(base_command._get_tokenfiles(["tokenfile.txt"]), ["--tokenfile", "tokenfile.txt"])
    self.assertEqual(base_command._get_tokenfiles(["tokenfile.txt", "tokenfile2.txt"]), ["--tokenfile", "tokenfile.txt", "--tokenfile", "tokenfile2.txt"])

  def test_base_get_include_sections(self):
    base_command = BaseCommand(MockCommander())
    self.assertEqual(base_command._get_include_sections([]), [])
    self.assertEqual(base_command._get_include_sections(["section1"]), ["--include-section", "section1"])
    self.assertEqual(base_command._get_include_sections(["section1", "section2"]), ["--include-section", "section1", "--include-section", "section2"])

  def test_base_get_exclude_sections(self):
    base_command = BaseCommand(MockCommander())
    self.assertEqual(base_command._get_exclude_sections([]), [])
    self.assertEqual(base_command._get_exclude_sections(["section1"]), ["--exclude-section", "section1"])
    self.assertEqual(base_command._get_exclude_sections(["section1", "section2"]), ["--exclude-section", "section1", "--exclude-section", "section2"])
