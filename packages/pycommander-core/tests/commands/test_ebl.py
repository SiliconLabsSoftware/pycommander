import unittest

from tests.mock_commander import MockCommander


class TestEbl(unittest.TestCase):
  def test_ebl_aat_usageinfo(self):
    commander = MockCommander()
    commander.ebl.aat_usageinfo()
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "ebl", "aat-usageinfo", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_ebl_create(self):
    commander = MockCommander()
    commander.ebl.create("out.ebl", app="app.s37", sign_keyfile="key.pem")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "ebl", "create", "out.ebl", "--app", "app.s37", "--sign", "key.pem", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_ebl_keyconvert(self):
    commander = MockCommander()
    commander.ebl.keyconvert("pub.pem", type="ecc-p256", outfile="token.dat")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "ebl", "keyconvert", "pub.pem", "--type", "ecc-p256", "--outfile", "token.dat", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_ebl_keygen(self):
    commander = MockCommander()
    commander.ebl.keygen("aes-ccm", outfile="key.bin")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "ebl", "keygen", "--type", "aes-ccm", "--outfile", "key.bin", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_ebl_parse(self):
    commander = MockCommander()
    commander.ebl.parse("in.ebl", app="app.s37", verify_keyfile="pub.pem")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "ebl", "parse", "in.ebl", "--app", "app.s37", "--verify", "pub.pem", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_ebl_print(self):
    commander = MockCommander()
    commander.ebl.print("file.ebl")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "ebl", "print", "file.ebl", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)
