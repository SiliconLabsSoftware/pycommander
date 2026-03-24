import unittest

from ..mock_commander import MockCommander


class TestVerify(unittest.TestCase):
  def test_verify_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.verify.verify(
      ["app.s37", "boot.s37"],
      address=0x08000000,
      patches=[(0x100, 0xAB, 1)],
      tokens=[("TOKEN_A", "1")],
      tokenfiles=["tokens.json"],
      tokengroup="zigbee",
      tokendefs="defs.json",
      reset=False,
      regions=["@main"],
      binary=True,
      device="EFR32MG24",
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "verify", "app.s37", "boot.s37",
      "--serialno", "123456789", "--device", "EFR32MG24",
      "--address", "0x08000000",
      "--patch", "0x00000100:0x000000AB:1",
      "--token", "TOKEN_A:1", "--tokenfile", "tokens.json", "--tokengroup", "zigbee",
      "--tokendefs", "defs.json",
      "--noreset", "--region", "@main", "--binary",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_verify_command_blank(self):
    commander = MockCommander(serial_number="123456789")
    commander.verify.verify(filenames=None, blank=True, regions=["@main"])
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "verify",
      "--serialno", "123456789", "--blank", "--region", "@main",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)
