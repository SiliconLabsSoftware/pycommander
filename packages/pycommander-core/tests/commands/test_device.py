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


class TestDevice(unittest.TestCase):
  def test_get_general_args(self):
    # Initialized with serial number and debug options
    commander = MockCommander(serial_number="123456789", debug_speed=4000, debug_tif="SWD")
    args = commander.device._get_general_args()
    self.assertEqual(args, ["--serialno", "123456789", "--speed", "4000", "--tif", "SWD"])

    # Initialized with ip address
    commander = MockCommander(ip_address="192.168.1.100")
    args = commander.device._get_general_args()
    self.assertEqual(args, ["--ip", "192.168.1.100"])

    # Initialized with serial port
    commander = MockCommander(serial_port="/dev/tty.usbmodem141101")
    args = commander.device._get_general_args()
    self.assertEqual(args, ["--identifybyserialport", "/dev/tty.usbmodem141101"])

    # Serial number as kwarg
    commander = MockCommander()
    args = commander.device._get_general_args(serial_number="123456789")
    self.assertEqual(args, ["--serialno", "123456789"])

    # Ip address as kwarg
    commander = MockCommander()
    args = commander.device._get_general_args(ip_address="192.168.1.100")
    self.assertEqual(args, ["--ip", "192.168.1.100"])

    # Serial port as kwarg
    commander = MockCommander()
    args = commander.device._get_general_args(serial_port="/dev/tty.usbmodem141101")
    self.assertEqual(args, ["--identifybyserialport", "/dev/tty.usbmodem141101"])

    # Debug options as kwargs
    commander = MockCommander()
    args = commander.device._get_general_args(debug_speed=4000, debug_tif="SWD", debug_irpre=2, debug_drpre=1)
    self.assertEqual(args, ["--speed", "4000", "--tif", "SWD", "--irpre", "2", "--drpre", "1"])

  def test_device_info_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.device.info()
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "device", "info", "--serialno", "123456789", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_device_info_command_with_device(self):
    commander = MockCommander(serial_number="123456789")
    commander.device.info(target_device="EFR32MG24")
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
    commander.device.masserase(target_device="EFR32MG24")
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
