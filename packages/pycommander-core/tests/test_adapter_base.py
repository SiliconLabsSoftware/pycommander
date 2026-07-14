"""
License
Copyright 2026 Silicon Laboratories Inc. www.silabs.com
*******************************************************************************
The licensor of this software is Silicon Laboratories Inc. Your use of this
software is governed by the terms of Silicon Labs Master Software License
Agreement (MSLA) available at
www.silabs.com/about-us/legal/master-software-license-agreement. This
software is distributed to you in Source Code format and is governed by the
sections of the MSLA applicable to Source Code.
*******************************************************************************
"""

import json
import unittest

from pathlib import Path

from pycommander_core.target import Target
from pycommander_core.adapter_base import AdapterBase
from pycommander_core.runner import RunnerResult
from pycommander_core.types import *

from .mock_adapter import MockAdapter
from .mock_commander import MockCommander

class TestAdapterBase(unittest.TestCase):
  def test_adapter_base_init(self):
    mock_commander = MockCommander(serial_number="123456789")
    mock_device = Target(part_number="EFR32MG24B020F1536IM48", commander=mock_commander)
    adapter = AdapterBase(commander=mock_commander, target=mock_device)

    self.assertEqual(adapter._commander, mock_commander)
    self.assertEqual(adapter.target, mock_device)

  def test_adapter_base_init_failed(self):
    with self.assertRaises(ValueError):
      AdapterBase(commander=None, target=None)

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
            "nickname": "Adapter 1",
            "vcom_port": "tty.usbmodem0001234567891",
            "vcom_supported": true
        }
    },
    "success": true
}
"""
    , "")
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
      nickname="Adapter 1",
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
      , "")
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
            "nickname": "Adapter 1",
            "vcom_port": "tty.usbmodem0001234567891",
            "vcom_supported": true
        }
    },
    "success": true
}
"""
      , "")
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
            "nickname": "Adapter 1",
            "vcom_port": "tty.usbmodem0001234567891",
            "vcom_supported": true
        }
    },
    "success": true
}
"""
      , "")
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
      , "")
    )
    
    self.assertEqual(adapter.info(), None)
    self.assertEqual(adapter._commander._runner.logged_commands, [["mock", "adapter", "probe", "--serialno", "123456789", "--json"]])

  def test_adapter_base_reset(self):
    adapter = MockAdapter(serial_number="123456789", target_device="EFR32MG24B020F1536IM48")
    
    adapter._commander._runner.queue_result(
      RunnerResult(
        0,
"""
{
    "success": true
}
"""
      , "")
    )
    self.assertEqual(adapter.reset(), True)
    self.assertEqual(adapter._commander._runner.logged_commands, [["mock", "adapter", "reset", "--serialno", "123456789", "--json"]])

  def test_adapter_base_reset_failed(self):
    adapter = MockAdapter(serial_number="123456789", target_device="EFR32MG24B020F1536IM48")
    
    adapter._commander._runner.queue_result(
      RunnerResult(
        254,
"""
{
    "success": false
}
"""
      , "")
    )
    self.assertEqual(adapter.reset(), False)
    self.assertEqual(adapter._commander._runner.logged_commands, [["mock", "adapter", "reset", "--serialno", "123456789", "--json"]])

  def test_adapter_base_upgradeFirmware_with_file(self):
    adapter = MockAdapter(serial_number="123456789", target_device="EFR32MG24B020F1536IM48")

    # probe (current version)
    adapter._commander._runner.queue_result(
      RunnerResult(
        0,
        '{"result": {"firmware_info": {"fw_version": "1v0p0"}}, "success": true}'
      , "")
    )
    # fwupgrade
    adapter._commander._runner.queue_result(
      RunnerResult(
        0,
        '{"success": true}'
      , "")
    )
    # probe (new version)
    adapter._commander._runner.queue_result(
      RunnerResult(
        0,
        '{"result": {"firmware_info": {"fw_version": "2v0p1"}}, "success": true}'
      , "")
    )

    self.assertEqual(
      adapter.upgradeFirmware(filename=Path("firmware.emz")),
      AdapterFwUpgradeResult(
        package_was_installed=True,
        currently_installed_version="2v0p1",
      ),
    )
    self.assertEqual(adapter._commander._runner.logged_commands, [
      ["mock", "adapter", "probe", "--serialno", "123456789", "--json"],
      ["mock", "adapter", "fwupgrade", "firmware.emz", "--serialno", "123456789", "--json"],
      ["mock", "adapter", "probe", "--serialno", "123456789", "--json"],
    ])

  def test_adapter_base_upgradeFirmware_with_empty_filename(self):
    adapter = MockAdapter(serial_number="123456789", target_device="EFR32MG24B020F1536IM48")

    # probe (current version)
    adapter._commander._runner.queue_result(
      RunnerResult(
        0,
        '{"result": {"firmware_info": {"fw_version": "1v0p0"}}, "success": true}'
      , "")
    )
    # fwupgradecheck
    adapter._commander._runner.queue_result(
      RunnerResult(
        0,
        '{"result": {"upgrade_available": true}, "success": true}'
      , "")
    )
    # fwupgrade
    adapter._commander._runner.queue_result(
      RunnerResult(
        0,
        '{"success": true}'
      , "")
    )
    # probe (new version)
    adapter._commander._runner.queue_result(
      RunnerResult(
        0,
        '{"result": {"firmware_info": {"fw_version": "2v0p1"}}, "success": true}'
      , "")
    )

    self.assertEqual(
      adapter.upgradeFirmware(filename=""),
      AdapterFwUpgradeResult(
      package_was_installed=True,
      currently_installed_version="2v0p1",
    ))
    self.assertEqual(adapter._commander._runner.logged_commands, [
      ["mock", "adapter", "probe", "--serialno", "123456789", "--json"],
      ["mock", "adapter", "fwupgradecheck", "--serialno", "123456789", "--json"],
      ["mock", "adapter", "fwupgrade", "--serialno", "123456789", "--json"],
      ["mock", "adapter", "probe", "--serialno", "123456789", "--json"],
    ])

  def test_adapter_base_upgradeFirmware_with_file_failed(self):
    adapter = MockAdapter(serial_number="123456789", target_device="EFR32MG24B020F1536IM48")

    # probe (current version)
    adapter._commander._runner.queue_result(
      RunnerResult(
        0,
        '{"result": {"firmware_info": {"fw_version": "1v0p0"}}, "success": true}'
      , "")
    )
    # fwupgrade
    adapter._commander._runner.queue_result(
      RunnerResult(
        254,
        '{"success": false}'
      , "")
    )

    self.assertEqual(adapter.upgradeFirmware(filename=Path("firmware.emz")), None)
    self.assertEqual(adapter._commander._runner.logged_commands, [
      ["mock", "adapter", "probe", "--serialno", "123456789", "--json"],
      ["mock", "adapter", "fwupgrade", "firmware.emz", "--serialno", "123456789", "--json"],
    ])

  def test_adapter_base_upgradeFirmware_bundled(self):
    adapter = MockAdapter(serial_number="123456789", target_device="EFR32MG24B020F1536IM48")

    # probe (current version)
    adapter._commander._runner.queue_result(
      RunnerResult(
        0,
        '{"result": {"firmware_info": {"fw_version": "1v0p0"}}, "success": true}'
      , "")
    )
    # fwupgradecheck
    adapter._commander._runner.queue_result(
      RunnerResult(
        0,
        '{"result": {"upgrade_available": true}, "success": true}'
      , "")
    )
    # fwupgrade
    adapter._commander._runner.queue_result(
      RunnerResult(
        0,
        '{"success": true}'
      , "")
    )
    # probe (new version)
    adapter._commander._runner.queue_result(
      RunnerResult(
        0,
        '{"result": {"firmware_info": {"fw_version": "2v0p1"}}, "success": true}'
      , "")
    )

    self.assertEqual(
      adapter.upgradeFirmware(),
      AdapterFwUpgradeResult(
        package_was_installed=True,
        currently_installed_version="2v0p1",
      ),
    )
    self.assertEqual(adapter._commander._runner.logged_commands, [
      ["mock", "adapter", "probe", "--serialno", "123456789", "--json"],
      ["mock", "adapter", "fwupgradecheck", "--serialno", "123456789", "--json"],
      ["mock", "adapter", "fwupgrade", "--serialno", "123456789", "--json"],
      ["mock", "adapter", "probe", "--serialno", "123456789", "--json"],
    ])

  def test_adapter_base_upgradeFirmware_bundled_no_upgrade_available(self):
    adapter = MockAdapter(serial_number="123456789", target_device="EFR32MG24B020F1536IM48")

    # probe (current version)
    adapter._commander._runner.queue_result(
      RunnerResult(
        0,
        '{"result": {"firmware_info": {"fw_version": "2v0p1"}}, "success": true}'
      , "")
    )
    # fwupgradecheck
    adapter._commander._runner.queue_result(
      RunnerResult(
        0,
        '{"result": {"upgrade_available": false}, "success": true}'
      , "")
    )

    self.assertEqual(
      adapter.upgradeFirmware(),
      AdapterFwUpgradeResult(
        package_was_installed=False,
        currently_installed_version="2v0p1",
      ),
    )
    self.assertEqual(adapter._commander._runner.logged_commands, [
      ["mock", "adapter", "probe", "--serialno", "123456789", "--json"],
      ["mock", "adapter", "fwupgradecheck", "--serialno", "123456789", "--json"],
    ])

  def test_adapter_base_upgradeFirmware_bundled_check_failed(self):
    adapter = MockAdapter(serial_number="123456789", target_device="EFR32MG24B020F1536IM48")

    # probe (current version)
    adapter._commander._runner.queue_result(
      RunnerResult(
        0,
        '{"result": {"firmware_info": {"fw_version": "1v0p0"}}, "success": true}'
      , "")
    )
    # fwupgradecheck
    adapter._commander._runner.queue_result(
      RunnerResult(
        254,
        '{"success": false}'
      , "")
    )

    self.assertEqual(adapter.upgradeFirmware(), None)
    self.assertEqual(adapter._commander._runner.logged_commands, [
      ["mock", "adapter", "probe", "--serialno", "123456789", "--json"],
      ["mock", "adapter", "fwupgradecheck", "--serialno", "123456789", "--json"],
    ])

  def test_adapter_base_getVoltage(self):
    adapter = MockAdapter(serial_number="123456789", target_device="EFR32MG24B020F1536IM48")
    
    adapter._commander._runner.queue_result(
      RunnerResult(
        0,
"""
{
    "result": {
        "voltages": [
            {
                "configured_voltage_v": 3.299999952316284,
                "measured_voltage_v": 3.308469772338867,
                "rail_index": 0,
                "rail_powered": true
            }
        ]
    },
    "success": true
}
"""
      , "")
    )
    self.assertEqual(adapter.getVoltage(), AdapterVoltageInfo(
      rails=[
        AdapterRailInfo(
          rail_index=0,
          configured_voltage_v=3.299999952316284,
          measured_voltage_v=3.308469772338867,
          rail_powered=True,
        ),
      ],
    ))
    self.assertEqual(adapter._commander._runner.logged_commands, [["mock", "adapter", "voltage", "--serialno", "123456789", "--json"]])

  def test_adapter_base_getVoltage_multiple_rails(self):
    adapter = MockAdapter(serial_number="123456789", target_device="EFR32MG24B020F1536IM48")
    
    adapter._commander._runner.queue_result(
      RunnerResult(
        0,
"""
{
    "result": {
        "voltages": [
            {
                "configured_voltage_v": 3.299999952316284,
                "measured_voltage_v": 3.308469772338867,
                "rail_index": 0,
                "rail_powered": true
            },
            {
                "configured_voltage_v": 1.8,
                "measured_voltage_v": 1.8,
                "rail_index": 1,
                "rail_powered": false
            }
        ]
    },
    "success": true
}
"""
      , "")
    )

    expected_voltage_info : AdapterVoltageInfo = AdapterVoltageInfo(
      rails=[
        AdapterRailInfo(
          rail_index=0,
          configured_voltage_v=3.299999952316284,
          measured_voltage_v=3.308469772338867,
          rail_powered=True,
        ),
        AdapterRailInfo(
          rail_index=1,
          configured_voltage_v=1.8,
          measured_voltage_v=1.8,
          rail_powered=False,
        ),
      ],
    )

    self.assertEqual(adapter.getVoltage(), expected_voltage_info)
    self.assertEqual(adapter._commander._runner.logged_commands, [["mock", "adapter", "voltage", "--serialno", "123456789", "--json"]])

  def test_adapter_base_getVoltage_missing_one_rail_index(self):
    adapter = MockAdapter(serial_number="123456789", target_device="EFR32MG24B020F1536IM48")
    
    adapter._commander._runner.queue_result(
      RunnerResult(
        0,
"""
{
    "result": {
        "voltages": [
            {
                "configured_voltage_v": 3.299999952316284,
                "measured_voltage_v": 3.308469772338867,
                "rail_index": 0,
                "rail_powered": true
            },
            {
                "configured_voltage_v": 1.8,
                "measured_voltage_v": 1.8,
                "rail_powered": false
            }
        ]
    },
    "success": true
}
"""
      , "")
    )

    expected_voltage_info : AdapterVoltageInfo = AdapterVoltageInfo(
      rails=[
        AdapterRailInfo(
          rail_index=0,
          configured_voltage_v=3.299999952316284,
          measured_voltage_v=3.308469772338867,
          rail_powered=True,
        ),
        AdapterRailInfo(
          rail_index=None,
          configured_voltage_v=1.8,
          measured_voltage_v=1.8,
          rail_powered=False,
        ),
      ],
    )

    self.assertEqual(adapter.getVoltage(), expected_voltage_info)
    self.assertEqual(adapter._commander._runner.logged_commands, [["mock", "adapter", "voltage", "--serialno", "123456789", "--json"]])

  def test_adapter_base_getVoltage_failed(self):
    adapter = MockAdapter(serial_number="123456789", target_device="EFR32MG24B020F1536IM48")
    
    adapter._commander._runner.queue_result(
      RunnerResult(
        254,
"""
{
    "success": false
}
"""
      , "")
    )
    self.assertEqual(adapter.getVoltage(), None)

  def test_adapter_base_setVoltage(self):
    adapter = MockAdapter(serial_number="123456789", target_device="EFR32MG24B020F1536IM48")
    
    adapter._commander._runner.queue_result(
      RunnerResult(
        0,
"""
{
    "success": true
}
"""
      , "")
    )
    self.assertEqual(adapter.setVoltage(3.3), True)
    self.assertEqual(adapter._commander._runner.logged_commands, [["mock", "adapter", "voltage", "3.3", "--serialno", "123456789", "--json"]])

  def test_adapter_base_setVoltage_failed(self):
    adapter = MockAdapter(serial_number="123456789", target_device="EFR32MG24B020F1536IM48")
    
    adapter._commander._runner.queue_result(
      RunnerResult(
        254,
"""
{
    "success": false
}
"""
      , "")
    )
    self.assertEqual(adapter.setVoltage(3.3), False)
    self.assertEqual(adapter._commander._runner.logged_commands, [["mock", "adapter", "voltage", "3.3", "--serialno", "123456789", "--json"]])

  def test_adapter_base_setVcomConfig(self):
    adapter = MockAdapter(serial_number="123456789", target_device="EFR32MG24B020F1536IM48")
    
    adapter._commander._runner.queue_result(
      RunnerResult(
        0,
"""
{
    "success": true
}
"""
      , "")
    )
    self.assertEqual(adapter.setVcomConfig(baudrate=115200, handshake=VcomHandshake.RTSCTS, store=True), True)
    self.assertEqual(adapter._commander._runner.logged_commands, [
      ["mock", "vcom", "config", "--serialno", "123456789", "--baudrate", "115200", "--handshake", "rtscts", "--store", "--json"]
    ])

  def test_adapter_base_setVcomConfig_failed(self):
    adapter = MockAdapter(serial_number="123456789", target_device="EFR32MG24B020F1536IM48")
    
    adapter._commander._runner.queue_result(
      RunnerResult(
        254,
"""
{
    "success": false
}
"""
      , "")
    )
    self.assertEqual(adapter.setVcomConfig(baudrate=115200, handshake=VcomHandshake.RTSCTS, store=True), False)
    self.assertEqual(adapter._commander._runner.logged_commands, [
      ["mock", "vcom", "config", "--serialno", "123456789", "--baudrate", "115200", "--handshake", "rtscts", "--store", "--json"]
    ])

  def test_adapter_base_setVcomConfig_invalid_handshake(self):
    adapter = MockAdapter(serial_number="123456789", target_device="EFR32MG24B020F1536IM48")
    
    with self.assertRaises(ValueError):
      adapter.setVcomConfig(baudrate=115200, handshake="invalid", store=True)
    self.assertEqual(adapter._commander._runner.logged_commands, [])

  def test_adapter_base_analyzeEnergyUsage(self):
    adapter = MockAdapter(serial_number="123456789", target_device="EFR32MG24B020F1536IM48")

    test_json = Path(__file__).parent / "resources" / "aem_analyze" / "all.json"

    adapter._commander._runner.queue_result(
      RunnerResult(
        0,
        test_json.read_text()
      , "")
    )

    expected_aem_analysis_result : AemAnalysisResult = AemAnalysisResult(
      clustering=AemClustering(
        blocks=[
          AemClusterBlock(
            duration_ms=10010.876,
            end_ms=10010.876,
            level_mA=1.8975981200205052,
            max_mA=3.1142637599259615,
            min_mA=0.8984369924291968,
            range_mA=2.2158267674967647,
            samples=957696,
            start_ms=0,
          ),
        ],
        configuration=AemClusterConfiguration(
          false_alarm_probability=0.3,
          max_points=8000,
          min_segment_ms=25,
        ),
        method="bayesian_blocks_time_aware",
        total_blocks=1,
        type="clustering_analysis",
        unique_states=1,
      ),
      distribution=AemDistribution(
        bins=[
          AemDistributionBin(
            average_current=1.20966,
            bin_max=1.268,
            bin_min=0.898,
            current_unit="mA",
            num_samples=11918,
            percentage=1.24,
            standard_deviation=0.04979,
            time=124.58,
            time_unit="ms",
          ),
          AemDistributionBin(
            average_current=1.4887,
            bin_max=1.637,
            bin_min=1.268,
            current_unit="mA",
            num_samples=200152,
            percentage=20.9,
            standard_deviation=0.09698,
            time=2092.2,
            time_unit="ms",
          ),
          AemDistributionBin(
            average_current=1.84472,
            bin_max=2.006,
            bin_min=1.637,
            current_unit="mA",
            num_samples=467572,
            percentage=48.82,
            standard_deviation=0.09796,
            time=4887.57,
            time_unit="ms",
          ),
          AemDistributionBin(
            average_current=2.18105,
            bin_max=2.376,
            bin_min=2.006,
            current_unit="mA",
            num_samples=158381,
            percentage=16.54,
            standard_deviation=0.11033,
            time=1655.57,
            time_unit="ms",
          ),
          AemDistributionBin(
            average_current=2.48148,
            bin_max=2.745,
            bin_min=2.376,
            current_unit="mA",
            num_samples=119565,
            percentage=12.48,
            standard_deviation=0.05565,
            time=1249.82,
            time_unit="ms",
          ),
          AemDistributionBin(
            average_current=2.83663,
            bin_max=3.114,
            bin_min=2.745,
            current_unit="mA",
            num_samples=108,
            percentage=0.01,
            standard_deviation=0.07824,
            time=1.13,
            time_unit="ms",
          ),
        ],
        configuration=AemDistributionConfiguration(
          bins=6,
          logarithmic=False,
        ),
        summary=AemDistributionSummary(
          max_current=3.114,
          min_current=0.898,
          total_duration_ms=10010.871,
          total_samples=957696,
          unit="mA",
        ),
        type="distribution_analysis",
      ),
      period_detection=AemPeriodDetection(
        configuration=AemPeriodDetectionConfiguration(
          max_period_ms=3336.957,
          min_period_ms=5,
        ),
        result=AemPeriodDetectionResult(
          confidence=0.7,
          frequency_hz=0.672006881350465,
          interval_summary=AemPeriodDetectionIntervalSummary(
            average_mean_current_ma=1.89548635216511,
            average_peak_current_ma=2.960399352014065,
            max_period_ms=1723.781,
            min_period_ms=1462.1689999999999,
          ),
          intervals=[
            AemPeriodDetectionInterval(
              cycle=1,
              end_index=161334,
              end_ms=1636.38,
              mean_current_ma=1.8895799483840778,
              peak_current_ma=2.96447379514575,
              period_ms=1517.2,
              start_index=11534,
              start_ms=119.18,
            ),
            AemPeriodDetectionInterval(
              cycle=2,
              end_index=329104,
              end_ms=3360.161,
              mean_current_ma=1.9065092930951,
              peak_current_ma=2.9293037950992584,
              period_ms=1723.781,
              start_index=161334,
              start_ms=1636.38,
            ),
            AemPeriodDetectionInterval(
              cycle=3,
              end_index=468793,
              end_ms=4822.33,
              mean_current_ma=1.8944068558556009,
              peak_current_ma=2.9628875199705362,
              period_ms=1462.1689999999999,
              start_index=329104,
              start_ms=3360.161,
            ),
            AemPeriodDetectionInterval(
              cycle=4,
              end_index=617601,
              end_ms=6398.73,
              mean_current_ma=1.9014176508696041,
              peak_current_ma=2.9328842647373676,
              period_ms=1576.3999999999996,
              start_index=468793,
              start_ms=4822.33,
            ),
            AemPeriodDetectionInterval(
              cycle=5,
              end_index=760665,
              end_ms=7910.011,
              mean_current_ma=1.8855180126211657,
              peak_current_ma=3.0124473851174116,
              period_ms=1511.2810000000009,
              start_index=617601,
              start_ms=6398.73,
            ),
          ],
          is_periodic=True,
          jitter_relative=0.25,
          method="FFT Spectrum",
          method_results=[
            AemPeriodDetectionMethodResult(
              method="Edge Detection",
              detected=False,
            ),
            AemPeriodDetectionMethodResult(
              method="Autocorrelation",
              detected=False,
            ),
            AemPeriodDetectionMethodResult(
              confidence=1,
              detected=True,
              method="FFT Spectrum",
              period_ms=1488.08,
              relative_error=0,
            ),
          ],
          num_cycles=6,
          period_ms=1488.08,
        ),
        type="period_detection",
      ),
      signal_characteristics=AemSignalCharacteristics(
        average_voltage_v=3.31,
        dynamic_range_ratio=3,
        estimated_states=3,
        max_current_ma=3.114,
        min_current_ma=0.8984,
        noise_level_mad_sigma_ma=0.1093,
      ),
    )

    self.assertEqual(adapter.analyzeEnergyUsage(duration_s=10, get_distribution=True, cluster_states=True, detect_period=True), expected_aem_analysis_result)
    self.assertEqual(adapter._commander._runner.logged_commands, [["mock", "aem", "analyze", "--serialno", "123456789", "--windowlength", "10000", "--showdistribution", "--cluster", "--findperiod", "--json"]])

  def test_adapter_base_analyzeEnergyUsage_failed(self):
    adapter = MockAdapter(serial_number="123456789", target_device="EFR32MG24B020F1536IM48")
    
    adapter._commander._runner.queue_result(
      RunnerResult(
        254,
        """
        {
          "success": false
        }
        """
      , "")
    )
    self.assertEqual(adapter.analyzeEnergyUsage(duration_s=10, get_distribution=True, cluster_states=True, detect_period=True), None)
    self.assertEqual(adapter._commander._runner.logged_commands, [["mock", "aem", "analyze", "--serialno", "123456789", "--windowlength", "10000", "--showdistribution", "--cluster", "--findperiod", "--json"]])

  def test_adapter_base_analyzeEnergyUsage_invalid_options(self):
    adapter = MockAdapter(serial_number="123456789", target_device="EFR32MG24B020F1536IM48")
    
    with self.assertRaises(ValueError):
      adapter.analyzeEnergyUsage(duration_s=10, get_distribution=False, cluster_states=False, detect_period=False)
    self.assertEqual(adapter._commander._runner.logged_commands, [])


  def test_adapter_base_parse_aem_analyze_output_missing_result_key(self):
    self.assertIsNone(AdapterBase._AdapterBase__parse_aem_analyze_output({"success": True}))

  def test_adapter_base_parse_aem_analyze_output_empty_result(self):
    result = AdapterBase._AdapterBase__parse_aem_analyze_output({"result": {}})
    self.assertIsNotNone(result)
    self.assertIsNone(result.clustering)
    self.assertIsNone(result.distribution)
    self.assertIsNone(result.period_detection)
    self.assertIsNone(result.signal_characteristics)

  def test_adapter_base_parse_aem_analyze_output_clustering_only(self):
    data = json.loads((Path(__file__).parent / "resources" / "aem_analyze" / "clustering.json").read_text())
    result = AdapterBase._AdapterBase__parse_aem_analyze_output(data)

    self.assertIsNotNone(result)
    self.assertIsNotNone(result.clustering)
    self.assertIsNotNone(result.signal_characteristics)
    self.assertIsNone(result.distribution)
    self.assertIsNone(result.period_detection)

    self.assertEqual(len(result.clustering.blocks), 1)
    self.assertEqual(result.clustering.total_blocks, 1)
    self.assertEqual(result.clustering.method, "bayesian_blocks_time_aware")

  def test_adapter_base_parse_aem_analyze_output_distribution_only(self):
    data = json.loads((Path(__file__).parent / "resources" / "aem_analyze" / "distribution.json").read_text())
    result = AdapterBase._AdapterBase__parse_aem_analyze_output(data)

    self.assertIsNotNone(result)
    self.assertIsNotNone(result.distribution)
    self.assertIsNotNone(result.signal_characteristics)
    self.assertIsNone(result.clustering)
    self.assertIsNone(result.period_detection)

    self.assertEqual(len(result.distribution.bins), 6)
    self.assertEqual(result.distribution.configuration.bins, 6)
    self.assertEqual(result.distribution.summary.total_samples, 957696)

  def test_adapter_base_parse_aem_analyze_output_period_detection_only(self):
    data = json.loads( (Path(__file__).parent / "resources" / "aem_analyze" / "period-detection.json").read_text())
    result = AdapterBase._AdapterBase__parse_aem_analyze_output(data)

    self.assertIsNotNone(result)
    self.assertIsNotNone(result.period_detection)
    self.assertIsNotNone(result.signal_characteristics)
    self.assertIsNone(result.clustering)
    self.assertIsNone(result.distribution)

    self.assertTrue(result.period_detection.result.is_periodic)
    self.assertEqual(len(result.period_detection.result.intervals), 5)
    self.assertEqual(result.period_detection.result.num_cycles, 6)
    self.assertEqual(len(result.period_detection.result.method_results), 3)

  def test_adapter_base_get_current_firmware_version(self):
    adapter = MockAdapter(serial_number="123456789", target_device="EFR32MG24B020F1536IM48")

    adapter._commander._runner.queue_result(
      RunnerResult(
        0,
        '{"result": {"firmware_info": {"fw_version": "1v0p0"}}, "success": true}'
      , "")
    )

    self.assertEqual(adapter._AdapterBase__get_current_firmware_version(), "1v0p0")
    self.assertEqual(adapter._commander._runner.logged_commands, [["mock", "adapter", "probe", "--serialno", "123456789", "--json"]])

  def test_adapter_base_get_current_firmware_version_failed(self):
    adapter = MockAdapter(serial_number="123456789", target_device="EFR32MG24B020F1536IM48")

    adapter._commander._runner.queue_result(
      RunnerResult(
        254,
        '{"success": false}'
      , "")
    )

    self.assertIsNone(adapter._AdapterBase__get_current_firmware_version())
    self.assertEqual(adapter._commander._runner.logged_commands, [["mock", "adapter", "probe", "--serialno", "123456789", "--json"]])

  def test_adapter_base_get_current_firmware_version_missing_firmware_info(self):
    adapter = MockAdapter(serial_number="123456789", target_device="EFR32MG24B020F1536IM48")

    adapter._commander._runner.queue_result(
      RunnerResult(
        0,
        '{"result": {}, "success": true}'
      , "")
    )

    self.assertIsNone(adapter._AdapterBase__get_current_firmware_version())
    self.assertEqual(adapter._commander._runner.logged_commands, [["mock", "adapter", "probe", "--serialno", "123456789", "--json"]])
  