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


class TestUtil(unittest.TestCase):
  def test_get_general_args(self):
    # Initialized with device
    commander = MockCommander(target_device="EFR32MG24B020F1536IM48")
    args = commander.util._get_general_args()
    self.assertEqual(args, ["--device", "EFR32MG24B020F1536IM48"])

    # Device as kwarg
    commander = MockCommander()
    args = commander.util._get_general_args(target_device="EFR32MG24B020F1536IM48")
    self.assertEqual(args, ["--device", "EFR32MG24B020F1536IM48"])

    # No args
    commander = MockCommander()
    args = commander.util._get_general_args()
    self.assertEqual(args, [])

  def test_util_appinfo_command(self):
    commander = MockCommander()
    commander.util.appinfo("app.s37")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "util", "appinfo", "app.s37", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_util_appinfo_command_with_device(self):
    commander = MockCommander()
    commander.util.appinfo("app.s37", target_device="EFR32MG24")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "util", "appinfo", "app.s37", "--device", "EFR32MG24", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_util_elfinfo_command(self):
    commander = MockCommander()
    commander.util.elfinfo("app.elf")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "util", "elfinfo", "app.elf", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_util_extractkeys_command(self):
    commander = MockCommander()
    commander.util.extractkeys("config.json", "keys_dir")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "util", "extractkeys", "config.json", "--dir", "keys_dir", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_util_gencert_command(self):
    commander = MockCommander()
    commander.util.gencert("cert.der", 1, "gbl", "pub.pem", sign_keyfile="key.pem", extsign=True)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "util", "gencert",
      "--outfile", "cert.der", "--cert-version", "1", "--cert-type", "gbl", "--cert-pubkey", "pub.pem",
      "--sign", "key.pem", "--extsign",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_util_genkey_command(self):
    commander = MockCommander()
    commander.util.genkey("ecc-p256", pubkey="pub.pem", privkey="priv.pem", outfile="out.pem", tokenfile="tok.dat")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "util", "genkey",
      "--type", "ecc-p256", "--pubkey", "pub.pem", "--privkey", "priv.pem", "--outfile", "out.pem", "--tokenfile", "tok.dat",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_util_keytotoken_command(self):
    commander = MockCommander()
    commander.util.keytotoken("pub.pem", outfile="token.dat", key_type="ecc-p256")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "util", "keytotoken", "pub.pem", "--outfile", "token.dat", "--type", "ecc-p256", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_util_rpsinfo_command(self):
    commander = MockCommander()
    commander.util.rpsinfo("app.rps")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "util", "rpsinfo", "app.rps", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_util_usage_command(self):
    commander = MockCommander()
    commander.util.usage("app.elf", map_filename="app.map", include_sections=[".text"], exclude_sections=[".debug"])
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "util", "usage", "app.elf",
      "--map", "app.map", "--include-section", ".text", "--exclude-section", ".debug",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_util_verifysign_command(self):
    commander = MockCommander()
    commander.util.verifysign("signed.bin", "pub.pem")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "util", "verifysign", "signed.bin", "--verify", "pub.pem", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_util_signcert_command(self):
    commander = MockCommander()
    commander.util.signcert("cert.der", "sig.der", "gbl", "signed.der", verify_keyfile="pub.pem")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "util", "signcert", "cert.der",
      "--signature", "sig.der", "--cert-type", "gbl", "--outfile", "signed.der", "--verify", "pub.pem",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_util_genkeyconfig_command(self):
    commander = MockCommander()
    commander.util.genkeyconfig("keyconfig.json")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "util", "genkeyconfig",
      "--outfile", "keyconfig.json",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)
