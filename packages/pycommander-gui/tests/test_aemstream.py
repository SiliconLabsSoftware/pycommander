import unittest

from pycommander_gui.aemstream import AemStream

class TestAemStream(unittest.TestCase):
  def test_aemstream_init_serial_number(self):
    stream = AemStream(serial_number="123456789")
    self.assertEqual(stream._commander._serial_number, "123456789")
    self.assertEqual(stream._commander._runner, stream._runner)
    self.assertEqual(stream._process, None)
    self.assertEqual(stream._args, ["aem", "dump", "--serialno", "123456789"])

  def test_aemstream_init_ip_address(self):
    stream = AemStream(ip_address="192.168.1.100")
    self.assertEqual(stream._commander._ip_address, "192.168.1.100")
    self.assertEqual(stream._commander._runner, stream._runner)
    self.assertEqual(stream._process, None)
    self.assertEqual(stream._args, ["aem", "dump", "--ip", "192.168.1.100"])
