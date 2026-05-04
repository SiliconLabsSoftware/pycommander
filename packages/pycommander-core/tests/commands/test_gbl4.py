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


class TestGbl4(unittest.TestCase):
  def test_get_general_args(self):
    # Initialized with device
    commander = MockCommander(target_device="EFR32MG24B020F1536IM48")
    args = commander.gbl4._get_general_args()
    self.assertEqual(args, ["--device", "EFR32MG24B020F1536IM48"])

    # Device as kwarg
    commander = MockCommander()
    args = commander.gbl4._get_general_args(target_device="EFR32MG24B020F1536IM48")
    self.assertEqual(args, ["--device", "EFR32MG24B020F1536IM48"])

    # No args
    commander = MockCommander()
    args = commander.gbl4._get_general_args()
    self.assertEqual(args, [])

  def test_gbl4_create_command(self):
    commander = MockCommander()
    commander.gbl4.create(
      "out.gbl4",
      config="config.yaml",
      data=["app.s37"],
      seupgrade="se.s37",
      encrypt_keyfile="key.bin",
      compress="lz4",
      certificate="cert.pem",
      sign_keyfile="key.pem",
      extsign=True,
      productid="0123456789ABCDEF",
      bundleversion="1.0.0",
      minversion="0.9.0",
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "gbl4", "create", "out.gbl4",
      "--config", "config.yaml", "--data", "app.s37", "--seupgrade", "se.s37",
      "--encrypt", "key.bin", "--compress", "lz4", "--certificate", "cert.pem",
      "--sign", "key.pem", "--extsign",
      "--productid", "0123456789ABCDEF", "--bundleversion", "1.0.0", "--minversion", "0.9.0",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_gbl4_createconfig_command(self):
    commander = MockCommander()
    commander.gbl4.createconfig("config.yaml")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "gbl4", "createconfig", "--outfile", "config.yaml", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_gbl4_createconfig_command_with_device(self):
    commander = MockCommander()
    commander.gbl4.createconfig("config.yaml", target_device="EFR32MG24")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "gbl4", "createconfig", "--device", "EFR32MG24", "--outfile", "config.yaml", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_gbl4_info_command(self):
    commander = MockCommander()
    commander.gbl4.info("file.gbl4")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "gbl4", "info", "file.gbl4", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_gbl4_parse_command(self):
    commander = MockCommander()
    commander.gbl4.parse("in.gbl4", seupgrade="se.s37", outfile="out.s37")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "gbl4", "parse", "in.gbl4", "--seupgrade", "se.s37", "--outfile", "out.s37", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_gbl4_sign_command(self):
    commander = MockCommander()
    commander.gbl4.sign("unsigned.gbl4", "sig.der", "signed.gbl4", verify_keyfile="pub.pem")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "gbl4", "sign", "unsigned.gbl4",
      "--signature", "sig.der", "--outfile", "signed.gbl4", "--verify", "pub.pem",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)
