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
import shutil

from pathlib import Path

from pycommander_cli.commander import Commander

class TestCommander(unittest.TestCase):
  def test_commander_cli_executable_path(self):
    commander = Commander()
    self.assertTrue(Path(commander._runner._executable).exists())

  def test_commander_cli_all_options_passed(self):
    command = shutil.which("echo")
    if command is None:
      self.fail("echo command not found")

    commander = Commander(
      serial_number="123456789",
      debug_speed=115200,
      debug_tif="TIF1",
      debug_irpre=1,
      debug_drpre=1,
      log_file_path=Path("test.log"),
      executable_path=Path(command),
    )

    self.assertEqual(commander._serial_number, "123456789")
    self.assertEqual(commander._debug_speed, 115200)
    self.assertEqual(commander._debug_tif, "TIF1")
    self.assertEqual(commander._debug_irpre, 1)
    self.assertEqual(commander._debug_drpre, 1)
    self.assertEqual(commander._runner._log_file_path, Path("test.log"))
    self.assertEqual(commander._runner._executable, str(Path(command)))


  def test_commander_cli_serial_number_and_ip_address_provided(self):
    with self.assertRaises(ValueError):
      Commander(serial_number="123456789", ip_address="192.168.1.1")

  def test_commander_cli_serial_number_and_serial_port_provided(self):
    with self.assertRaises(ValueError):
      Commander(serial_number="123456789", serial_port="COM1")

  def test_commander_cli_ip_address_and_serial_port_provided(self):
    with self.assertRaises(ValueError):
      Commander(ip_address="192.168.1.1", serial_port="COM1")
