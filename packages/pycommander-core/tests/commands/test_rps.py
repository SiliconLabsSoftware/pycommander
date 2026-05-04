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


class TestRps(unittest.TestCase):
  def test_get_general_args(self):
    # Initialized with device
    commander = MockCommander(target_device="EFR32MG24B020F1536IM48")
    args = commander.rps._get_general_args()
    self.assertEqual(args, ["--device", "EFR32MG24B020F1536IM48"])

    # Device as kwarg
    commander = MockCommander()
    args = commander.rps._get_general_args(target_device="EFR32MG24B020F1536IM48")
    self.assertEqual(args, ["--device", "EFR32MG24B020F1536IM48"])

    # No args
    commander = MockCommander()
    args = commander.rps._get_general_args()
    self.assertEqual(args, [])

  def test_rps_create_command(self):
    commander = MockCommander()
    commander.rps.create(
      "out.rps",
      encrypt_key="enc.key",
      mic_key="mic.key",
      iv_file="iv.bin",
      sign_keyfile="sign.pem",
      sha="sha256",
      extsign=True,
      address=0x08000000,
      app="app.s37",
      app_version=1,
      fw_info=2,
      include_sections=[".text"],
      exclude_sections=[".debug"],
      map_file="app.map",
      combinedimage=True,
      key_type="ecc-p256",
      new_key="new.key",
      prev_key="prev.key",
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "rps", "create", "out.rps",
      "--encrypt", "enc.key", "--mic", "mic.key", "--iv", "iv.bin", "--sign", "sign.pem", "--sha", "sha256",
      "--extsign",
      "--address", "0x08000000", "--app", "app.s37", "--app-version", "1", "--fw-info", "2",
      "--include-section", ".text", "--exclude-section", ".debug",
      "--map", "app.map", "--combinedimage",
      "--key-type", "ecc-p256", "--new-key", "new.key", "--prev-key", "prev.key",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_rps_convert_command(self):
    commander = MockCommander()
    commander.rps.convert(
      "out.rps",
      encrypt_key="enc.key",
      mic_key="mic.key",
      iv_file="iv.bin",
      sign_keyfile="sign.pem",
      sha="sha256",
      extsign=True,
      app="app.s37",
      nwpapp="nwp.s37",
      app_version=1,
      fw_info=2,
      combinedimage=True,
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "rps", "convert", "out.rps",
      "--encrypt", "enc.key", "--mic", "mic.key", "--iv", "iv.bin", "--sign", "sign.pem", "--sha", "sha256",
      "--extsign",
      "--app", "app.s37", "--nwpapp", "nwp.s37", "--app-version", "1", "--fw-info", "2", "--combinedimage",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_rps_load_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.rps.load("file.rps", eraseapp=True)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "rps", "load", "file.rps", "--serialno", "123456789", "--eraseapp", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_rps_load_command_with_device(self):
    commander = MockCommander(serial_number="123456789")
    commander.rps.load("file.rps", target_device="SiWx917")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "rps", "load", "file.rps", "--device", "SiWx917", "--serialno", "123456789", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_rps_sign_command(self):
    commander = MockCommander()
    commander.rps.sign("in.rps", "sig.der", outfile="signed.rps")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "rps", "sign", "in.rps", "--signature", "sig.der", "--outfile", "signed.rps",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)
