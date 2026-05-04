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
  def test_get_general_args(self):
    # Initialized with serial number
    commander = MockCommander(serial_number="123456789")
    args = commander.serial._get_general_args()
    self.assertEqual(args, ["--serialno", "123456789"])

    # Initialized with ip address
    commander = MockCommander(ip_address="192.168.1.100")
    args = commander.serial._get_general_args()
    self.assertEqual(args, ["--ip", "192.168.1.100"])

    # Initialized with serial port
    commander = MockCommander(serial_port="/dev/tty.usbmodem141101")
    args = commander.serial._get_general_args()
    self.assertEqual(args, ["--identifybyserialport", "/dev/tty.usbmodem141101"])

    # Serial number as kwarg
    commander = MockCommander()
    args = commander.serial._get_general_args(serial_number="123456789")
    self.assertEqual(args, ["--serialno", "123456789"])

    # Ip address as kwarg
    commander = MockCommander()
    args = commander.serial._get_general_args(ip_address="192.168.1.100")
    self.assertEqual(args, ["--ip", "192.168.1.100"])

    # Serial port as kwarg
    commander = MockCommander()
    args = commander.serial._get_general_args(serial_port="/dev/tty.usbmodem141101")
    self.assertEqual(args, ["--identifybyserialport", "/dev/tty.usbmodem141101"])

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
