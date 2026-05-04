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


class TestCtune(unittest.TestCase):
  def test_get_general_args(self):
    # Initialized with serial number and debug options
    commander = MockCommander(serial_number="123456789", debug_speed=4000, debug_tif="SWD")
    args = commander.ctune._get_general_args()
    self.assertEqual(args, ["--serialno", "123456789", "--speed", "4000", "--tif", "SWD"])

    # Initialized with ip address
    commander = MockCommander(ip_address="192.168.1.100")
    args = commander.ctune._get_general_args()
    self.assertEqual(args, ["--ip", "192.168.1.100"])

    # Initialized with serial port
    commander = MockCommander(serial_port="/dev/tty.usbmodem141101")
    args = commander.ctune._get_general_args()
    self.assertEqual(args, ["--identifybyserialport", "/dev/tty.usbmodem141101"])

    # Serial number as kwarg
    commander = MockCommander()
    args = commander.ctune._get_general_args(serial_number="123456789")
    self.assertEqual(args, ["--serialno", "123456789"])

    # Ip address as kwarg
    commander = MockCommander()
    args = commander.ctune._get_general_args(ip_address="192.168.1.100")
    self.assertEqual(args, ["--ip", "192.168.1.100"])

    # Serial port as kwarg
    commander = MockCommander()
    args = commander.ctune._get_general_args(serial_port="/dev/tty.usbmodem141101")
    self.assertEqual(args, ["--identifybyserialport", "/dev/tty.usbmodem141101"])

    # Debug options as kwargs
    commander = MockCommander()
    args = commander.ctune._get_general_args(debug_speed=4000, debug_tif="SWD", debug_irpre=2, debug_drpre=1)
    self.assertEqual(args, ["--speed", "4000", "--tif", "SWD", "--irpre", "2", "--drpre", "1"])

  def test_ctune_autoset_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.ctune.autoset()
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "ctune", "autoset", "--serialno", "123456789", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_ctune_autoset_command_with_device(self):
    commander = MockCommander(serial_number="123456789")
    commander.ctune.autoset(target_device="EFR32MG24")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "ctune", "autoset", "--serialno", "123456789", "--device", "EFR32MG24", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_ctune_get_command(self):
    commander = MockCommander(serial_number="123456789", debug_speed=2000000)
    commander.ctune.get()
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "ctune", "get", "--serialno", "123456789", "--speed", "2000000", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_ctune_set_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.ctune.set("AABBCCDD")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "ctune", "set", "--serialno", "123456789", "--value", "AABBCCDD", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)
