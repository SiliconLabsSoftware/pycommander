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


class TestSecurity(unittest.TestCase):
  def test_get_general_args(self):
    # Initialized with serial number and debug options
    commander = MockCommander(serial_number="123456789", debug_speed=4000, debug_tif="SWD")
    args = commander.security._get_general_args()
    self.assertEqual(args, ["--serialno", "123456789", "--speed", "4000", "--tif", "SWD"])

    # Initialized with ip address
    commander = MockCommander(ip_address="192.168.1.100")
    args = commander.security._get_general_args()
    self.assertEqual(args, ["--ip", "192.168.1.100"])

    # Initialized with serial port
    commander = MockCommander(serial_port="/dev/tty.usbmodem141101")
    args = commander.security._get_general_args()
    self.assertEqual(args, ["--identifybyserialport", "/dev/tty.usbmodem141101"])

    # Serial number as kwarg
    commander = MockCommander()
    args = commander.security._get_general_args(serial_number="123456789")
    self.assertEqual(args, ["--serialno", "123456789"])

    # Ip address as kwarg
    commander = MockCommander()
    args = commander.security._get_general_args(ip_address="192.168.1.100")
    self.assertEqual(args, ["--ip", "192.168.1.100"])

    # Serial port as kwarg
    commander = MockCommander()
    args = commander.security._get_general_args(serial_port="/dev/tty.usbmodem141101")
    self.assertEqual(args, ["--identifybyserialport", "/dev/tty.usbmodem141101"])

    # Debug options as kwargs
    commander = MockCommander()
    args = commander.security._get_general_args(debug_speed=4000, debug_tif="SWD", debug_irpre=2, debug_drpre=1)
    self.assertEqual(args, ["--speed", "4000", "--tif", "SWD", "--irpre", "2", "--drpre", "1"])

  def test_security_attestation_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.security.attestation(reset=False)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "security", "attestation",
      "--serialno", "123456789", "--noreset",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_security_attestation_command_with_device(self):
    commander = MockCommander(serial_number="123456789")
    commander.security.attestation(target_device="EFR32MG24")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "security", "attestation",
      "--serialno", "123456789", "--device", "EFR32MG24",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_security_closeregion_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.security.closeregion(1, reset=False, codeversion=2)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "security", "closeregion", "1",
      "--serialno", "123456789", "--noreset", "--codeversion", "2",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_security_disabledeviceerase_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.security.disabledeviceerase(reset=False, dryrun=True, prompt=False)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "security", "disabledeviceerase",
      "--serialno", "123456789", "--noreset", "--dryrun", "--noprompt",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_security_disabletamper_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.security.disabletamper(reset=False, store=False, cert="cert.pem", cert_privkey="cert_privkey.pem", command_key="command_key.pem", cert_signature="cert_signature.pem", command_signature="command_signature.pem", authorization="authorization.dat", cert_pubkey="cert_pubkey.pem", disable_param="disable_param")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "security", "disabletamper",
      "--serialno", "123456789", "--noreset", "--nostore", "--cert", "cert.pem", "--cert-privkey", "cert_privkey.pem", "--command-key", "command_key.pem", "--cert-signature", "cert_signature.pem", "--command-signature", "command_signature.pem", "--authorization", "authorization.dat", "--cert-pubkey", "cert_pubkey.pem", "--disable-param", "disable_param",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_security_erasedevice_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.security.erasedevice(reset=False, dryrun=True)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "security", "erasedevice",
      "--serialno", "123456789", "--noreset", "--dryrun",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_security_fwupgrade_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.security.fwupgrade("fw.bin", reset=False, address=0x08000000, prompt=False)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "security", "fwupgrade", "fw.bin",
      "--serialno", "123456789", "--noreset", "--address", "0x08000000", "--noprompt", "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_security_fwupgradecheck_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.security.fwupgradecheck(reset=False)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "security", "fwupgradecheck",
      "--serialno", "123456789", "--noreset", "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_security_genauth_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.security.genauth(outfile="auth.dat", store=False, deviceserialno="123456789", reset=False)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "security", "genauth",
      "--serialno", "123456789", "--outfile", "auth.dat", "--nostore", "--deviceserialno", "123456789", "--noreset",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_security_gencert_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.security.gencert(
      outfile="cert.der",
      store=False,
      deviceserialno="123456789",
      reset=False,
      cert_pubkey="pub.pem",
      authorization="auth.dat",
      command_key="command.key",
      extsign=True,
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "security", "gencert",
      "--serialno", "123456789",
      "--outfile", "cert.der",
      "--nostore",
      "--deviceserialno", "123456789",
      "--noreset",
      "--cert-pubkey", "pub.pem",
      "--authorization", "auth.dat",
      "--command-key", "command.key",
      "--extsign",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_security_gencommand_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.security.gencommand(
      outfile="command.dat",
      store=False,
      reset=False,
      action="disable",
      disable_param=1,
      unlock_param="unlock_param",
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "security", "gencommand",
      "--serialno", "123456789", "--outfile", "command.dat", "--nostore", "--noreset",
      "--action", "disable", "--disable-param", "1", "--unlock-param", "unlock_param",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_security_genconfig_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.security.genconfig(outfile="config.json", store=False, deviceserialno="123456789", reset=False)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "security", "genconfig",
      "--serialno", "123456789", "--outfile", "config.json", "--nostore", "--deviceserialno", "123456789", "--noreset",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_security_genkey_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.security.genkey("ecc-p256", outfile="key.pem", privkey="priv.pem", pubkey="pub.pem")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "security", "genkey",
      "--serialno", "123456789", "--type", "ecc-p256",
      "--outfile", "key.pem", "--privkey", "priv.pem", "--pubkey", "pub.pem",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_security_getpath_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.security.getpath(reset=False, deviceserialno="123456789")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "security", "getpath",
      "--serialno", "123456789", "--noreset", "--deviceserialno", "123456789",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_security_lock_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.security.lock(reset=False, dryrun=True, trustzone="tz.yaml")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "security", "lock",
      "--serialno", "123456789", "--noreset", "--dryrun", "--trustzone", "tz.yaml",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_security_lockconfig_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.security.lockconfig(reset=False, secure_debug_unlock="secure_debug_unlock.yaml", dryrun=True, prompt=False)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "security", "lockconfig",
      "--serialno", "123456789", "--noreset", "--secure-debug-unlock", "secure_debug_unlock.yaml", "--dryrun", "--noprompt",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_security_otprollbackcount_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.security.otprollbackcount(reset=False)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "security", "otprollbackcount",
      "--serialno", "123456789", "--noreset",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_security_provision_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.security.provision(reset=False, sefw="se.fw")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "security", "provision",
      "--serialno", "123456789", "--noreset", "--sefw", "se.fw",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_security_readcert_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.security.readcert("device", outfile="cert.der", reset=False)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "security", "readcert", "device",
      "--serialno", "123456789", "--outfile", "cert.der", "--noreset",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_security_status_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.security.status(reset=False, trustzone=True, verbose=True)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "security", "status",
      "--serialno", "123456789", "--noreset", "--trustzone", "--verbose",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_security_readconfig_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.security.readconfig(reset=False)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "security", "readconfig",
      "--serialno", "123456789", "--noreset",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_security_readkey_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.security.readkey(sign=True, command=True, outfile="key.pem", reset=False, store=False)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "security", "readkey",
      "--serialno", "123456789", "--sign", "--command", "--outfile", "key.pem", "--noreset", "--nostore",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_security_readregionconfig_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.security.readregionconfig(outfile="region.json", reset=False)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "security", "readregionconfig",
      "--serialno", "123456789", "--outfile", "region.json", "--noreset",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_security_rollchallenge_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.security.rollchallenge(reset=False, store=False)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "security", "rollchallenge",
      "--serialno", "123456789", "--noreset", "--nostore",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_security_transitiontodevelopment_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.security.transitiontodevelopment(reset=False, dryrun=True, prompt=False)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "security", "transitiontodevelopment",
      "--serialno", "123456789", "--noreset", "--dryrun", "--noprompt",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_security_unlock_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.security.unlock(
      reset=False, store=False, cert="c.pem", cert_privkey="cp.pem",
      command_key="ck.pem", cert_signature="cs.pem", command_signature="coms.pem",
      authorization="auth.dat", cert_pubkey="cpub.pem", unlock_param="up",
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "security", "unlock",
      "--serialno", "123456789", "--noreset", "--nostore",
      "--cert", "c.pem", "--cert-privkey", "cp.pem", "--command-key", "ck.pem",
      "--cert-signature", "cs.pem", "--command-signature", "coms.pem",
      "--authorization", "auth.dat", "--cert-pubkey", "cpub.pem", "--unlock-param", "up",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_security_writeconfig_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.security.writeconfig(store=False, reset=False, dryrun=True, prompt=False, configfile="config.json")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "security", "writeconfig",
      "--serialno", "123456789", "--nostore", "--noreset", "--dryrun", "--noprompt", "--configfile", "config.json",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_security_writekey_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.security.writekey(
      sign_keyfile="s.pem", command_keyfile="c.pem", decrypt_keyfile="d.pem",
      reset=False, store=False, prompt=False, dryrun=True,
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "security", "writekey",
      "--serialno", "123456789", "--sign", "s.pem", "--command", "c.pem", "--decrypt", "d.pem",
      "--noreset", "--nostore", "--noprompt", "--dryrun",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_security_writeregionconfig_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.security.writeregionconfig("region.json", reset=False)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "security", "writeregionconfig", "region.json",
      "--serialno", "123456789", "--noreset",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)
