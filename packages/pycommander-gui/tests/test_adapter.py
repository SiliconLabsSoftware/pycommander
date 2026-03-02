import unittest
import shutil

from pathlib import Path

from pycommander_gui.adapter import Adapter
from pycommander_gui.commander import Commander
from pycommander_core.target import Target

class TestAdapter(unittest.TestCase):
  def test_adapter_no_commander_missing_connection_arguments(self):
    with self.assertRaisesRegex(ValueError, "Either serial_number, ip_address, or serial_port must be provided"):
      Adapter(target_device="EFR32MG24", debug_speed=1000, debug_tif="SWD", debug_irpre=1, debug_drpre=1)

  def test_adapter_no_commander_with_serial_number(self):
    adapter = Adapter(serial_number="123456789", target_device="EFR32MG24", debug_speed=1000, debug_tif="SWD", debug_irpre=1, debug_drpre=1)
    self.assertEqual(adapter._commander._serial_number, "123456789")
    self.assertEqual(adapter._commander._debug_speed, 1000)
    self.assertEqual(adapter._commander._debug_tif, "SWD")
    self.assertEqual(adapter._commander._debug_irpre, 1)
    self.assertEqual(adapter._commander._debug_drpre, 1)

  def test_adapter_no_commander_with_ip_address(self):
    adapter = Adapter(ip_address="192.168.1.100", target_device="EFR32MG24", debug_speed=1000, debug_tif="SWD", debug_irpre=1, debug_drpre=1)
    self.assertEqual(adapter._commander._ip_address, "192.168.1.100")
    self.assertEqual(adapter._commander._debug_speed, 1000)
    self.assertEqual(adapter._commander._debug_tif, "SWD")
    self.assertEqual(adapter._commander._debug_irpre, 1)
    self.assertEqual(adapter._commander._debug_drpre, 1)

  def test_adapter_no_commander_with_serial_port(self):
    adapter = Adapter(serial_port="/dev/tty.usbmodem141101", target_device="EFR32MG24", debug_speed=1000, debug_tif="SWD", debug_irpre=1, debug_drpre=1)
    self.assertEqual(adapter._commander._serial_port, "/dev/tty.usbmodem141101")
    self.assertEqual(adapter._commander._debug_speed, 1000)
    self.assertEqual(adapter._commander._debug_tif, "SWD")
    self.assertEqual(adapter._commander._debug_irpre, 1)
    self.assertEqual(adapter._commander._debug_drpre, 1)

  def test_adapter_yes_commander_missing_target_device(self):
    command = shutil.which("echo")
    if command is None:
      self.fail("echo command not found")

    commander = Commander(serial_number="123456789", executable_path=command)

    with self.assertRaisesRegex(ValueError, "target_device must be provided"):
      Adapter(commander=commander)

  def test_adapter_yes_commander_and_target_device(self):
    command = shutil.which("echo")
    if command is None:
      self.fail("echo command not found")

    commander = Commander(serial_number="123456789", executable_path=command)
    adapter = Adapter(commander=commander, target_device="EFR32MG24")

    self.assertTrue(isinstance(adapter._commander, Commander))
    self.assertTrue(isinstance(adapter.target, Target))
