from re import A
import unittest


from pycommander_core.device import Device
from pycommander_core.runner import RunnerResult
from pycommander_core.types import AdapterInfo, AdapterBoardInfo, AdapterFwInfo

from tests.mock_adapter import MockAdapter
from tests.mock_commander import MockCommander

class TestAdapterBase(unittest.TestCase):
  def test_adapter_base_info(self):
    adapter = MockAdapter(serial_number="123456789", target_device="EFR32MG24B020F1536IM48")
    
    adapter._commander._runner.queue_result(
      RunnerResult(
        0,
"""
{
    "result": {
        "board_lists": [
            {
                "name": "Wireless Pro Kit Mainboard",
                "part_number": "BRD4002A Rev. A06",
                "serial_number": "233216889"
            },
            {
                "name": "EFR32xG24 2.4 GHz 20 dBm Radio Board",
                "part_number": "BRD4187B Rev. A00",
                "serial_number": "213200173",
                "target_device": "EFR32MG24B020F1536IM48-A"
            }
        ],
        "firmware_info": {
            "fw_version": "2v0p1b410",
            "new_fw_version": "2v0p1",
            "upgrade_available": false
        },
        "kit_info": {
            "aem_supported": true,
            "debug_mode": "MCU",
            "debug_part": "EFR32MG24B020F1536IM48-A",
            "ip_address": "10.5.161.83",
            "ip_supported": true,
            "j_link_serial": 123456789,
            "kit_name": "Wireless Pro Kit",
            "kit_part_number": "",
            "mac_address": "D0:CF:5E:01:E1:29",
            "vcom_port": "tty.usbmodem0001234567891",
            "vcom_supported": true
        }
    },
    "success": true
}
"""
    )
  )

    expected_adapter_info : AdapterInfo = AdapterInfo(
      board_list=[
        AdapterBoardInfo(
          name="Wireless Pro Kit Mainboard",
          part_number="BRD4002A Rev. A06",
          serial_number="233216889",
        ),
        AdapterBoardInfo(
          name="EFR32xG24 2.4 GHz 20 dBm Radio Board",
          part_number="BRD4187B Rev. A00",
          serial_number="213200173",
          target_device="EFR32MG24B020F1536IM48-A",
        ),
      ],
      fw_info=AdapterFwInfo(
        current_version="2v0p1b410",
        latest_version="2v0p1",
        upgrade_available=False,
      ),
      jlink_serial_number=123456789,
      vcom_port="tty.usbmodem0001234567891",
      vcom_supported=True,
      ip_supported=True,
      ip_address="10.5.161.83",
      mac_address="D0:CF:5E:01:E1:29",
      kit_name="Wireless Pro Kit",
      kit_part_number="",
      aem_supported=True,
      debug_mode="MCU",
      debug_part="EFR32MG24B020F1536IM48-A",
    )

    self.assertEqual(adapter.info(), expected_adapter_info)
    self.assertEqual(adapter._commander._runner.logged_commands, [["mock", "adapter", "probe", "--serialno", "123456789", "--json"]])

  def test_adapter_base_info_failed(self):
    adapter = MockAdapter(serial_number="123456789", target_device="EFR32MG24B020F1536IM48")
    
    adapter._commander._runner.queue_result(
      RunnerResult(
        254,
        '{"success": false, "error": "Failed to get adapter information"}'
      )
    )
    
    self.assertEqual(adapter.info(), None)
    self.assertEqual(adapter._commander._runner.logged_commands, [["mock", "adapter", "probe", "--serialno", "123456789", "--json"]])

  def test_adapter_base_no_board_lists(self):
    adapter = MockAdapter(serial_number="123456789", target_device="EFR32MG24B020F1536IM48")
    
    adapter._commander._runner.queue_result(
      RunnerResult(
        0,
"""
{
    "result": {
        "firmware_info": {
            "fw_version": "2v0p1b410",
            "new_fw_version": "2v0p1",
            "upgrade_available": false
        },
        "kit_info": {
            "aem_supported": true,
            "debug_mode": "MCU",
            "debug_part": "EFR32MG24B020F1536IM48-A",
            "ip_address": "10.5.161.83",
            "ip_supported": true,
            "j_link_serial": 123456789,
            "kit_name": "Wireless Pro Kit",
            "kit_part_number": "",
            "mac_address": "D0:CF:5E:01:E1:29",
            "vcom_port": "tty.usbmodem0001234567891",
            "vcom_supported": true
        }
    },
    "success": true
}
"""
      )
    )
    
    self.assertEqual(adapter.info(), None)
    self.assertEqual(adapter._commander._runner.logged_commands, [["mock", "adapter", "probe", "--serialno", "123456789", "--json"]])

  def test_adapter_base_no_firmware_info(self):
    adapter = MockAdapter(serial_number="123456789", target_device="EFR32MG24B020F1536IM48")
    
    adapter._commander._runner.queue_result(
      RunnerResult(
        0,
"""
{
    "result": {
        "board_lists": [
            {
                "name": "Wireless Pro Kit Mainboard",
                "part_number": "BRD4002A Rev. A06",
                "serial_number": "233216889"
            },
            {
                "name": "EFR32xG24 2.4 GHz 20 dBm Radio Board",
                "part_number": "BRD4187B Rev. A00",
                "serial_number": "213200173",
                "target_device": "EFR32MG24B020F1536IM48-A"
            }
        ],
        "kit_info": {
            "aem_supported": true,
            "debug_mode": "MCU",
            "debug_part": "EFR32MG24B020F1536IM48-A",
            "ip_address": "10.5.161.83",
            "ip_supported": true,
            "j_link_serial": 123456789,
            "kit_name": "Wireless Pro Kit",
            "kit_part_number": "",
            "mac_address": "D0:CF:5E:01:E1:29",
            "vcom_port": "tty.usbmodem0001234567891",
            "vcom_supported": true
        }
    },
    "success": true
}
"""
      )
    )
    
    self.assertEqual(adapter.info(), None)
    self.assertEqual(adapter._commander._runner.logged_commands, [["mock", "adapter", "probe", "--serialno", "123456789", "--json"]])

  def test_adapter_base_no_kit_info(self):
    adapter = MockAdapter(serial_number="123456789", target_device="EFR32MG24B020F1536IM48")
    
    adapter._commander._runner.queue_result(
      RunnerResult(
        0,
"""
{
    "result": {
        "board_lists": [
            {
                "name": "Wireless Pro Kit Mainboard",
                "part_number": "BRD4002A Rev. A06",
                "serial_number": "233216889"
            },
            {
                "name": "EFR32xG24 2.4 GHz 20 dBm Radio Board",
                "part_number": "BRD4187B Rev. A00",
                "serial_number": "213200173",
                "target_device": "EFR32MG24B020F1536IM48-A"
            }
        ],
        "firmware_info": {
            "fw_version": "2v0p1b410",
            "new_fw_version": "2v0p1",
            "upgrade_available": false
        }
    },
    "success": true
}
"""
      )
    )
    
    self.assertEqual(adapter.info(), None)
    self.assertEqual(adapter._commander._runner.logged_commands, [["mock", "adapter", "probe", "--serialno", "123456789", "--json"]])