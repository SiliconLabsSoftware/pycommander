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


class TestOta(unittest.TestCase):
  def test_ota_create_command(self):
    commander = MockCommander()
    commander.ota.create(
      "out.ota",
      type="matter",
      input_files=["app.gbl", "boot.gbl"],
      vendorid=1,
      productid=2,
      swversion=3,
      swstring="1.0.0",
      min_sw=0,
      max_sw=99,
      releasenote="https://example.com/notes",
      digest="sha256",
      upgrade_images=["zigbee.gbl"],
      firmware_version=10,
      manufacturer_id=100,
      image_type=200,
      string="Zigbee OTA",
      stack_version=2,
      credentials=1,
      destination="0x0000",
      min_hw=0,
      max_hw=5,
      null_tag="tag",
      manufacturer_tags=["tag1", "tag2"],
      certificate="cert.pem",
      sign=True,
      extsign=True,
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "ota", "create",
      "--outfile", "out.ota", "--type", "matter",
      "--input", "app.gbl", "--input", "boot.gbl",
      "--vendorid", "1", "--productid", "2", "--swversion", "3", "--swstring", "1.0.0",
      "--min-sw", "0", "--max-sw", "99",
      "--releasenote", "https://example.com/notes", "--digest", "sha256",
      "--upgrade-image", "zigbee.gbl",
      "--firmware-version", "10", "--manufacturer-id", "100", "--image-type", "200",
      "--string", "Zigbee OTA", "--stack-version", "2", "--credentials", "1", "--destination", "0x0000",
      "--min-hw", "0", "--max-hw", "5", "--null", "tag",
      "--manufacturer-tag", "tag1", "--manufacturer-tag", "tag2",
      "--certificate", "cert.pem", "--sign", "--extsign",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_ota_parse_command(self):
    commander = MockCommander()
    commander.ota.parse("in.ota", type="zigbee", outfile="out.bin")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "ota", "parse", "in.ota", "--type", "zigbee", "--outfile", "out.bin", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_ota_sign_command(self):
    commander = MockCommander()
    commander.ota.sign("in.ota", "sig.der", "out.ota", "prime256v1")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "ota", "sign", "in.ota",
      "--signature", "sig.der", "--outfile", "out.ota", "--curve", "prime256v1",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_ota_verify_command(self):
    commander = MockCommander()
    commander.ota.verify("file.ota", "cert.pem")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "ota", "verify", "file.ota", "--certificate", "cert.pem", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_ota_verify_command_with_device(self):
    commander = MockCommander()
    commander.ota.verify("file.ota", "cert.pem", target_device="EFR32MG24")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "ota", "verify", "file.ota", "--device", "EFR32MG24", "--certificate", "cert.pem", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)
