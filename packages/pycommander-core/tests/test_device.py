import unittest

from pycommander_core.device import Device
from pycommander_core.runner import RunnerResult
from pycommander_core.types import DeviceInfo, CtuneValue

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