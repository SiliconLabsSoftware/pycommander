import unittest

from ..mock_commander import MockCommander


class TestGbl3(unittest.TestCase):
  def test_gbl3_aat_usageinfo_command(self):
    commander = MockCommander()
    commander.gbl3.aat_usageinfo()
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "gbl3", "aat-usageinfo", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_gbl3_create_command(self):
    commander = MockCommander()
    commander.gbl3.create(
      "out.gbl3",
      app="app.s37",
      bootloader="boot.s37",
      seupgrade="se.s37",
      metadata="meta.bin",
      compress="lz4",
      certificate="cert.der",
      include_sections=[".text"],
      exclude_sections=[".debug"],
      seunencrypted=True,
      dep_app="1.0.0",
      dep_boot="2.0.0",
      dep_se="3.0.0",
      delta_app="delta.s37",
      sign_keyfile="key.pem",
      encrypt_keyfile="enc.key",
      extsign=True,
      signature="sig.der",
      verify_keyfile="pub.pem",
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "gbl3", "create", "out.gbl3",
      "--app", "app.s37", "--bootloader", "boot.s37", "--seupgrade", "se.s37", "--metadata", "meta.bin",
      "--compress", "lz4", "--certificate", "cert.der",
      "--include-section", ".text", "--exclude-section", ".debug",
      "--seunencrypted",
      "--dep-app", "1.0.0", "--dep-boot", "2.0.0", "--dep-se", "3.0.0", "--delta-app", "delta.s37",
      "--sign", "key.pem", "--encrypt", "enc.key", "--extsign", "--signature", "sig.der", "--verify", "pub.pem",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_gbl3_keyconvert_command(self):
    commander = MockCommander()
    commander.gbl3.keyconvert("pub.pem", type="ecc-p256", outfile="tok.dat")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "gbl3", "keyconvert", "pub.pem", "--type", "ecc-p256", "--outfile", "tok.dat", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_gbl3_keygen_command(self):
    commander = MockCommander()
    commander.gbl3.keygen("ecc-p256", outfile="key.pem")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "gbl3", "keygen", "--type", "ecc-p256", "--outfile", "key.pem", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_gbl3_parse_command(self):
    commander = MockCommander()
    commander.gbl3.parse(
      "in.gbl3",
      app="app.s37",
      bootloader="boot.s37",
      seupgrade="se.s37",
      metadata="meta.bin",
      verify_keyfile="pub.pem",
      decrypt_keyfile="dec.key",
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "gbl3", "parse", "in.gbl3",
      "--app", "app.s37", "--bootloader", "boot.s37", "--seupgrade", "se.s37", "--metadata", "meta.bin",
      "--verify", "pub.pem", "--decrypt", "dec.key",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_gbl3_sign_command(self):
    commander = MockCommander()
    commander.gbl3.sign("unsigned.gbl3", "signed.gbl3", "sig.der", verify_keyfile="pub.pem")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "gbl3", "sign", "unsigned.gbl3",
      "--outfile", "signed.gbl3", "--signature", "sig.der", "--verify", "pub.pem",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)
