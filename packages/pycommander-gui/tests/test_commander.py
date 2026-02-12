import unittest

from pathlib import Path

from pycommander_core.paths import EXECUTABLE_PATH_GUI
from pycommander_gui.commander import Commander

class TestCommander(unittest.TestCase):
  def test_commander_gui_executable_path(self):
    commander = Commander()
    self.assertEqual(commander._runner._executable, EXECUTABLE_PATH_GUI)
    self.assertTrue(commander._runner._executable.exists())

  def test_commander_gui_all_options_passed(self):
    commander = Commander(
      serial_number="123456789",
      ip_address="192.168.1.1",
      serial_port="COM1",
      debug_speed=115200,
      debug_tif="TIF1",
      debug_irpre=1,
      debug_drpre=1,
      log_file_path=Path("test.log"),
      executable_path=Path("derp"),
    )

    self.assertEqual(commander._serial_number, "123456789")
    self.assertEqual(commander._ip_address, "192.168.1.1")
    self.assertEqual(commander._serial_port, "COM1")
    self.assertEqual(commander._debug_speed, 115200)
    self.assertEqual(commander._debug_tif, "TIF1")
    self.assertEqual(commander._debug_irpre, 1)
    self.assertEqual(commander._debug_drpre, 1)
    self.assertEqual(commander._runner._log_file_path, Path("test.log"))
    self.assertEqual(commander._runner._executable, Path("derp"))
