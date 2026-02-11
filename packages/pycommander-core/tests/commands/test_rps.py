import unittest

from tests.mock_commander import MockCommander


class TestRps(unittest.TestCase):
  def test_rps_create(self):
    commander = MockCommander()
    commander.rps.create(
      "out.rps",
      encrypt_key="enc.key",
      mic_key="mic.key",
      iv_file="iv.bin",
      sign_keyfile="sign.pem",
      sha="sha256",
      extsign=True,
      address=0x08000000,
      app="app.s37",
      app_version=1,
      fw_info=2,
      include_sections=[".text"],
      exclude_sections=[".debug"],
      map_file="app.map",
      combinedimage=True,
      key_type="ecc-p256",
      new_key="new.key",
      prev_key="prev.key",
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "rps", "create", "out.rps",
      "--encrypt", "enc.key", "--mic", "mic.key", "--iv", "iv.bin", "--sign", "sign.pem", "--sha", "sha256",
      "--extsign",
      "--address", "0x08000000", "--app", "app.s37", "--app-version", "1", "--fw-info", "2",
      "--include-section", ".text", "--exclude-section", ".debug",
      "--map", "app.map", "--combinedimage",
      "--key-type", "ecc-p256", "--new-key", "new.key", "--prev-key", "prev.key",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_rps_convert(self):
    commander = MockCommander()
    commander.rps.convert(
      "out.rps",
      encrypt_key="enc.key",
      mic_key="mic.key",
      iv_file="iv.bin",
      sign_keyfile="sign.pem",
      sha="sha256",
      extsign=True,
      app="app.s37",
      nwpapp="nwp.s37",
      app_version=1,
      fw_info=2,
      combinedimage=True,
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "rps", "convert", "out.rps",
      "--encrypt", "enc.key", "--mic", "mic.key", "--iv", "iv.bin", "--sign", "sign.pem", "--sha", "sha256",
      "--extsign",
      "--app", "app.s37", "--nwpapp", "nwp.s37", "--app-version", "1", "--fw-info", "2", "--combinedimage",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_rps_load(self):
    commander = MockCommander(serial_number="123456789")
    commander.rps.load("file.rps", eraseapp=True)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "rps", "load", "file.rps", "--serialno", "123456789", "--eraseapp", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_rps_sign(self):
    commander = MockCommander()
    commander.rps.sign("in.rps", "sig.der", outfile="signed.rps")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "rps", "sign", "in.rps", "--signature", "sig.der", "--outfile", "signed.rps",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)
