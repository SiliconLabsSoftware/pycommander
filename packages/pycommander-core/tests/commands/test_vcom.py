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


class TestVcom(unittest.TestCase):
  def test_get_general_args(self):
    # Initialized with serial number
    commander = MockCommander(serial_number="123456789")
    args = commander.vcom._get_general_args()
    self.assertEqual(args, ["--serialno", "123456789"])

    # Initialized with ip address
    commander = MockCommander(ip_address="192.168.1.100")
    args = commander.vcom._get_general_args()
    self.assertEqual(args, ["--ip", "192.168.1.100"])

    # Initialized with serial port
    commander = MockCommander(serial_port="/dev/tty.usbmodem141101")
    args = commander.vcom._get_general_args()
    self.assertEqual(args, ["--identifybyserialport", "/dev/tty.usbmodem141101"])

    # Serial number as kwarg
    commander = MockCommander()
    args = commander.vcom._get_general_args(serial_number="123456789")
    self.assertEqual(args, ["--serialno", "123456789"])

    # Ip address as kwarg
    commander = MockCommander()
    args = commander.vcom._get_general_args(ip_address="192.168.1.100")
    self.assertEqual(args, ["--ip", "192.168.1.100"])

    # Serial port as kwarg
    commander = MockCommander()
    args = commander.vcom._get_general_args(serial_port="/dev/tty.usbmodem141101")
    self.assertEqual(args, ["--identifybyserialport", "/dev/tty.usbmodem141101"])

  def test_vcom_config_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.vcom.config(baudrate=115200, handshake="rtscts", store=True)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "vcom", "config",
      "--serialno", "123456789", "--baudrate", "115200", "--handshake", "rtscts", "--store",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_vcom_config_command_with_device(self):
    commander = MockCommander(serial_number="123456789")
    commander.vcom.config(target_device="EFR32MG24")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "vcom", "config",
      "--serialno", "123456789", "--device", "EFR32MG24",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)
