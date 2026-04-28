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
