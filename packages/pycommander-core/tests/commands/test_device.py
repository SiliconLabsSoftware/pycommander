import unittest

from ..mock_commander import MockCommander


class TestDevice(unittest.TestCase):
  def test_device_info_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.device.info()
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "device", "info", "--serialno", "123456789", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_device_info_command_with_device(self):
    commander = MockCommander(serial_number="123456789")
    commander.device.info(device="EFR32MG24")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "device", "info", "--serialno", "123456789", "--device", "EFR32MG24", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_device_lock_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.device.lock()
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "device", "lock", "--serialno", "123456789", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_device_unlock_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.device.unlock()
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "device", "unlock", "--serialno", "123456789", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_device_masserase_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.device.masserase()
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "device", "masserase", "--serialno", "123456789", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_device_masserase_command_with_device(self):
    commander = MockCommander(serial_number="123456789")
    commander.device.masserase(device="EFR32MG24")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "device", "masserase", "--serialno", "123456789", "--device", "EFR32MG24", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_device_pageerase_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.device.pageerase(ranges=[(0x0, 0x8000)], regions=["@main"])
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "device", "pageerase",
      "--range", "0x00000000:0x00008000", "--region", "@main",
      "--serialno", "123456789", "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_device_protect_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.device.protect(read=True, write=True, disable=True, ranges=[(0x0, 0x1000)])
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "device", "protect",
      "--read", "--write", "--disable",
      "--range", "0x00000000:0x00001000",
      "--serialno", "123456789", "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_device_recover_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.device.recover()
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "device", "recover", "--serialno", "123456789", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_device_reset_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.device.reset()
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "device", "reset", "--serialno", "123456789", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_device_zwave_qrcode_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.device.zwave_qrcode(timeout_ms=5000)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "device", "zwave-qrcode", "--serialno", "123456789", "--timeout", "5000", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)
