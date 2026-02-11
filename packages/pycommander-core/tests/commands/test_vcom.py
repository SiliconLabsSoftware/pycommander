import unittest

from tests.mock_commander import MockCommander


class TestVcom(unittest.TestCase):
  def test_vcom_config(self):
    commander = MockCommander(serial_number="123456789")
    commander.vcom.config(baudrate=115200, handshake="rtscts", store=True)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "vcom", "config",
      "--serialno", "123456789", "--baudrate", "115200", "--handshake", "rtscts", "--store",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)
