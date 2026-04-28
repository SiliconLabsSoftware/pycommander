"""
License
Copyright 2026 Silicon Laboratories Inc. www.silabs.com
*******************************************************************************
The licensor of this software is Silicon Laboratories Inc. Your use of this
software is governed by the terms of Silicon Labs Master Software License
Agreement (MSLA) available at
www.silabs.com/about-us/legal/master-software-license-agreement. This
software is distributed to you in Source Code format and is governed by the
sections of the MSLA applicable to Source Code.
*******************************************************************************
"""

import unittest

from pycommander_core.commands._base import BaseCommand, CommandResult
from pycommander_core.runner import RunnerResult

from ..mock_commander import MockCommander

class TestBase(unittest.TestCase):

  def test_base_run(self):
    commander = MockCommander()
    base_command = BaseCommand(commander)
    self.assertEqual(base_command._run("command", "arg1", "arg2"), CommandResult(0, {"result": {}}))
    self.assertEqual(commander._runner.logged_commands, [["mock", "command", "arg1", "arg2", "--json"]])

  def test_base_run_empty_args(self):
    commander = MockCommander()
    base_command = BaseCommand(commander)
    self.assertEqual(base_command._run("command", "", "arg2"), CommandResult(0, {"result": {}}))
    self.assertEqual(commander._runner.logged_commands, [["mock", "command", "arg2", "--json"]])

  def test_base_run_none_args(self):
    commander = MockCommander()
    base_command = BaseCommand(commander)
    self.assertEqual(base_command._run("command", "arg1", None, "arg3"), CommandResult(0, {"result": {}}))
    self.assertEqual(commander._runner.logged_commands, [["mock", "command", "arg1", "arg3", "--json"]])

  def test_base_run_bad_json_returncode_zero(self):
    commander = MockCommander()
    commander._runner.queue_result(RunnerResult(0, "This is not JSON"))
    base_command = BaseCommand(commander)
    self.assertEqual(base_command._run("command", "arg1", "arg2"), CommandResult(0, {"success": True, "output": "This is not JSON"}))
    self.assertEqual(commander._runner.logged_commands, [["mock", "command", "arg1", "arg2", "--json"]])

  def test_base_run_bad_json_returncode_non_zero(self):
    commander = MockCommander()
    commander._runner.queue_result(RunnerResult(1, "This is not JSON"))
    base_command = BaseCommand(commander)
    self.assertEqual(base_command._run("command", "arg1", "arg2"), CommandResult(1, {"success": False, "error": "This is not JSON"}))
    self.assertEqual(commander._runner.logged_commands, [["mock", "command", "arg1", "arg2", "--json"]])

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

  def test_base_get_debug_args(self):
    commander = MockCommander(debug_speed=1000000, debug_tif="SWD", debug_irpre=1000000, debug_drpre=1000000)
    base_command = BaseCommand(commander)
    self.assertEqual(base_command._get_debug_args(), ["--speed", "1000000", "--tif", "SWD", "--irpre", "1000000", "--drpre", "1000000"])

  def test_base_get_kwargs(self):
    base_command = BaseCommand(MockCommander())
    self.assertEqual(base_command._get_kwargs(), [])
    self.assertEqual(base_command._get_kwargs(serial_number="123456789"), ["--serialno", "123456789"])
    self.assertEqual(base_command._get_kwargs(ip_address="192.168.1.100"), ["--ip", "192.168.1.100"])
    self.assertEqual(base_command._get_kwargs(serial_port="/dev/tty.usbmodem141101"), ["--identifybyserialport", "/dev/tty.usbmodem141101"])
    self.assertEqual(base_command._get_kwargs(debug_speed=1000000), ["--speed", "1000000"])
    self.assertEqual(base_command._get_kwargs(debug_tif="SWD"), ["--tif", "SWD"])
    self.assertEqual(base_command._get_kwargs(debug_irpre=1000000), ["--irpre", "1000000"])
    self.assertEqual(base_command._get_kwargs(debug_drpre=1000000), ["--drpre", "1000000"])
    self.assertEqual(base_command._get_kwargs(target_device="123456789"), ["--device", "123456789"])
    self.assertEqual(base_command._get_kwargs(force=True), ["--force"])
    self.assertEqual(base_command._get_kwargs(target_device=None), [])
    self.assertEqual(base_command._get_kwargs(force=False), [])
    self.assertEqual(base_command._get_kwargs(
      target_device="Cortex-M4",
      force=True,
      debug_speed=1000000,
      debug_tif="SWD",
      debug_irpre=1000000,
      debug_drpre=1000000,
      serial_number="123456789",
      ip_address="192.168.1.100",
      serial_port="/dev/tty.usbmodem141101",
    ), [
      "--serialno", "123456789",
      "--ip", "192.168.1.100",
      "--identifybyserialport", "/dev/tty.usbmodem141101",
      "--speed", "1000000",
      "--tif", "SWD",
      "--irpre", "1000000",
      "--drpre", "1000000",
      "--device", "Cortex-M4",
      "--force",
    ])

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
    self.assertEqual(base_command._get_tokens([("TOKEN_NAME", "value")]), ["--token", "TOKEN_NAME:value"])
    self.assertEqual(base_command._get_tokens([("TOKEN_NAME", "value"), ("TOKEN_NAME2", "value2")]), ["--token", "TOKEN_NAME:value", "--token", "TOKEN_NAME2:value2"])

  def test_base_get_token_names(self):
    base_command = BaseCommand(MockCommander())
    self.assertEqual(base_command._get_token_names([]), [])
    self.assertEqual(base_command._get_token_names(["TOKEN_NAME"]), ["--token", "TOKEN_NAME"])
    self.assertEqual(base_command._get_token_names(["TOKEN_NAME", "TOKEN_NAME2"]), ["--token", "TOKEN_NAME", "--token", "TOKEN_NAME2"])

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
