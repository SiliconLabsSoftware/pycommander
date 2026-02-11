import unittest

from tests.mock_commander import MockCommander


class TestVerify(unittest.TestCase):
  def test_verify(self):
    commander = MockCommander(serial_number="123456789")
    commander.verify.verify(
      ["app.s37", "boot.s37"],
      address=0x08000000,
      tokens=["TOKEN_A:1"],
      tokenfiles=["tokens.json"],
      tokengroup="zigbee",
      reset=False,
      regions=["@main"],
      binary=True,
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "verify", "app.s37", "boot.s37",
      "--serialno", "123456789",
      "--address", "0x08000000", "--token", "TOKEN_A:1", "--tokenfile", "tokens.json", "--tokengroup", "zigbee",
      "--noreset", "--region", "@main", "--binary",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_verify_blank(self):
    commander = MockCommander(serial_number="123456789")
    commander.verify.verify(filenames=None, blank=True, regions=["@main"])
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "verify",
      "--serialno", "123456789", "--blank", "--region", "@main",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)
