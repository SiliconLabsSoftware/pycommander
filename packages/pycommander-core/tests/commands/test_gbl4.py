import unittest

from tests.mock_commander import MockCommander


class TestGbl4(unittest.TestCase):
  def test_gbl4_create(self):
    commander = MockCommander()
    commander.gbl4.create(
      "out.gbl4",
      config="config.yaml",
      data=["app.s37"],
      seupgrade="se.s37",
      encrypt_keyfile="key.bin",
      compress="lz4",
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
      "--encrypt", "key.bin", "--compress", "lz4", "--sign", "key.pem", "--extsign",
      "--productid", "0123456789ABCDEF", "--bundleversion", "1.0.0", "--minversion", "0.9.0",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_gbl4_createconfig(self):
    commander = MockCommander()
    commander.gbl4.createconfig("config.yaml")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "gbl4", "createconfig", "--outfile", "config.yaml", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_gbl4_info(self):
    commander = MockCommander()
    commander.gbl4.info("file.gbl4")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "gbl4", "info", "file.gbl4", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_gbl4_parse(self):
    commander = MockCommander()
    commander.gbl4.parse("in.gbl4", seupgrade="se.s37", outfile="out.s37")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "gbl4", "parse", "in.gbl4", "--seupgrade", "se.s37", "--outfile", "out.s37", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_gbl4_sign(self):
    commander = MockCommander()
    commander.gbl4.sign("unsigned.gbl4", "sig.der", "signed.gbl4", verify_keyfile="pub.pem")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "gbl4", "sign", "unsigned.gbl4",
      "--signature", "sig.der", "--outfile", "signed.gbl4", "--verify", "pub.pem",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)
