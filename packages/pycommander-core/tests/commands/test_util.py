import unittest

from tests.mock_commander import MockCommander


class TestUtil(unittest.TestCase):
  def test_util_appinfo_command(self):
    commander = MockCommander()
    commander.util.appinfo("app.s37")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "util", "appinfo", "app.s37", "--json"]
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
