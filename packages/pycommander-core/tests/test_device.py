import tempfile
import unittest
from pathlib import Path

from pycommander_core.device import Device
from pycommander_core.runner import RunnerResult
from pycommander_core.types import *

from .mock_commander import MockCommander

class TestDevice(unittest.TestCase):
  
  def test_device_info(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(
      RunnerResult(
        0,
"""
{
    "result": {
        "device_info": {
            "die_revision": "A0",
            "flash_size_kb": 1536,
            "part_number": "EFR32MG24B020F1536IM48",
            "production_version": "0",
            "sram_size_kb": 256,
            "unique_id": "84fd27fffe64ac04"
        }
    },
    "success": true
}
"""
      )
    )

    expected_device_info = DeviceInfo(
      part_number="EFR32MG24B020F1536IM48",
      die_revision="A0",
      production_version="0",
      flash_size_kb=1536,
      sram_size_kb=256,
      unique_id="84fd27fffe64ac04",
    )

    self.assertEqual(device.info(), expected_device_info)
    self.assertEqual(commander._runner.logged_commands, [["mock", "device", "info", "--serialno", "123456789", "--json"]])

  def test_device_info_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)
    
    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Failed to get device information"}'))
    
    self.assertEqual(device.info(), None)
    self.assertEqual(commander._runner.logged_commands, [["mock", "device", "info", "--serialno", "123456789", "--json"]])

  def test_device_reset(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertEqual(device.reset(), True)
    self.assertEqual(commander._runner.logged_commands, [["mock", "device", "reset", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_device_reset_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Failed to reset the device"}'))

    self.assertEqual(device.reset(), False)
    self.assertEqual(commander._runner.logged_commands, [["mock", "device", "reset", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_device_masserase(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertEqual(device.masserase(), True)
    self.assertEqual(commander._runner.logged_commands, [["mock", "device", "masserase", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_device_masserase_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Failed to mass erase the device"}'))

    self.assertEqual(device.masserase(), False)
    self.assertEqual(commander._runner.logged_commands, [["mock", "device", "masserase", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_device_pageerase(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))
    self.assertEqual(device.pageerase(ranges=[(0x0, 0x8000)], regions=["@main"]), True)
    self.assertEqual(commander._runner.logged_commands, [["mock", "device", "pageerase", "--range", "0x00000000:0x00008000", "--region", "@main", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_device_pageerase_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Failed to erase the pages"}'))
    self.assertEqual(device.pageerase(ranges=[(0x0, 0x8000)], regions=["@main"]), False)
    self.assertEqual(commander._runner.logged_commands, [["mock", "device", "pageerase", "--range", "0x00000000:0x00008000", "--region", "@main", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_device_getCTUNE(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(
      RunnerResult(
        0,
"""
{
    "info": [
        "Getting CTUNE values from the Device Info page, stored in EEPROM on the board, and MFG token."
    ],
    "result": {
        "ctune": {
            "board": {
                "status_str": "OK",
                "valid": true,
                "value": 103
            },
            "di": {
                "status_str": "Not set",
                "valid": false,
                "value": 0
            },
            "token": {
                "status_str": "OK",
                "valid": true,
                "value": 92
            }
        }
    },
    "success": true
}
"""
      )
    )

    expected_ctune_value = CtuneValue(
      di=None,
      board=103,
      token=92,
    )

    self.assertEqual(device.getCTUNE(), expected_ctune_value)
    self.assertEqual(commander._runner.logged_commands, [["mock", "ctune", "get", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_device_getCTUNE_failed(self):
    """
    Test the device getCTUNE method when getting the CTUNE value from the board fails.
    The method should return None.
    """

    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)
    
    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Failed to get CTUNE value from the board"}'))
    
    self.assertEqual(device.getCTUNE(), None)
    self.assertEqual(commander._runner.logged_commands, [["mock", "ctune", "get", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_device_setCTUNE_autoset_same_value(self):
    """
    Test the device setCTUNE method with autoset, no force, and the desired value is the same as the current value in the board EEPROM.
    The method should return True and *not* call the autoset command.
    """

    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    # We get the CTUNE value from the board first
    device._commander._runner.queue_result(
      RunnerResult(
        0,
"""
{
    "info": [
        "Getting CTUNE values from the Device Info page, stored in EEPROM on the board, and MFG token."
    ],
    "result": {
        "ctune": {
            "board": {
                "status_str": "OK",
                "valid": true,
                "value": 92
            },
            "di": {
                "status_str": "Not set",
                "valid": false,
                "value": 0
            },
            "token": {
                "status_str": "OK",
                "valid": true,
                "value": 92
            }
        }
    },
    "success": true
}
"""
      )
    )

    self.assertEqual(device.setCTUNE(), True)
    self.assertEqual(commander._runner.logged_commands, [["mock", "ctune", "get", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_device_setCTUNE_autoset_same_value_force(self):
    """
    Test the device setCTUNE method with autoset, force, and the desired value is the same as the current value in the board EEPROM.
    The method should return True and call the autoset command.
    """

    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    # We get the CTUNE value from the board first
    device._commander._runner.queue_result(
      RunnerResult(
        0,
"""
{
    "info": [
        "Getting CTUNE values from the Device Info page, stored in EEPROM on the board, and MFG token."
    ],
    "result": {
        "ctune": {
            "board": {
                "status_str": "OK",
                "valid": true,
                "value": 92
            },
            "di": {
                "status_str": "Not set",
                "valid": false,
                "value": 0
            },
            "token": {
                "status_str": "OK",
                "valid": true,
                "value": 92
            }
        }
    },
    "success": true
}
"""
      )
    )

    # Force was specified, so we call the autoset command. The result from this should just be true, no more fuss than that.
    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertEqual(device.setCTUNE(force=True), True)
    self.assertEqual(commander._runner.logged_commands,
    [
      ["mock", "ctune", "get",     "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"],
      ["mock", "ctune", "autoset", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]
    ])

  def test_device_setCTUNE_autoset_different_value(self):
    """
    Test the device setCTUNE method with autoset, no force, and the desired value is different from the current value in the board EEPROM.
    The method should return True and call the autoset command.
    """

    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)
    
    # We get the CTUNE value from the board first
    device._commander._runner.queue_result(
      RunnerResult(
        0,
"""
{
    "info": [
        "Getting CTUNE values from the Device Info page, stored in EEPROM on the board, and MFG token."
    ],
    "result": {
        "ctune": {
            "board": {
                "status_str": "OK",
                "valid": true,
                "value": 103
            },
            "di": {
                "status_str": "Not set",
                "valid": false,
                "value": 0
            },
            "token": {
                "status_str": "OK",
                "valid": true,
                "value": 92
            }
        }
    },
    "success": true
}
"""
      )
    )
    
    # Then we call the autoset command. The result from this should just be true, no more fuss than that.
    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertEqual(device.setCTUNE(), True)
    self.assertEqual(commander._runner.logged_commands,
    [
      ["mock", "ctune", "get",     "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"],
      ["mock", "ctune", "autoset", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]
    ])

  def test_device_setCTUNE_set_same_value(self):
    """
    Test the device setCTUNE method with set, no force, and the desired value is the same as the current value in the board EEPROM.
    The method should return True and *not* call the set command.
    """

    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)
    
    # We get the CTUNE value from the board first
    device._commander._runner.queue_result(
      RunnerResult(
        0,
"""
{
    "info": [
        "Getting CTUNE values from the Device Info page, stored in EEPROM on the board, and MFG token."
    ],
    "result": {
        "ctune": {
            "board": {
                "status_str": "OK",
                "valid": true,
                "value": 92
            },
            "di": {
                "status_str": "Not set",
                "valid": false,
                "value": 0
            },
            "token": {
                "status_str": "OK",
                "valid": true,
                "value": 92
            }
        }
    },
    "success": true
}
"""
      )
    )

    self.assertEqual(device.setCTUNE(value=92, force=False), True)
    self.assertEqual(commander._runner.logged_commands, [["mock", "ctune", "get", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_device_setCTUNE_set_same_value_force(self):
    """
    Test the device setCTUNE method with set, force, and the desired value is the same as the current value in the board EEPROM.
    The method should return True and call the set command.
    """

    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)
    
    # We get the CTUNE value from the board first
    device._commander._runner.queue_result(
      RunnerResult(
        0,
"""
{
    "info": [
        "Getting CTUNE values from the Device Info page, stored in EEPROM on the board, and MFG token."
    ],
    "result": {
        "ctune": {
            "board": {
                "status_str": "OK",
                "valid": true,
                "value": 92
            },
            "di": {
                "status_str": "Not set",
                "valid": false,
                "value": 0
            },
            "token": {
                "status_str": "OK",
                "valid": true,
                "value": 92
            }
        }
    },
    "success": true
}
"""
      )
    )
    
    # Force was specified, so we call the set command. The result from this should just be true, no more fuss than that.
    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertEqual(device.setCTUNE(value=92, force=True), True)
    self.assertEqual(commander._runner.logged_commands,
    [
      ["mock", "ctune", "get", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"],
      ["mock", "ctune", "set", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--value", "0x0000005C", "--json"]
    ])

  def test_device_setCTUNE_set_different_value(self):
    """
    Test the device setCTUNE method with set, no force, and the desired value is different from the current value in the board EEPROM.
    The method should return True and call the set command.
    """

    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)
    
    # We get the CTUNE value from the board first
    device._commander._runner.queue_result(
      RunnerResult(
        0,
"""
{
    "info": [
        "Getting CTUNE values from the Device Info page, stored in EEPROM on the board, and MFG token."
    ],
    "result": {
        "ctune": {
            "board": {
                "status_str": "OK",
                "valid": true,
                "value": 92
            },
            "di": {
                "status_str": "Not set",
                "valid": false,
                "value": 0
            },
            "token": {
                "status_str": "OK",
                "valid": true,
                "value": 92
            }
        }
    },
    "success": true
}
"""
      )
    )
    
    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertEqual(device.setCTUNE(value=93, force=False), True)
    self.assertEqual(commander._runner.logged_commands,
    [
      ["mock", "ctune", "get", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"],
      ["mock", "ctune", "set", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--value", "0x0000005D", "--json"]
    ])

  def test_device_setCTUNE_get_failed(self):
    """
    Test the device setCTUNE method when getting the CTUNE value from the board fails.
    The method should return False.
    """

    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)
    
    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Failed to get CTUNE value from the board"}'))
    
    self.assertEqual(device.setCTUNE(), False)
    self.assertEqual(commander._runner.logged_commands, [["mock", "ctune", "get", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_device_lockDebugAccess(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertEqual(device.lockDebugAccess(), True)
    self.assertEqual(commander._runner.logged_commands, [["mock", "device", "lock", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_device_lockDebugAccess_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Failed to lock the device"}'))

    self.assertEqual(device.lockDebugAccess(), False)
    self.assertEqual(commander._runner.logged_commands, [["mock", "device", "lock", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_device_unlockDebugAccess(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertEqual(device.unlockDebugAccess(), True)
    self.assertEqual(commander._runner.logged_commands, [["mock", "device", "unlock", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_device_unlockDebugAccess_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Failed to unlock the device"}'))

    self.assertEqual(device.unlockDebugAccess(), False)
    self.assertEqual(commander._runner.logged_commands, [["mock", "device", "unlock", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_device_enableWriteProtection_requires_range_or_region(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)
    with self.assertRaises(ValueError) as ctx:
      device.enableWriteProtection()
    self.assertIn("At least one range or region must be specified", str(ctx.exception))

  def test_device_enableWriteProtection_with_range(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertEqual(device.enableWriteProtection(ranges=[(0x0, 0x1000)]), True)
    self.assertEqual(commander._runner.logged_commands, [["mock", "device", "protect", "--write", "--range", "0x00000000:0x00001000", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_device_enableWriteProtection_with_region(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertEqual(device.enableWriteProtection(regions=["@main"]), True)
    self.assertEqual(commander._runner.logged_commands, [["mock", "device", "protect", "--write", "--region", "@main", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_device_enableWriteProtection_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Failed to enable write protection"}'))

    self.assertEqual(device.enableWriteProtection(ranges=[(0x0, 0x8000)]), False)
    self.assertEqual(commander._runner.logged_commands, [["mock", "device", "protect", "--write", "--range", "0x00000000:0x00008000", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_device_enableReadProtection_requires_range_or_region(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)
    with self.assertRaises(ValueError) as ctx:
      device.enableReadProtection()
    self.assertIn("At least one range or region must be specified", str(ctx.exception))

  def test_device_enableReadProtection_with_range(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertEqual(device.enableReadProtection(ranges=[(0x0, 0x1000)]), True)
    self.assertEqual(commander._runner.logged_commands, [["mock", "device", "protect", "--read", "--range", "0x00000000:0x00001000", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_device_enableReadProtection_with_region(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertEqual(device.enableReadProtection(regions=["@main"]), True)
    self.assertEqual(commander._runner.logged_commands, [["mock", "device", "protect", "--read", "--region", "@main", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_device_enableReadProtection_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Failed to enable read protection"}'))

    self.assertEqual(device.enableReadProtection(ranges=[(0x0, 0x8000)]), False)
    self.assertEqual(commander._runner.logged_commands, [["mock", "device", "protect", "--read", "--range", "0x00000000:0x00008000", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_device_disableWriteProtection(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertEqual(device.disableWriteProtection(), True)
    self.assertEqual(commander._runner.logged_commands, [["mock", "device", "protect", "--write", "--disable", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_device_disableWriteProtection_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Failed to disable write protection"}'))

    self.assertEqual(device.disableWriteProtection(), False)
    self.assertEqual(commander._runner.logged_commands, [["mock", "device", "protect", "--write", "--disable", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_device_disableReadProtection(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertEqual(device.disableReadProtection(), True)
    self.assertEqual(commander._runner.logged_commands, [["mock", "device", "protect", "--read", "--disable", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_device_disableReadProtection_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Failed to disable read protection"}'))

    self.assertEqual(device.disableReadProtection(), False)
    self.assertEqual(commander._runner.logged_commands, [["mock", "device", "protect", "--read", "--disable", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_device_info_no_device_info_key(self):
    """Result is successful but the 'device_info' key is missing from the response."""
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(
      RunnerResult(0, '{"result": {}, "success": true}')
    )

    self.assertIsNone(device.info())
    self.assertEqual(commander._runner.logged_commands, [["mock", "device", "info", "--serialno", "123456789", "--json"]])

  def test_device_writeManufacturingTokens(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    with tempfile.NamedTemporaryFile(suffix=".txt") as tf:
      device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

      self.assertTrue(device.writeManufacturingTokens(tokenfiles=[Path(tf.name)]))
      self.assertEqual(commander._runner.logged_commands, [
        ["mock", "tokens", "write", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--tokenfile", tf.name, "--json"]
      ])

  def test_device_writeManufacturingTokens_file_not_found(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    with self.assertRaises(FileNotFoundError):
      device.writeManufacturingTokens(tokenfiles=[Path("/nonexistent/file.txt")])

  def test_device_writeManufacturingTokens_with_options(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    with tempfile.NamedTemporaryFile(suffix=".txt") as tf:
      device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

      self.assertTrue(device.writeManufacturingTokens(
        tokenfiles=[Path(tf.name)],
        tokens=[("MFG_TOKEN", "0xAB")],
        tokengroup="zigbee",
        tokendefs=Path("/path/to/tokendefs.json"),
        securerange=(0x0, 0x8000),
      ))
      self.assertEqual(commander._runner.logged_commands, [
        ["mock", "tokens", "write",
         "--serialno", "123456789",
         "--device", "EFR32MG24B020F1536IM48",
         "--tokenfile", tf.name,
         "--token", "MFG_TOKEN:0xAB",
         "--tokengroup", "zigbee",
         "--tokendefs", str(Path("/path/to/tokendefs.json")),
         "--securerange", "0x00000000:0x00008000",
         "--json"]
      ])

  def test_device_writeManufacturingTokens_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    with tempfile.NamedTemporaryFile(suffix=".txt") as tf:
      device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Token write failed"}'))

      self.assertFalse(device.writeManufacturingTokens(tokenfiles=[Path(tf.name)]))

  def test_device_writeStaticTokens(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    with tempfile.NamedTemporaryFile(suffix=".txt") as tf:
      device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

      self.assertTrue(device.writeStaticTokens(tokenfiles=[Path(tf.name)]))
      self.assertEqual(commander._runner.logged_commands, [
        ["mock", "tokens", "write", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--tokenfile", tf.name, "--json"]
      ])

  def test_device_writeStaticTokens_file_not_found(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    with self.assertRaises(FileNotFoundError):
      device.writeStaticTokens(tokenfiles=[Path("/nonexistent/file.txt")])

  def test_device_flashApplication(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    with tempfile.NamedTemporaryFile(suffix=".s37") as tf:
      device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

      self.assertTrue(device.flashApplication(filenames=[Path(tf.name)]))
      self.assertEqual(commander._runner.logged_commands, [
        ["mock", "flash", tf.name, "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]
      ])

  def test_device_flashApplication_file_not_found(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    with self.assertRaises(FileNotFoundError):
      device.flashApplication(filenames=[Path("/nonexistent/firmware.s37")])

  def test_device_flashApplication_multiple_files(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    with tempfile.NamedTemporaryFile(suffix=".s37") as tf1, \
         tempfile.NamedTemporaryFile(suffix=".hex") as tf2:
      device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

      self.assertTrue(device.flashApplication(filenames=[Path(tf1.name), Path(tf2.name)]))
      self.assertEqual(commander._runner.logged_commands, [
        ["mock", "flash", tf1.name, tf2.name, "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]
      ])

  def test_device_flashApplication_multiple_files_one_missing(self):
    """One file exists and one doesn't -- should raise before running the command."""
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    with tempfile.NamedTemporaryFile(suffix=".s37") as tf:
      with self.assertRaises(FileNotFoundError):
        device.flashApplication(filenames=[Path(tf.name), Path("/nonexistent/firmware.hex")])
      self.assertEqual(commander._runner.logged_commands, [])

  def test_device_flashApplication_with_options(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    with tempfile.NamedTemporaryFile(suffix=".bin") as tf:
      device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

      self.assertTrue(device.flashApplication(
        filenames=[Path(tf.name)],
        address=0x08000000,
        treat_as_binary=True,
        masserase=True,
        force=True,
        reset=False,
        halt=True,
        close=False,
        verify=False,
        include_sections=[".text"],
        exclude_sections=[".debug"],
      ))
      self.assertEqual(commander._runner.logged_commands, [
        ["mock", "flash", tf.name,
         "--serialno", "123456789",
         "--device", "EFR32MG24B020F1536IM48",
         "--force",
         "--address", "0x08000000",
         "--halt",
         "--masserase",
         "--noreset",
         "--noclose",
         "--noverify",
         "--binary",
         "--include-section", ".text",
         "--exclude-section", ".debug",
         "--json"]
      ])

  def test_device_flashApplication_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    with tempfile.NamedTemporaryFile(suffix=".s37") as tf:
      device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Flash failed"}'))

      self.assertFalse(device.flashApplication(filenames=[Path(tf.name)]))

  def test_device_flashPatches(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertTrue(device.flashPatches(patches=[(0x08000000, 0xABCD, 2)]))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "flash",
       "--serialno", "123456789",
       "--device", "EFR32MG24B020F1536IM48",
       "--patch", "0x08000000:0x0000ABCD:2",
       "--json"]
    ])

  def test_device_flashPatches_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Patching failed"}'))

    self.assertFalse(device.flashPatches(patches=[(0x08000000, 0xABCD, 2)]))

  def test_device_getCTUNE_alternate_validity(self):
    """Board invalid, DI valid, token invalid -- covers the branches missed by the main test."""
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(
      RunnerResult(
        0,
"""
{
    "result": {
        "ctune": {
            "board": {
                "status_str": "Not set",
                "valid": false,
                "value": 0
            },
            "di": {
                "status_str": "OK",
                "valid": true,
                "value": 140
            },
            "token": {
                "status_str": "Not set",
                "valid": false,
                "value": 0
            }
        }
    },
    "success": true
}
"""
      )
    )

    expected_ctune_value = CtuneValue(
      di=140,
      board=None,
      token=None,
    )

    self.assertEqual(device.getCTUNE(), expected_ctune_value)
    self.assertEqual(commander._runner.logged_commands, [["mock", "ctune", "get", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_device_flashRamCode(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    with tempfile.NamedTemporaryFile(suffix=".bin") as tf:
      device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

      self.assertTrue(device.flashRamCode(filenames=[Path(tf.name)]))
      self.assertEqual(commander._runner.logged_commands, [
        ["mock", "flash", tf.name,
         "--serialno", "123456789",
         "--device", "EFR32MG24B020F1536IM48",
         "--noreset",
         "--json"]
      ])

  def test_device_flashRamCode_multiple_files(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    with tempfile.NamedTemporaryFile(suffix=".bin") as tf1, \
         tempfile.NamedTemporaryFile(suffix=".hex") as tf2:
      device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

      self.assertTrue(device.flashRamCode(filenames=[Path(tf1.name), Path(tf2.name)]))
      self.assertEqual(commander._runner.logged_commands, [
        ["mock", "flash", tf1.name, tf2.name,
         "--serialno", "123456789",
         "--device", "EFR32MG24B020F1536IM48",
         "--noreset",
         "--json"]
      ])

  def test_device_flashRamCode_with_options(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    with tempfile.NamedTemporaryFile(suffix=".bin") as tf:
      device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

      self.assertTrue(device.flashRamCode(
        filenames=[Path(tf.name)],
        address=0x20000000,
        include_sections=[".text"],
        exclude_sections=[".debug"],
        vtor=0x20000000,
        force=True,
        halt=True,
      ))
      self.assertEqual(commander._runner.logged_commands, [
        ["mock", "flash", tf.name,
         "--serialno", "123456789",
         "--device", "EFR32MG24B020F1536IM48",
         "--force",
         "--address", "0x20000000",
         "--halt",
         "--noreset",
         "--include-section", ".text",
         "--exclude-section", ".debug",
         "--vtor", "0x20000000",
         "--json"]
      ])

  def test_device_flashRamCode_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    with tempfile.NamedTemporaryFile(suffix=".bin") as tf:
      device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "RAM flash failed"}'))

      self.assertFalse(device.flashRamCode(filenames=[Path(tf.name)]))

  def test_device_flashRamCode_file_not_found(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    with self.assertRaises(FileNotFoundError):
      device.flashRamCode(filenames=[Path("/nonexistent/firmware.bin")])

  def test_device_flashRamCode_multiple_files_one_missing(self):
    """One file exists and one doesn't -- should raise before running the command."""
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="EFR32MG24B020F1536IM48", commander=commander)

    with tempfile.NamedTemporaryFile(suffix=".bin") as tf:
      with self.assertRaises(FileNotFoundError):
        device.flashRamCode(filenames=[Path(tf.name), Path("/nonexistent/firmware.hex")])
      self.assertEqual(commander._runner.logged_commands, [])

  def test_device_readRegionConfig(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="SiMG301", commander=commander)

    device._commander._runner.queue_result(
      RunnerResult(0,
"""
{
  "result": {
    "data_region": {
      "location": 18546688,
      "size": 2007040
    },
    "regions": [
      {
        "closed": false,
        "index": 0,
        "protection_mode": "Encrypted and authenticated",
        "size_kb": 32
      },
      {
        "closed": false,
        "index": 1,
        "protection_mode": "Encrypted and authenticated",
        "size_kb": 1696
      }
    ]
  },
  "success": true
}
"""
    ))

    actual_config = device.readRegionConfig(allow_reset=False)
    self.assertIsNotNone(actual_config)

    expected_config = RegionConfig(
      code_regions=[
        CodeRegionConfig(index=0, size_kb=32, protection_mode=CodeRegionProtectionMode.ENCRYPTED_AND_AUTHENTICATED, closed=False),
        CodeRegionConfig(index=1, size_kb=1696, protection_mode=CodeRegionProtectionMode.ENCRYPTED_AND_AUTHENTICATED, closed=False),
      ],
      data_region=DataRegionConfig(location=18546688, size=2007040),
    )
    self.assertEqual(actual_config, expected_config)
    self.assertEqual(commander._runner.logged_commands, [["mock", "security", "readregionconfig", "--serialno", "123456789", "--device", "SiMG301", "--noreset", "--json"]])

  def test_device_readRegionConfig_allow_reset(self):
    """Default allow_reset=True should not add --noreset."""
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="SiMG301", commander=commander)

    device._commander._runner.queue_result(
      RunnerResult(0,
"""
{
  "result": {
    "data_region": { 
      "location": 0,
      "size": 0
    },
    "regions": [
      { 
        "closed": true,
        "index": 0,
        "protection_mode": "None",
        "size_kb": 64
      }
    ]
  },
  "success": true
}
"""
    ))

    result = device.readRegionConfig()
    self.assertIsNotNone(result)
    self.assertEqual(result.code_regions[0].protection_mode, CodeRegionProtectionMode.NONE)
    self.assertTrue(result.code_regions[0].closed)
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "readregionconfig", "--serialno", "123456789", "--device", "SiMG301", "--json"]
    ])

  def test_device_readRegionConfig_all_protection_modes(self):
    """Cover the Encrypted and None protection mode branches."""
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="SiMG301", commander=commander)

    device._commander._runner.queue_result(
      RunnerResult(0,
"""
{
  "result": {
    "data_region": {
      "location": 100,
      "size": 200
    },
    "regions": [
      { 
        "closed": false,
        "index": 0,
        "protection_mode": "Encrypted and authenticated",
        "size_kb": 32 
      },
      { 
        "closed": false,
        "index": 1,
        "protection_mode": "Encrypted",
        "size_kb": 64 
      },
      { 
        "closed": true,
        "index": 2,
        "protection_mode": "None",
        "size_kb": 128
      }
    ]
  },
  "success": true
}
"""
    ))

    result = device.readRegionConfig()
    self.assertEqual(result.code_regions[0].protection_mode, CodeRegionProtectionMode.ENCRYPTED_AND_AUTHENTICATED)
    self.assertEqual(result.code_regions[1].protection_mode, CodeRegionProtectionMode.ENCRYPTED)
    self.assertEqual(result.code_regions[2].protection_mode, CodeRegionProtectionMode.NONE)

  def test_device_readRegionConfig_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="SiMG301", commander=commander)

    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Failed"}'))

    self.assertIsNone(device.readRegionConfig())

  def test_device_readRegionConfig_missing_regions(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="SiMG301", commander=commander)

    device._commander._runner.queue_result(
      RunnerResult(0,
"""
{
  "result": {
    "data_region": {
      "location": 0,
      "size": 0
    }
  },
  "success": true
}
"""
    ))

    self.assertIsNone(device.readRegionConfig())

  def test_device_readRegionConfig_missing_data_region(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="SiMG301", commander=commander)

    device._commander._runner.queue_result(
      RunnerResult(0, '{"result": {"regions": []}, "success": true}')
    )

    self.assertIsNone(device.readRegionConfig())

  def test_device_readRegionConfigToFile(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="SiMG301", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertTrue(device.readRegionConfigToFile(outfile=Path("/tmp/output.yaml")))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "readregionconfig", "--serialno", "123456789", "--device", "SiMG301", "--outfile", "/tmp/output.yaml", "--json"]
    ])

  def test_device_readRegionConfigToFile_noreset(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="SiMG301", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertTrue(device.readRegionConfigToFile(outfile=Path("/tmp/output.yaml"), allow_reset=False))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "readregionconfig", "--serialno", "123456789", "--device", "SiMG301", "--outfile", "/tmp/output.yaml", "--noreset", "--json"]
    ])

  def test_device_readRegionConfigToFile_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="SiMG301", commander=commander)

    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Failed"}'))

    self.assertFalse(device.readRegionConfigToFile(outfile=Path("/tmp/output.yaml")))

  def test_device_writeRegionConfig_force(self):
    """force=True skips comparison, writes directly."""
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="SiMG301", commander=commander)

    config = RegionConfig(
      code_regions=[
        CodeRegionConfig(index=0, size_kb=32, protection_mode=CodeRegionProtectionMode.ENCRYPTED_AND_AUTHENTICATED, closed=False),
      ],
      data_region=DataRegionConfig(location=0, size=0),
    )

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertTrue(device.writeRegionConfig(config, force=True))
    self.assertEqual(len(commander._runner.logged_commands), 1)
    self.assertEqual(commander._runner.logged_commands[0][0:3], ["mock", "security", "writeregionconfig"])

  def test_device_writeRegionConfig_force_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="SiMG301", commander=commander)

    config = RegionConfig(
      code_regions=[
        CodeRegionConfig(index=0, size_kb=32, protection_mode=CodeRegionProtectionMode.ENCRYPTED, closed=False),
      ],
      data_region=DataRegionConfig(location=0, size=0),
    )

    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Write failed"}'))

    self.assertFalse(device.writeRegionConfig(config, force=True))

  def test_device_writeRegionConfig_no_force_configs_equal(self):
    """Existing config matches desired -- should return True without writing."""
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="SiMG301", commander=commander)

    config = RegionConfig(
      code_regions=[
        CodeRegionConfig(index=0, size_kb=32, protection_mode=CodeRegionProtectionMode.ENCRYPTED_AND_AUTHENTICATED, closed=False),
      ],
      data_region=DataRegionConfig(location=18546688, size=2007040),
    )

    device._commander._runner.queue_result(
      RunnerResult(0,
"""
{
    "result": {
        "data_region": { "location": 18546688, "size": 2007040 },
        "regions": [
            { "closed": false, "index": 0, "protection_mode": "Encrypted and authenticated", "size_kb": 32 }
        ]
    },
    "success": true
}
"""
    ))

    self.assertTrue(device.writeRegionConfig(config, force=False))
    self.assertEqual(len(commander._runner.logged_commands), 1)
    self.assertIn("readregionconfig", commander._runner.logged_commands[0])

  def test_device_writeRegionConfig_no_force_configs_differ(self):
    """Existing config differs -- should write the new config."""
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="SiMG301", commander=commander)

    config = RegionConfig(
      code_regions=[
        CodeRegionConfig(index=0, size_kb=64, protection_mode=CodeRegionProtectionMode.ENCRYPTED, closed=False),
      ],
      data_region=DataRegionConfig(location=18546688, size=2007040),
    )

    device._commander._runner.queue_result(
      RunnerResult(0,
"""
{
    "result": {
        "data_region": { "location": 18546688, "size": 2007040 },
        "regions": [
            { "closed": false, "index": 0, "protection_mode": "Encrypted and authenticated", "size_kb": 32 }
        ]
    },
    "success": true
}
"""
    ))

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertTrue(device.writeRegionConfig(config, force=False))
    self.assertEqual(len(commander._runner.logged_commands), 2)
    self.assertIn("readregionconfig", commander._runner.logged_commands[0])
    self.assertIn("writeregionconfig", commander._runner.logged_commands[1])

  def test_device_writeRegionConfig_no_force_data_region_differs(self):
    """Existing data_region location differs -- should write."""
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="SiMG301", commander=commander)

    config = RegionConfig(
      code_regions=[
        CodeRegionConfig(index=0, size_kb=32, protection_mode=CodeRegionProtectionMode.ENCRYPTED_AND_AUTHENTICATED, closed=False),
      ],
      data_region=DataRegionConfig(location=99999, size=2007040),
    )

    device._commander._runner.queue_result(
      RunnerResult(0,
"""
{
    "result": {
        "data_region": { "location": 18546688, "size": 2007040 },
        "regions": [
            { "closed": false, "index": 0, "protection_mode": "Encrypted and authenticated", "size_kb": 32 }
        ]
    },
    "success": true
}
"""
    ))

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertTrue(device.writeRegionConfig(config, force=False))
    self.assertEqual(len(commander._runner.logged_commands), 2)

  def test_device_writeRegionConfig_no_force_closed_differs(self):
    """Existing closed state differs -- should write."""
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="SiMG301", commander=commander)

    config = RegionConfig(
      code_regions=[
        CodeRegionConfig(index=0, size_kb=32, protection_mode=CodeRegionProtectionMode.ENCRYPTED_AND_AUTHENTICATED, closed=True),
      ],
      data_region=DataRegionConfig(location=18546688, size=2007040),
    )

    device._commander._runner.queue_result(
      RunnerResult(0,
"""
{
    "result": {
        "data_region": { "location": 18546688, "size": 2007040 },
        "regions": [
            { "closed": false, "index": 0, "protection_mode": "Encrypted and authenticated", "size_kb": 32 }
        ]
    },
    "success": true
}
"""
    ))

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertTrue(device.writeRegionConfig(config, force=False))
    self.assertEqual(len(commander._runner.logged_commands), 2)

  def test_device_writeRegionConfig_no_force_read_fails(self):
    """readRegionConfig fails -- should return False without writing."""
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="SiMG301", commander=commander)

    config = RegionConfig(
      code_regions=[
        CodeRegionConfig(index=0, size_kb=32, protection_mode=CodeRegionProtectionMode.ENCRYPTED, closed=False),
      ],
      data_region=DataRegionConfig(location=0, size=0),
    )

    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Read failed"}'))

    self.assertFalse(device.writeRegionConfig(config, force=False))
    self.assertEqual(len(commander._runner.logged_commands), 1)
    self.assertIn("readregionconfig", commander._runner.logged_commands[0])

  def test_device_writeRegionConfig_no_force_index_differs(self):
    """Existing index differs -- should write."""
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="SiMG301", commander=commander)

    config = RegionConfig(
      code_regions=[
        CodeRegionConfig(index=1, size_kb=32, protection_mode=CodeRegionProtectionMode.ENCRYPTED_AND_AUTHENTICATED, closed=False),
      ],
      data_region=DataRegionConfig(location=18546688, size=2007040),
    )

    device._commander._runner.queue_result(
      RunnerResult(0,
"""
{
    "result": {
        "data_region": { "location": 18546688, "size": 2007040 },
        "regions": [
            { "closed": false, "index": 0, "protection_mode": "Encrypted and authenticated", "size_kb": 32 }
        ]
    },
    "success": true
}
"""
    ))

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertTrue(device.writeRegionConfig(config, force=False))
    self.assertEqual(len(commander._runner.logged_commands), 2)

  def test_device_writeRegionConfig_invalid_protection_mode(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="SiMG301", commander=commander)

    config = RegionConfig(
      code_regions=[
        CodeRegionConfig(index=0, size_kb=32, protection_mode="bogus", closed=False),
      ],
      data_region=DataRegionConfig(location=0, size=0),
    )

    with self.assertRaises(ValueError) as ctx:
      device.writeRegionConfig(config, force=True)
    self.assertIn("Invalid protection mode", str(ctx.exception))

  def test_device_writeRegionConfigFromFile_force(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="SiMG301", commander=commander)

    with tempfile.NamedTemporaryFile(suffix=".yaml", mode="w") as tf:
      tf.write("regions:\n  - size_kb: 32\n    protection_mode: encrypted_authenticated\n")
      tf.flush()

      device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

      self.assertTrue(device.writeRegionConfigFromFile(config_file=Path(tf.name), force=True))
      self.assertEqual(commander._runner.logged_commands, [
        ["mock", "security", "writeregionconfig", tf.name, "--serialno", "123456789", "--device", "SiMG301", "--json"]
      ])

  def test_device_writeRegionConfigFromFile_force_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="SiMG301", commander=commander)

    with tempfile.NamedTemporaryFile(suffix=".yaml", mode="w") as tf:
      tf.write("regions:\n  - size_kb: 32\n    protection_mode: encrypted_authenticated\n")
      tf.flush()

      device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Write failed"}'))

      self.assertFalse(device.writeRegionConfigFromFile(config_file=Path(tf.name), force=True))

  def test_device_writeRegionConfigFromFile_noreset(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="SiMG301", commander=commander)

    with tempfile.NamedTemporaryFile(suffix=".yaml", mode="w") as tf:
      tf.write("regions:\n  - size_kb: 32\n    protection_mode: none\n")
      tf.flush()

      device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

      self.assertTrue(device.writeRegionConfigFromFile(config_file=Path(tf.name), allow_reset=False, force=True))
      self.assertEqual(commander._runner.logged_commands, [
        ["mock", "security", "writeregionconfig", tf.name, "--serialno", "123456789", "--device", "SiMG301", "--noreset", "--json"]
      ])

  def test_device_writeRegionConfigFromFile_file_not_found(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="SiMG301", commander=commander)

    with self.assertRaises(FileNotFoundError):
      device.writeRegionConfigFromFile(config_file=Path("/nonexistent/config.yaml"))

  def test_device_writeRegionConfigFromFile_missing_regions(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="SiMG301", commander=commander)

    with tempfile.NamedTemporaryFile(suffix=".yaml", mode="w") as tf:
      tf.write("something_else: true\n")
      tf.flush()

      with self.assertRaises(ValueError) as ctx:
        device.writeRegionConfigFromFile(config_file=Path(tf.name))
      self.assertIn("Regions are required", str(ctx.exception))

  def test_device_writeRegionConfigFromFile_missing_size_kb(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="SiMG301", commander=commander)

    with tempfile.NamedTemporaryFile(suffix=".yaml", mode="w") as tf:
      tf.write("regions:\n  - protection_mode: encrypted\n")
      tf.flush()

      with self.assertRaises(ValueError) as ctx:
        device.writeRegionConfigFromFile(config_file=Path(tf.name))
      self.assertIn("Size KB is required", str(ctx.exception))

  def test_device_writeRegionConfigFromFile_missing_protection_mode(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="SiMG301", commander=commander)

    with tempfile.NamedTemporaryFile(suffix=".yaml", mode="w") as tf:
      tf.write("regions:\n  - size_kb: 32\n")
      tf.flush()

      with self.assertRaises(ValueError) as ctx:
        device.writeRegionConfigFromFile(config_file=Path(tf.name))
      self.assertIn("Protection mode is required", str(ctx.exception))

  def test_device_writeRegionConfigFromFile_invalid_protection_mode(self):
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="SiMG301", commander=commander)

    with tempfile.NamedTemporaryFile(suffix=".yaml", mode="w") as tf:
      tf.write("regions:\n  - size_kb: 32\n    protection_mode: bogus_mode\n")
      tf.flush()

      with self.assertRaises(ValueError) as ctx:
        device.writeRegionConfigFromFile(config_file=Path(tf.name))
      self.assertIn("Invalid protection mode", str(ctx.exception))

  def test_device_writeRegionConfigFromFile_no_force_configs_equal(self):
    """Existing config matches file config -- returns True without writing."""
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="SiMG301", commander=commander)

    device._commander._runner.queue_result(
      RunnerResult(0,
"""
{
    "result": {
        "data_region": { "location": 0, "size": 0 },
        "regions": [
            { "closed": false, "index": 0, "protection_mode": "Encrypted and authenticated", "size_kb": 32 }
        ]
    },
    "success": true
}
"""
    ))

    with tempfile.NamedTemporaryFile(suffix=".yaml", mode="w") as tf:
      tf.write("regions:\n  - size_kb: 32\n    protection_mode: encrypted_authenticated\n")
      tf.flush()

      self.assertTrue(device.writeRegionConfigFromFile(config_file=Path(tf.name), force=False))
      self.assertEqual(len(commander._runner.logged_commands), 1)
      self.assertIn("readregionconfig", commander._runner.logged_commands[0])

  def test_device_writeRegionConfigFromFile_no_force_configs_differ(self):
    """Existing config differs from file config -- should write."""
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="SiMG301", commander=commander)

    device._commander._runner.queue_result(
      RunnerResult(0,
"""
{
    "result": {
        "data_region": { "location": 0, "size": 0 },
        "regions": [
            { "closed": false, "index": 0, "protection_mode": "Encrypted and authenticated", "size_kb": 32 }
        ]
    },
    "success": true
}
"""
    ))

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    with tempfile.NamedTemporaryFile(suffix=".yaml", mode="w") as tf:
      tf.write("regions:\n  - size_kb: 64\n    protection_mode: none\n")
      tf.flush()

      self.assertTrue(device.writeRegionConfigFromFile(config_file=Path(tf.name), force=False))
      self.assertEqual(len(commander._runner.logged_commands), 2)
      self.assertIn("readregionconfig", commander._runner.logged_commands[0])
      self.assertIn("writeregionconfig", commander._runner.logged_commands[1])

  def test_device_writeRegionConfigFromFile_no_force_read_fails(self):
    """readRegionConfig fails -- returns False without writing."""
    commander = MockCommander(serial_number="123456789")
    device = Device(part_number="SiMG301", commander=commander)

    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Read failed"}'))

    with tempfile.NamedTemporaryFile(suffix=".yaml", mode="w") as tf:
      tf.write("regions:\n  - size_kb: 32\n    protection_mode: encrypted\n")
      tf.flush()

      self.assertFalse(device.writeRegionConfigFromFile(config_file=Path(tf.name), force=False))
      self.assertEqual(len(commander._runner.logged_commands), 1)
