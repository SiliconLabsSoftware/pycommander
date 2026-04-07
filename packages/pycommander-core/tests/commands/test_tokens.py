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


class TestTokens(unittest.TestCase):
  def test_tokens_createheader_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.tokens.createheader("tokens.h", tokengroup="zigbee", tokendefs="defs.json")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "tokens", "createheader", "tokens.h",
      "--serialno", "123456789", "--tokengroup", "zigbee", "--tokendefs", "defs.json",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_tokens_erase_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.tokens.erase(
      securerange=(0x08000000, 0x08001000),
      type="secure",
      tokens=["TOKEN_A", "TOKEN_B"],
      tokengroup="common",
      tokendefs="defs.json",
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "tokens", "erase",
      "--serialno", "123456789",
      "--securerange", "0x08000000:0x08001000", "--type", "secure", "--token", "TOKEN_A", "--token", "TOKEN_B", "--tokengroup", "common",
      "--tokendefs", "defs.json",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_tokens_read_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.tokens.read(
      filenames=[],
      outfile="out.txt",
      showoverrides=True,
      tokens=["T1", "T2"],
      tokengroup="zigbee",
      tokendefs="defs.json",
      range=(0x0, 0x1000),
      securerange=(0x08000000, 0x08001000),
      type="device",
      includeall=True,
      address=0x08000000,
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "tokens", "read",
      "--serialno", "123456789",
      "--outfile", "out.txt", "--token", "T1", "--token", "T2", "--tokengroup", "zigbee",
      "--tokendefs", "defs.json",
      "--range", "0x00000000:0x00001000", "--showoverrides",
      "--securerange", "0x08000000:0x08001000",
      "--type", "device", "--includeall", "--address", "0x08000000",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_tokens_read_command_with_filenames(self):
    commander = MockCommander(serial_number="123456789")
    commander.tokens.read(filenames=["app.s37"])
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "tokens", "read", "app.s37",
      "app.s37", "--serialno", "123456789",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_tokens_write_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.tokens.write(
      tokenfiles=["tokens.json"],
      tokens=[("TOKEN_X", "1")],
      tokengroup="znet",
      tokendefs="defs.json",
      securerange=(0x08000000, 0x08002000),
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "tokens", "write",
      "--serialno", "123456789",
      "--tokenfile", "tokens.json", "--token", "TOKEN_X:1", "--tokengroup", "znet",
      "--tokendefs", "defs.json",
      "--securerange", "0x08000000:0x08002000",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_tokens_write_command_with_device(self):
    commander = MockCommander(serial_number="123456789")
    commander.tokens.write(
      tokenfiles=["tokens.json"],
      device="EFR32MG24",
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "tokens", "write",
      "--serialno", "123456789", "--device", "EFR32MG24",
      "--tokenfile", "tokens.json",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)
