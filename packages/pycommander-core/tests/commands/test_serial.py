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

from ..mock_commander import MockCommander


class TestSerial(unittest.TestCase):
  def test_serial_getopn_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.serial.getopn()
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "serial", "getopn", "--serialno", "123456789", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_serial_getopn_command_with_serialport(self):
    commander = MockCommander()
    commander.serial.getopn(serialport="COM1")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "serial", "getopn", "--serialport", "COM1", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_serial_load_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.serial.load("image.s37", fixedspeed=True, serialport="COM2")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "serial", "load", "image.s37",
      "--serialno", "123456789", "--fixedspeed", "--serialport", "COM2",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_serial_load_command_with_device(self):
    commander = MockCommander(serial_number="123456789")
    commander.serial.load("image.s37", target_device="EFR32MG24")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "serial", "load", "image.s37",
      "--serialno", "123456789", "--device", "EFR32MG24",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_serial_lock_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.serial.lock(token_file="t.dat", key_file="k.dat", userdata="ud", serialport="COM1")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "serial", "lock",
      "--serialno", "123456789", "--token", "t.dat", "--key", "k.dat", "--userdata", "ud", "--serialport", "COM1",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_serial_unlock_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.serial.unlock(token_file="t.dat", key_file="k.dat", userdata="ud", serialport="COM3")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "serial", "unlock",
      "--serialno", "123456789", "--token", "t.dat", "--key", "k.dat", "--userdata", "ud", "--serialport", "COM3",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)
