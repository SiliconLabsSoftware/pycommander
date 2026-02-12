import unittest

from tests.mock_commander import MockCommander


class TestSecurity(unittest.TestCase):
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

  def test_security_gencert_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.security.gencert(outfile="cert.der", store=False, extsign=True)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "security", "gencert",
      "--serialno", "123456789", "--outfile", "cert.der", "--nostore", "--extsign",
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

  def test_security_unlock_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.security.unlock(reset=False, store=False, cert="c.pem", authorization="auth.dat")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "security", "unlock",
      "--serialno", "123456789", "--noreset", "--nostore", "--cert", "c.pem", "--authorization", "auth.dat",
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

  def test_security_writekey_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.security.writekey(sign_keyfile="s.pem", command_keyfile="c.pem", reset=False, dryrun=True)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "security", "writekey",
      "--serialno", "123456789", "--sign", "s.pem", "--command", "c.pem", "--noreset", "--dryrun",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)
