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


class TestWritemem(unittest.TestCase):
  def test_get_general_args(self):
    # Initialized with serial number and debug options
    commander = MockCommander(serial_number="123456789", debug_speed=4000, debug_tif="SWD")
    args = commander.writemem._get_general_args()
    self.assertEqual(args, ["--serialno", "123456789", "--speed", "4000", "--tif", "SWD"])

    # Initialized with ip address
    commander = MockCommander(ip_address="192.168.1.100")
    args = commander.writemem._get_general_args()
    self.assertEqual(args, ["--ip", "192.168.1.100"])

    # Initialized with serial port
    commander = MockCommander(serial_port="/dev/tty.usbmodem141101")
    args = commander.writemem._get_general_args()
    self.assertEqual(args, ["--identifybyserialport", "/dev/tty.usbmodem141101"])

    # Serial number as kwarg
    commander = MockCommander()
    args = commander.writemem._get_general_args(serial_number="123456789")
    self.assertEqual(args, ["--serialno", "123456789"])

    # Ip address as kwarg
    commander = MockCommander()
    args = commander.writemem._get_general_args(ip_address="192.168.1.100")
    self.assertEqual(args, ["--ip", "192.168.1.100"])

    # Serial port as kwarg
    commander = MockCommander()
    args = commander.writemem._get_general_args(serial_port="/dev/tty.usbmodem141101")
    self.assertEqual(args, ["--identifybyserialport", "/dev/tty.usbmodem141101"])

    # Debug options as kwargs
    commander = MockCommander()
    args = commander.writemem._get_general_args(debug_speed=4000, debug_tif="SWD", debug_irpre=2, debug_drpre=1)
    self.assertEqual(args, ["--speed", "4000", "--tif", "SWD", "--irpre", "2", "--drpre", "1"])

  def test_writemem_command_minimal(self):
    commander = MockCommander(serial_number="123456789")
    commander.writemem.writemem("mem.bin")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "writemem", "mem.bin", "--serialno", "123456789", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_writemem_command_patches_only(self):
    commander = MockCommander(serial_number="123456789")
    commander.writemem.writemem(patches=[(0x20000000, 0xAB, 1)])
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "writemem",
      "--serialno", "123456789",
      "--patch", "0x20000000:0x000000AB:1",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_writemem_command_with_options(self):
    commander = MockCommander(serial_number="123456789")
    commander.writemem.writemem(
      "mem.bin",
      address=0x20000000,
      halt=True,
      patches=[(0x20000004, 0xCD, 1)],
      binary=True,
      target_device="EFR32MG24",
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "writemem", "mem.bin",
      "--serialno", "123456789",
      "--device", "EFR32MG24",
      "--address", "0x20000000",
      "--halt",
      "--patch", "0x20000004:0x000000CD:1",
      "--binary",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)
