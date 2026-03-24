import unittest

from ..mock_commander import MockCommander


class TestEbl(unittest.TestCase):
  def test_ebl_aat_usageinfo_command(self):
    commander = MockCommander()
    commander.ebl.aat_usageinfo()
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "ebl", "aat-usageinfo", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_ebl_aat_usageinfo_command_with_device(self):
    commander = MockCommander()
    commander.ebl.aat_usageinfo(device="EFR32MG24")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "ebl", "aat-usageinfo", "--device", "EFR32MG24", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_ebl_create_command(self):
    commander = MockCommander()
    commander.ebl.create("out.ebl", app="app.s37", sign_keyfile="key.pem")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "ebl", "create", "out.ebl", "--app", "app.s37", "--sign", "key.pem", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_ebl_create_command_with_encrypt_extsign_signature_verify(self):
    commander = MockCommander()
    commander.ebl.create(
      "out.ebl",
      encrypt_keyfile="aes.key",
      extsign=True,
      signature="sig.der",
      verify_keyfile="pub.pem",
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "ebl", "create", "out.ebl",
      "--encrypt", "aes.key", "--extsign", "--signature", "sig.der", "--verify", "pub.pem",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_ebl_keyconvert_command(self):
    commander = MockCommander()
    commander.ebl.keyconvert("pub.pem", type="ecc-p256", outfile="token.dat")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "ebl", "keyconvert", "pub.pem", "--type", "ecc-p256", "--outfile", "token.dat", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_ebl_keygen_command(self):
    commander = MockCommander()
    commander.ebl.keygen("aes-ccm", outfile="key.bin")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "ebl", "keygen", "--type", "aes-ccm", "--outfile", "key.bin", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_ebl_parse_command(self):
    commander = MockCommander()
    commander.ebl.parse("in.ebl", app="app.s37", verify_keyfile="pub.pem")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "ebl", "parse", "in.ebl", "--app", "app.s37", "--verify", "pub.pem", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_ebl_parse_command_with_decrypt(self):
    commander = MockCommander()
    commander.ebl.parse("in.ebl", decrypt_keyfile="aes.key")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "ebl", "parse", "in.ebl", "--decrypt", "aes.key", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_ebl_print_command(self):
    commander = MockCommander()
    commander.ebl.print("file.ebl")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "ebl", "print", "file.ebl", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)
