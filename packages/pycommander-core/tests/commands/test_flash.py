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


class TestFlash(unittest.TestCase):
  def test_flash_command_minimal(self):
    commander = MockCommander(serial_number="123456789")
    commander.flash.flash(["app.s37"])
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "flash", "app.s37", "--serialno", "123456789", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_flash_command_with_options(self):
    commander = MockCommander(serial_number="123456789")
    commander.flash.flash(
      ["app.s37", "bootloader.s37"],
      address=0x08000000,
      halt=True,
      masserase=True,
      reset=False,
      close=False,
      verify=False,
      patches=[(0x100, 0xAB, 1)],
      tokens=[("TOKEN_X", "1")],
      tokenfiles=["tokens.json"],
      tokengroup="zigbee",
      tokendefs="defs.json",
      binary=True,
      include_sections=[".text"],
      exclude_sections=[".debug"],
      vtor=0x08000000,
      device="EFR32MG24",
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "flash", "app.s37", "bootloader.s37",
      "--serialno", "123456789", "--device", "EFR32MG24",
      "--address", "0x08000000", "--halt", "--masserase", "--noreset", "--noclose", "--noverify",
      "--patch", "0x00000100:0x000000AB:1",
      "--token", "TOKEN_X:1", "--tokenfile", "tokens.json", "--tokengroup", "zigbee",
      "--tokendefs", "defs.json",
      "--binary",
      "--include-section", ".text", "--exclude-section", ".debug",
      "--vtor", "0x08000000",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)
