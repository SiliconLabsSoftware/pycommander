import unittest

from ..mock_commander import MockCommander


class TestConvert(unittest.TestCase):
  def test_convert_command(self):
    commander = MockCommander()
    commander.convert.convert(
      ["a.bin", "b.hex"],
      outfile="out.s37",
      address=0x08000000,
      ranges=[(0x0, 0x1000)],
      tokens=["TOKEN_A:1"],
      tokengroup="zigbee",
      secureboot=True,
      keyfile="key.pem",
      crc=True,
      include_sections=[".text"],
      exclude_sections=[".debug"],
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "convert", "a.bin", "b.hex",
      "--outfile", "out.s37",
      "--address", "0x08000000",
      "--range", "0x00000000:0x00001000",
      "--token", "TOKEN_A:1",
      "--tokengroup", "zigbee",
      "--secureboot", "--keyfile", "key.pem", "--crc",
      "--include-section", ".text", "--exclude-section", ".debug",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_convert_command_with_patches_tokenfiles_and_signing(self):
    commander = MockCommander()
    commander.convert.convert(
      ["app.bin"],
      patches=[(0x100, 0xAB, 1)],
      tokenfiles=["tokens.json"],
      tokendefs="defs.json",
      certificate="cert.pem",
      aeskey="aes.key",
      extsign=True,
      signature="sig.der",
      verify_key="pub.pem",
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "convert", "app.bin",
      "--patch", "0x00000100:0x000000AB:1",
      "--tokenfile", "tokens.json",
      "--tokendefs", "defs.json",
      "--certificate", "cert.pem",
      "--aeskey", "aes.key",
      "--extsign",
      "--signature", "sig.der",
      "--verify", "pub.pem",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)
