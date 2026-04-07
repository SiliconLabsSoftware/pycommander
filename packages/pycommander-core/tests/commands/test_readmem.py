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


class TestReadmem(unittest.TestCase):
  def test_readmem_command_minimal(self):
    commander = MockCommander(serial_number="123456789")
    commander.readmem.readmem()
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "readmem", "--serialno", "123456789", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_readmem_command_with_options(self):
    commander = MockCommander(serial_number="123456789")
    commander.readmem.readmem(
      outfile="mem.bin",
      ranges=[(0x08000000, 0x08010000)],
      regions=["@main"],
      device="EFR32MG24",
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "readmem",
      "--serialno", "123456789", "--device", "EFR32MG24",
      "--outfile", "mem.bin", "--range", "0x08000000:0x08010000", "--region", "@main",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)
