import os
import tempfile
import unittest
from pathlib import Path

from pycommander_core.target import Target
from pycommander_core.runner import RunnerResult
from pycommander_core.types import *

from .mock_commander import MockCommander

class TestTarget(unittest.TestCase):
  
  def test_target_info(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

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

    expected_device_info = TargetInfo(
      part_number="EFR32MG24B020F1536IM48",
      die_revision="A0",
      production_version="0",
      flash_size_kb=1536,
      sram_size_kb=256,
      unique_id="84fd27fffe64ac04",
    )

    self.assertEqual(device.info(), expected_device_info)
    self.assertEqual(commander._runner.logged_commands, [["mock", "device", "info", "--serialno", "123456789", "--json"]])

  def test_target_info_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)
    
    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Failed to get device information"}'))
    
    self.assertEqual(device.info(), None)
    self.assertEqual(commander._runner.logged_commands, [["mock", "device", "info", "--serialno", "123456789", "--json"]])

  def test_target_reset(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertEqual(device.reset(), True)
    self.assertEqual(commander._runner.logged_commands, [["mock", "device", "reset", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_target_reset_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Failed to reset the device"}'))

    self.assertEqual(device.reset(), False)
    self.assertEqual(commander._runner.logged_commands, [["mock", "device", "reset", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_target_masserase(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertEqual(device.masserase(), True)
    self.assertEqual(commander._runner.logged_commands, [["mock", "device", "masserase", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_target_masserase_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Failed to mass erase the device"}'))

    self.assertEqual(device.masserase(), False)
    self.assertEqual(commander._runner.logged_commands, [["mock", "device", "masserase", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_target_pageerase(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))
    self.assertEqual(device.pageerase(ranges=[(0x0, 0x8000)], regions=["@main"]), True)
    self.assertEqual(commander._runner.logged_commands, [["mock", "device", "pageerase", "--range", "0x00000000:0x00008000", "--region", "@main", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_target_pageerase_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Failed to erase the pages"}'))
    self.assertEqual(device.pageerase(ranges=[(0x0, 0x8000)], regions=["@main"]), False)
    self.assertEqual(commander._runner.logged_commands, [["mock", "device", "pageerase", "--range", "0x00000000:0x00008000", "--region", "@main", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_target_getCTUNE(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

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

  def test_target_getCTUNE_failed(self):
    """
    Test the device getCTUNE method when getting the CTUNE value from the board fails.
    The method should return None.
    """

    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)
    
    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Failed to get CTUNE value from the board"}'))
    
    self.assertEqual(device.getCTUNE(), None)
    self.assertEqual(commander._runner.logged_commands, [["mock", "ctune", "get", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_target_setCTUNE_autoset_same_value(self):
    """
    Test the device setCTUNE method with autoset, no force, and the desired value is the same as the current value in the board EEPROM.
    The method should return True and *not* call the autoset command.
    """

    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

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

  def test_target_setCTUNE_autoset_same_value_force(self):
    """
    Test the device setCTUNE method with autoset, force, and the desired value is the same as the current value in the board EEPROM.
    The method should return True and call the autoset command.
    """

    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

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

  def test_target_setCTUNE_autoset_different_value(self):
    """
    Test the device setCTUNE method with autoset, no force, and the desired value is different from the current value in the board EEPROM.
    The method should return True and call the autoset command.
    """

    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)
    
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

  def test_target_setCTUNE_set_same_value(self):
    """
    Test the device setCTUNE method with set, no force, and the desired value is the same as the current value in the board EEPROM.
    The method should return True and *not* call the set command.
    """

    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)
    
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

  def test_target_setCTUNE_set_same_value_force(self):
    """
    Test the device setCTUNE method with set, force, and the desired value is the same as the current value in the board EEPROM.
    The method should return True and call the set command.
    """

    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)
    
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

  def test_target_setCTUNE_set_different_value(self):
    """
    Test the device setCTUNE method with set, no force, and the desired value is different from the current value in the board EEPROM.
    The method should return True and call the set command.
    """

    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)
    
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

  def test_target_setCTUNE_get_failed(self):
    """
    Test the device setCTUNE method when getting the CTUNE value from the board fails.
    The method should return False.
    """

    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)
    
    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Failed to get CTUNE value from the board"}'))
    
    self.assertEqual(device.setCTUNE(), False)
    self.assertEqual(commander._runner.logged_commands, [["mock", "ctune", "get", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_target_enableWriteProtection_requires_range_or_region(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)
    with self.assertRaises(ValueError) as ctx:
      device.enableWriteProtection()
    self.assertIn("At least one range or region must be specified", str(ctx.exception))

  def test_target_enableWriteProtection_with_range(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertEqual(device.enableWriteProtection(ranges=[(0x0, 0x1000)]), True)
    self.assertEqual(commander._runner.logged_commands, [["mock", "device", "protect", "--write", "--range", "0x00000000:0x00001000", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_target_enableWriteProtection_with_region(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertEqual(device.enableWriteProtection(regions=["@main"]), True)
    self.assertEqual(commander._runner.logged_commands, [["mock", "device", "protect", "--write", "--region", "@main", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_target_enableWriteProtection_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Failed to enable write protection"}'))

    self.assertEqual(device.enableWriteProtection(ranges=[(0x0, 0x8000)]), False)
    self.assertEqual(commander._runner.logged_commands, [["mock", "device", "protect", "--write", "--range", "0x00000000:0x00008000", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_target_enableReadProtection_requires_range_or_region(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)
    with self.assertRaises(ValueError) as ctx:
      device.enableReadProtection()
    self.assertIn("At least one range or region must be specified", str(ctx.exception))

  def test_target_enableReadProtection_with_range(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertEqual(device.enableReadProtection(ranges=[(0x0, 0x1000)]), True)
    self.assertEqual(commander._runner.logged_commands, [["mock", "device", "protect", "--read", "--range", "0x00000000:0x00001000", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_target_enableReadProtection_with_region(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertEqual(device.enableReadProtection(regions=["@main"]), True)
    self.assertEqual(commander._runner.logged_commands, [["mock", "device", "protect", "--read", "--region", "@main", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_target_enableReadProtection_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Failed to enable read protection"}'))

    self.assertEqual(device.enableReadProtection(ranges=[(0x0, 0x8000)]), False)
    self.assertEqual(commander._runner.logged_commands, [["mock", "device", "protect", "--read", "--range", "0x00000000:0x00008000", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_target_disableWriteProtection(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertEqual(device.disableWriteProtection(), True)
    self.assertEqual(commander._runner.logged_commands, [["mock", "device", "protect", "--write", "--disable", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_target_disableWriteProtection_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Failed to disable write protection"}'))

    self.assertEqual(device.disableWriteProtection(), False)
    self.assertEqual(commander._runner.logged_commands, [["mock", "device", "protect", "--write", "--disable", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_target_disableReadProtection(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertEqual(device.disableReadProtection(), True)
    self.assertEqual(commander._runner.logged_commands, [["mock", "device", "protect", "--read", "--disable", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_target_disableReadProtection_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Failed to disable read protection"}'))

    self.assertEqual(device.disableReadProtection(), False)
    self.assertEqual(commander._runner.logged_commands, [["mock", "device", "protect", "--read", "--disable", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_target_info_no_device_info_key(self):
    """Result is successful but the 'device_info' key is missing from the response."""
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(
      RunnerResult(0, '{"result": {}, "success": true}')
    )

    self.assertIsNone(device.info())
    self.assertEqual(commander._runner.logged_commands, [["mock", "device", "info", "--serialno", "123456789", "--json"]])

  def test_target_writeManufacturingTokens(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    tf = tempfile.NamedTemporaryFile(dir=".", suffix=".txt", delete=False)
    self.addCleanup(os.remove, tf.name)
    tf.close()

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertTrue(device.writeManufacturingTokens(tokenfiles=[Path(tf.name)]))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "tokens", "write", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--tokenfile", tf.name, "--json"]
    ])

  def test_target_writeManufacturingTokens_file_not_found(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    with self.assertRaises(FileNotFoundError):
      device.writeManufacturingTokens(tokenfiles=[Path("/nonexistent/file.txt")])

  def test_target_writeManufacturingTokens_with_options(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    tf = tempfile.NamedTemporaryFile(dir=".", suffix=".txt", delete=False)
    self.addCleanup(os.remove, tf.name)
    tf.close()

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

  def test_target_writeManufacturingTokens_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    tf = tempfile.NamedTemporaryFile(dir=".", suffix=".txt", delete=False)
    self.addCleanup(os.remove, tf.name)
    tf.close()

    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Token write failed"}'))

    self.assertFalse(device.writeManufacturingTokens(tokenfiles=[Path(tf.name)]))

  def test_target_writeStaticTokens(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    tf = tempfile.NamedTemporaryFile(dir=".", suffix=".txt", delete=False)
    self.addCleanup(os.remove, tf.name)
    tf.close()

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertTrue(device.writeStaticTokens(tokenfiles=[Path(tf.name)]))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "tokens", "write", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--tokenfile", tf.name, "--json"]
    ])

  def test_target_writeStaticTokens_file_not_found(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    with self.assertRaises(FileNotFoundError):
      device.writeStaticTokens(tokenfiles=[Path("/nonexistent/file.txt")])

  def test_target_flashApplication(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    tf = tempfile.NamedTemporaryFile(dir=".", suffix=".s37", delete=False)
    self.addCleanup(os.remove, tf.name)
    tf.close()

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertTrue(device.flashApplication(filenames=[Path(tf.name)]))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "flash", tf.name, "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]
    ])

  def test_target_flashApplication_file_not_found(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    with self.assertRaises(FileNotFoundError):
      device.flashApplication(filenames=[Path("/nonexistent/firmware.s37")])

  def test_target_flashApplication_multiple_files(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    tf1 = tempfile.NamedTemporaryFile(dir=".", suffix=".s37", delete=False)
    self.addCleanup(os.remove, tf1.name)
    tf1.close()
    tf2 = tempfile.NamedTemporaryFile(dir=".", suffix=".hex", delete=False)
    self.addCleanup(os.remove, tf2.name)
    tf2.close()

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertTrue(device.flashApplication(filenames=[Path(tf1.name), Path(tf2.name)]))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "flash", tf1.name, tf2.name, "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]
    ])

  def test_target_flashApplication_multiple_files_one_missing(self):
    """One file exists and one doesn't -- should raise before running the command."""
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    tf = tempfile.NamedTemporaryFile(dir=".", suffix=".s37", delete=False)
    self.addCleanup(os.remove, tf.name)
    tf.close()

    with self.assertRaises(FileNotFoundError):
      device.flashApplication(filenames=[Path(tf.name), Path("/nonexistent/firmware.hex")])
    self.assertEqual(commander._runner.logged_commands, [])

  def test_target_flashApplication_with_options(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    tf = tempfile.NamedTemporaryFile(dir=".", suffix=".bin", delete=False)
    self.addCleanup(os.remove, tf.name)
    tf.close()

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

  def test_target_flashApplication_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    tf = tempfile.NamedTemporaryFile(dir=".", suffix=".s37", delete=False)
    self.addCleanup(os.remove, tf.name)
    tf.close()

    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Flash failed"}'))

    self.assertFalse(device.flashApplication(filenames=[Path(tf.name)]))

  def test_target_flashPatches(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertTrue(device.flashPatches(patches=[(0x08000000, 0xABCD, 2)]))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "flash",
       "--serialno", "123456789",
       "--device", "EFR32MG24B020F1536IM48",
       "--patch", "0x08000000:0x0000ABCD:2",
       "--json"]
    ])

  def test_target_flashPatches_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Patching failed"}'))

    self.assertFalse(device.flashPatches(patches=[(0x08000000, 0xABCD, 2)]))

  def test_target_getCTUNE_alternate_validity(self):
    """Board invalid, DI valid, token invalid -- covers the branches missed by the main test."""
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

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

  def test_target_flashRamCode(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    tf = tempfile.NamedTemporaryFile(dir=".", suffix=".bin", delete=False)
    self.addCleanup(os.remove, tf.name)
    tf.close()

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertTrue(device.flashRamCode(filenames=[Path(tf.name)]))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "flash", tf.name,
       "--serialno", "123456789",
       "--device", "EFR32MG24B020F1536IM48",
       "--noreset",
       "--json"]
    ])

  def test_target_flashRamCode_multiple_files(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    tf1 = tempfile.NamedTemporaryFile(dir=".", suffix=".bin", delete=False)
    self.addCleanup(os.remove, tf1.name)
    tf1.close()
    tf2 = tempfile.NamedTemporaryFile(dir=".", suffix=".hex", delete=False)
    self.addCleanup(os.remove, tf2.name)
    tf2.close()

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertTrue(device.flashRamCode(filenames=[Path(tf1.name), Path(tf2.name)]))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "flash", tf1.name, tf2.name,
       "--serialno", "123456789",
       "--device", "EFR32MG24B020F1536IM48",
       "--noreset",
       "--json"]
    ])

  def test_target_flashRamCode_with_options(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    tf = tempfile.NamedTemporaryFile(dir=".", suffix=".bin", delete=False)
    self.addCleanup(os.remove, tf.name)
    tf.close()

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

  def test_target_flashRamCode_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    tf = tempfile.NamedTemporaryFile(dir=".", suffix=".bin", delete=False)
    self.addCleanup(os.remove, tf.name)
    tf.close()

    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "RAM flash failed"}'))

    self.assertFalse(device.flashRamCode(filenames=[Path(tf.name)]))

  def test_target_flashRamCode_file_not_found(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    with self.assertRaises(FileNotFoundError):
      device.flashRamCode(filenames=[Path("/nonexistent/firmware.bin")])

  def test_target_flashRamCode_multiple_files_one_missing(self):
    """One file exists and one doesn't -- should raise before running the command."""
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    tf = tempfile.NamedTemporaryFile(dir=".", suffix=".bin", delete=False)
    self.addCleanup(os.remove, tf.name)
    tf.close()

    with self.assertRaises(FileNotFoundError):
      device.flashRamCode(filenames=[Path(tf.name), Path("/nonexistent/firmware.hex")])
    self.assertEqual(commander._runner.logged_commands, [])

  def test_target_readRegionConfig(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="SiMG301", commander=commander)

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

  def test_target_readRegionConfig_allow_reset(self):
    """Default allow_reset=True should not add --noreset."""
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="SiMG301", commander=commander)

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

  def test_target_readRegionConfig_all_protection_modes(self):
    """Cover the Encrypted and None protection mode branches."""
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="SiMG301", commander=commander)

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

  def test_target_readRegionConfig_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="SiMG301", commander=commander)

    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Failed"}'))

    self.assertIsNone(device.readRegionConfig())

  def test_target_readRegionConfig_missing_regions(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="SiMG301", commander=commander)

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

  def test_target_readRegionConfig_missing_data_region(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="SiMG301", commander=commander)

    device._commander._runner.queue_result(
      RunnerResult(0, '{"result": {"regions": []}, "success": true}')
    )

    self.assertIsNone(device.readRegionConfig())

  def test_target_readRegionConfigToFile(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="SiMG301", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    file_path = Path("/tmp/output.yaml")
    self.assertTrue(device.readRegionConfigToFile(outfile=file_path))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "readregionconfig", "--serialno", "123456789", "--device", "SiMG301", "--outfile", str(file_path), "--json"]
    ])

  def test_target_readRegionConfigToFile_noreset(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="SiMG301", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))
   
    file_path = Path("/tmp/output.yaml")
    self.assertTrue(device.readRegionConfigToFile(outfile=file_path, allow_reset=False))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "readregionconfig", "--serialno", "123456789", "--device", "SiMG301", "--outfile", str(file_path), "--noreset", "--json"]
    ])

  def test_target_readRegionConfigToFile_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="SiMG301", commander=commander)

    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Failed"}'))

    file_path = Path("/tmp/output.yaml")
    self.assertFalse(device.readRegionConfigToFile(outfile=file_path))

  def test_target_writeRegionConfig_force(self):
    """force=True skips comparison, writes directly."""
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="SiMG301", commander=commander)

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

  def test_target_writeRegionConfig_force_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="SiMG301", commander=commander)

    config = RegionConfig(
      code_regions=[
        CodeRegionConfig(index=0, size_kb=32, protection_mode=CodeRegionProtectionMode.ENCRYPTED, closed=False),
      ],
      data_region=DataRegionConfig(location=0, size=0),
    )

    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Write failed"}'))

    self.assertFalse(device.writeRegionConfig(config, force=True))

  def test_target_writeRegionConfig_no_force_configs_equal(self):
    """Existing config matches desired -- should return True without writing."""
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="SiMG301", commander=commander)

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

  def test_target_writeRegionConfig_no_force_configs_differ(self):
    """Existing config differs -- should write the new config."""
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="SiMG301", commander=commander)

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

  def test_target_writeRegionConfig_no_force_data_region_differs(self):
    """Existing data_region location differs -- should write."""
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="SiMG301", commander=commander)

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

  def test_target_writeRegionConfig_no_force_closed_differs(self):
    """Existing closed state differs -- should write."""
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="SiMG301", commander=commander)

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

  def test_target_writeRegionConfig_no_force_read_fails(self):
    """readRegionConfig fails -- should return False without writing."""
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="SiMG301", commander=commander)

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

  def test_target_writeRegionConfig_no_force_index_differs(self):
    """Existing index differs -- should write."""
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="SiMG301", commander=commander)

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

  def test_target_writeRegionConfig_invalid_protection_mode(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="SiMG301", commander=commander)

    config = RegionConfig(
      code_regions=[
        CodeRegionConfig(index=0, size_kb=32, protection_mode="bogus", closed=False),
      ],
      data_region=DataRegionConfig(location=0, size=0),
    )

    with self.assertRaises(ValueError) as ctx:
      device.writeRegionConfig(config, force=True)
    self.assertIn("Invalid protection mode", str(ctx.exception))

  def test_target_writeRegionConfigFromFile_force(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="SiMG301", commander=commander)

    tf = tempfile.NamedTemporaryFile(dir=".", suffix=".yaml", mode="w", delete=False)
    self.addCleanup(os.remove, tf.name)
    tf.write("regions:\n  - size_kb: 32\n    protection_mode: encrypted_authenticated\n")
    tf.close()

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertTrue(device.writeRegionConfigFromFile(config_file=Path(tf.name), force=True))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "writeregionconfig", tf.name, "--serialno", "123456789", "--device", "SiMG301", "--json"]
    ])

  def test_target_writeRegionConfigFromFile_force_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="SiMG301", commander=commander)

    tf = tempfile.NamedTemporaryFile(dir=".", suffix=".yaml", mode="w", delete=False)
    self.addCleanup(os.remove, tf.name)
    tf.write("regions:\n  - size_kb: 32\n    protection_mode: encrypted_authenticated\n")
    tf.close()

    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Write failed"}'))

    self.assertFalse(device.writeRegionConfigFromFile(config_file=Path(tf.name), force=True))

  def test_target_writeRegionConfigFromFile_noreset(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="SiMG301", commander=commander)

    tf = tempfile.NamedTemporaryFile(dir=".", suffix=".yaml", mode="w", delete=False)
    self.addCleanup(os.remove, tf.name)
    tf.write("regions:\n  - size_kb: 32\n    protection_mode: none\n")
    tf.close()

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertTrue(device.writeRegionConfigFromFile(config_file=Path(tf.name), allow_reset=False, force=True))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "writeregionconfig", tf.name, "--serialno", "123456789", "--device", "SiMG301", "--noreset", "--json"]
    ])

  def test_target_writeRegionConfigFromFile_file_not_found(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="SiMG301", commander=commander)

    with self.assertRaises(FileNotFoundError):
      device.writeRegionConfigFromFile(config_file=Path("/nonexistent/config.yaml"))

  def test_target_writeRegionConfigFromFile_missing_regions(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="SiMG301", commander=commander)

    tf = tempfile.NamedTemporaryFile(dir=".", suffix=".yaml", mode="w", delete=False)
    self.addCleanup(os.remove, tf.name)
    tf.write("something_else: true\n")
    tf.close()

    with self.assertRaises(ValueError) as ctx:
      device.writeRegionConfigFromFile(config_file=Path(tf.name))
    self.assertIn("Regions are required", str(ctx.exception))

  def test_target_writeRegionConfigFromFile_missing_size_kb(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="SiMG301", commander=commander)

    tf = tempfile.NamedTemporaryFile(dir=".", suffix=".yaml", mode="w", delete=False)
    self.addCleanup(os.remove, tf.name)
    tf.write("regions:\n  - protection_mode: encrypted\n")
    tf.close()

    with self.assertRaises(ValueError) as ctx:
      device.writeRegionConfigFromFile(config_file=Path(tf.name))
    self.assertIn("Size KB is required", str(ctx.exception))

  def test_target_writeRegionConfigFromFile_missing_protection_mode(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="SiMG301", commander=commander)

    tf = tempfile.NamedTemporaryFile(dir=".", suffix=".yaml", mode="w", delete=False)
    self.addCleanup(os.remove, tf.name)
    tf.write("regions:\n  - size_kb: 32\n")
    tf.close()

    with self.assertRaises(ValueError) as ctx:
      device.writeRegionConfigFromFile(config_file=Path(tf.name))
    self.assertIn("Protection mode is required", str(ctx.exception))

  def test_target_writeRegionConfigFromFile_invalid_protection_mode(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="SiMG301", commander=commander)

    tf = tempfile.NamedTemporaryFile(dir=".", suffix=".yaml", mode="w", delete=False)
    self.addCleanup(os.remove, tf.name)
    tf.write("regions:\n  - size_kb: 32\n    protection_mode: bogus_mode\n")
    tf.close()

    with self.assertRaises(ValueError) as ctx:
      device.writeRegionConfigFromFile(config_file=Path(tf.name))
    self.assertIn("Invalid protection mode", str(ctx.exception))

  def test_target_writeRegionConfigFromFile_no_force_configs_equal(self):
    """Existing config matches file config -- returns True without writing."""
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="SiMG301", commander=commander)

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

    tf = tempfile.NamedTemporaryFile(dir=".", suffix=".yaml", mode="w", delete=False)
    self.addCleanup(os.remove, tf.name)
    tf.write("regions:\n  - size_kb: 32\n    protection_mode: encrypted_authenticated\n")
    tf.close()

    self.assertTrue(device.writeRegionConfigFromFile(config_file=Path(tf.name), force=False))
    self.assertEqual(len(commander._runner.logged_commands), 1)
    self.assertIn("readregionconfig", commander._runner.logged_commands[0])

  def test_target_writeRegionConfigFromFile_no_force_configs_differ(self):
    """Existing config differs from file config -- should write."""
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="SiMG301", commander=commander)

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

    tf = tempfile.NamedTemporaryFile(dir=".", suffix=".yaml", mode="w", delete=False)
    self.addCleanup(os.remove, tf.name)
    tf.write("regions:\n  - size_kb: 64\n    protection_mode: none\n")
    tf.close()

    self.assertTrue(device.writeRegionConfigFromFile(config_file=Path(tf.name), force=False))
    self.assertEqual(len(commander._runner.logged_commands), 2)
    self.assertIn("readregionconfig", commander._runner.logged_commands[0])
    self.assertIn("writeregionconfig", commander._runner.logged_commands[1])

  def test_target_writeRegionConfigFromFile_no_force_read_fails(self):
    """readRegionConfig fails -- returns False without writing."""
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="SiMG301", commander=commander)

    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Read failed"}'))

    tf = tempfile.NamedTemporaryFile(dir=".", suffix=".yaml", mode="w", delete=False)
    self.addCleanup(os.remove, tf.name)
    tf.write("regions:\n  - size_kb: 32\n    protection_mode: encrypted\n")
    tf.close()

    self.assertFalse(device.writeRegionConfigFromFile(config_file=Path(tf.name), force=False))
    self.assertEqual(len(commander._runner.logged_commands), 1)

  def test_target_closeCodeRegion(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="SiMG301", commander=commander)

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
        "closed": false,
        "index": 0,
        "protection_mode": "Encrypted and authenticated",
        "size_kb": 32
      }
    ]
  },
  "success": true
}
"""
    ))
    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertTrue(device.closeCodeRegion(index=0, code_version=1, allow_reset=False))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "readregionconfig", "--serialno", "123456789", "--device", "SiMG301", "--noreset", "--json"],
      ["mock", "security", "closeregion", "0", "--serialno", "123456789", "--device", "SiMG301", "--noreset", "--codeversion", "1", "--json"]
    ])

  def test_target_closeCodeRegion_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="SiMG301", commander=commander)

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
        "closed": false,
        "index": 0,
        "protection_mode": "Encrypted and authenticated",
        "size_kb": 32
      }
    ]
  },
  "success": true
}
"""
    ))
    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Close failed"}'))

    self.assertFalse(device.closeCodeRegion(index=0, code_version=1, allow_reset=False, force=False))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "readregionconfig", "--serialno", "123456789", "--device", "SiMG301", "--noreset", "--json"],
      ["mock", "security", "closeregion", "0", "--serialno", "123456789", "--device", "SiMG301", "--noreset", "--codeversion", "1", "--json"]
    ])

  def test_target_closeCodeRegion_already_closed(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="SiMG301", commander=commander)

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
        "protection_mode": "Encrypted and authenticated",
        "size_kb": 32
      }
    ]
  },
  "success": true
}
"""
    ))
    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))
    self.assertTrue(device.closeCodeRegion(index=0, code_version=1, allow_reset=False, force=False))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "readregionconfig", "--serialno", "123456789", "--device", "SiMG301", "--noreset", "--json"],
    ])

  def test_target_closeCodeRegion_already_closed_force(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="SiMG301", commander=commander)

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
        "protection_mode": "Encrypted and authenticated",
        "size_kb": 32
      }
    ]
  },
  "success": true
}
"""
    ))

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))
    self.assertTrue(device.closeCodeRegion(index=0, code_version=1, allow_reset=False, force=True))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "readregionconfig", "--serialno", "123456789", "--device", "SiMG301", "--noreset", "--json"],
      ["mock", "security", "closeregion", "0", "--serialno", "123456789", "--device", "SiMG301", "--noreset", "--codeversion", "1", "--json"]
    ])

  def test_target_closeCodeRegion_read_fails(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="SiMG301", commander=commander)

    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Read failed"}'))

    self.assertFalse(device.closeCodeRegion(index=0, code_version=1, allow_reset=False, force=False))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "readregionconfig", "--serialno", "123456789", "--device", "SiMG301", "--noreset", "--json"]
    ])

  def test_target_closeCodeRegion_invalid_index(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="SiMG301", commander=commander)

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
        "closed": false,
        "index": 0,
        "protection_mode": "Encrypted and authenticated",
        "size_kb": 32
      }
    ]
  },
  "success": true
}
"""
    ))

    with self.assertRaises(ValueError):
      device.closeCodeRegion(index=-1, code_version=1, allow_reset=False, force=False)
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "readregionconfig", "--serialno", "123456789", "--device", "SiMG301", "--noreset", "--json"]
    ])

  def test_target_closeCodeRegion_invalid_code_version(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="SiMG301", commander=commander)

    with self.assertRaises(ValueError):
      device.closeCodeRegion(index=0, code_version=-1, allow_reset=False)
    self.assertEqual(commander._runner.logged_commands, [])

  def test_target_closeCodeRegion_code_version_too_large(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="SiMG301", commander=commander)

    with self.assertRaises(ValueError):
      device.closeCodeRegion(index=0, code_version=0xFFFFFFFF + 1, allow_reset=False)
    self.assertEqual(commander._runner.logged_commands, [])

  def test_target_getSecurityStatus(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(
      RunnerResult(
        0,
"""
{
    "result": {
        "security": {
            "boot_status": 0,
            "boot_status_str": "SE_BOOT_OK",
            "command_key_installed": true,
            "debug_lock": "Enabled",
            "device_erase": "Enabled",
            "se_firmware_version": "2.2.6",
            "secure_boot_enabled": true,
            "secure_debug_unlock": "Enabled",
            "serial_number": "000000000000000014c86ee7a33c3185",
            "sign_key_installed": true,
            "tamper_ok": true
        }
    },
    "success": true
}
"""
      )
    )

    expected = SecurityStatus(
      boot_status=0,
      boot_status_str="SE_BOOT_OK",
      command_key_installed=True,
      debug_lock_enabled=True,
      device_erase_enabled=True,
      se_firmware_version="2.2.6",
      secure_boot_enabled=True,
      secure_debug_unlock_enabled=True,
      serial_number="000000000000000014c86ee7a33c3185",
      sign_key_installed=True,
      tamper_ok=True,
    )

    self.assertEqual(device.getSecurityStatus(), expected)
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "status", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]
    ])

  def test_target_getSecurityStatus_all_disabled(self):
    """All lock/erase/unlock fields report Disabled -- corresponding bools should be False."""
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(
      RunnerResult(
        0,
"""
{
    "result": {
        "security": {
            "boot_status": 0,
            "boot_status_str": "OK",
            "command_key_installed": false,
            "debug_lock": "Disabled",
            "device_erase": "Disabled",
            "se_firmware_version": "2.2.6",
            "secure_boot_enabled": false,
            "secure_debug_unlock": "Disabled",
            "serial_number": "000000000000000014c86ee7a33c3185",
            "sign_key_installed": false,
            "tamper_ok": true
        }
    },
    "success": true
}
"""
      )
    )

    expected = SecurityStatus(
      boot_status=0,
      boot_status_str="OK",
      command_key_installed=False,
      debug_lock_enabled=False,
      device_erase_enabled=False,
      se_firmware_version="2.2.6",
      secure_boot_enabled=False,
      secure_debug_unlock_enabled=False,
      serial_number="000000000000000014c86ee7a33c3185",
      sign_key_installed=False,
      tamper_ok=True,
    )

    self.assertEqual(device.getSecurityStatus(), expected)
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "status", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]
    ])

  def test_target_getSecurityStatus_missing_fields(self):
    """Security dict is present but individual keys are missing -- .get() defaults apply."""
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(
      RunnerResult(0, '{"result": {"security": {}}, "success": true}')
    )

    expected = SecurityStatus(
      boot_status=None,
      boot_status_str=None,
      command_key_installed=None,
      debug_lock_enabled=False,
      device_erase_enabled=False,
      se_firmware_version=None,
      secure_boot_enabled=None,
      secure_debug_unlock_enabled=False,
      serial_number=None,
      sign_key_installed=None,
      tamper_ok=None,
    )

    self.assertEqual(device.getSecurityStatus(), expected)

  def test_target_getSecurityStatus_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(
      RunnerResult(254, '{"success": false, "error": "Failed to get security status"}')
    )

    self.assertIsNone(device.getSecurityStatus())
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "status", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]
    ])

  def test_target_getSecurityStatus_missing_security_key(self):
    """Result is successful but the 'security' key is missing from the response."""
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(
      RunnerResult(0, '{"result": {}, "success": true}')
    )

    self.assertIsNone(device.getSecurityStatus())
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "status", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]
    ])

  def test_target_getSecurityStatus_noreset(self):
    """allow_reset=False should add --noreset to the command."""
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(
      RunnerResult(0, '{"result": {"security": {}}, "success": true}')
    )

    device.getSecurityStatus(allow_reset=False)
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "status", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--noreset", "--json"]
    ])

  def test_target_getSecurityStatus_with_trustzone(self):
    """show_trustzone_status=True with full trustzone data."""
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(
      RunnerResult(
        0,
"""
{
    "result": {
        "security": {
            "boot_status": 0,
            "boot_status_str": "SE_BOOT_OK",
            "command_key_installed": false,
            "debug_lock": "Disabled",
            "device_erase": "Enabled",
            "se_firmware_version": "2.2.6",
            "secure_boot_enabled": false,
            "secure_debug_unlock": "Disabled",
            "serial_number": "000000000000000014c86ee7a33c3185",
            "sign_key_installed": false,
            "tamper_ok": true
        },
        "trustzone": true,
        "trustzone_config": {
            "dbglock_locked": true,
            "debug_port_locked": true,
            "nidlock_locked": false,
            "spidlock_locked": true,
            "spnidlock_locked": false
        },
        "trustzone_state": {
            "dbglock_locked": true,
            "nidlock_locked": false,
            "spidlock_locked": true,
            "spnidlock_locked": false
        }
    },
    "success": true
}
"""
      )
    )

    expected = SecurityStatus(
      boot_status=0,
      boot_status_str="SE_BOOT_OK",
      command_key_installed=False,
      debug_lock_enabled=False,
      device_erase_enabled=True,
      se_firmware_version="2.2.6",
      secure_boot_enabled=False,
      secure_debug_unlock_enabled=False,
      serial_number="000000000000000014c86ee7a33c3185",
      sign_key_installed=False,
      tamper_ok=True,
      trustzone_config=TrustzoneConfig(
        debug_lock_locked=True,
        debug_port_locked=True,
        nidlock_locked=False,
        spidlock_locked=True,
        spnidlock_locked=False,
      ),
      trustzone_state=TrustzoneState(
        debug_lock_locked=True,
        nidlock_locked=False,
        spidlock_locked=True,
        spnidlock_locked=False,
      ),
    )

    self.assertEqual(device.getSecurityStatus(show_trustzone_status=True), expected)
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "status", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--trustzone", "--json"]
    ])

  def test_target_getSecurityStatus_with_trustzone_all_false(self):
    """show_trustzone_status=True with all trustzone fields false."""
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(
      RunnerResult(
        0,
"""
{
    "result": {
        "security": {
            "boot_status": 0,
            "boot_status_str": "SE_BOOT_OK",
            "command_key_installed": false,
            "debug_lock": "Disabled",
            "device_erase": "Disabled",
            "se_firmware_version": "2.2.6",
            "secure_boot_enabled": false,
            "secure_debug_unlock": "Disabled",
            "serial_number": "000000000000000014c86ee7a33c3185",
            "sign_key_installed": false,
            "tamper_ok": true
        },
        "trustzone": true,
        "trustzone_config": {
            "dbglock_locked": false,
            "debug_port_locked": false,
            "nidlock_locked": false,
            "spidlock_locked": false,
            "spnidlock_locked": false
        },
        "trustzone_state": {
            "dbglock_locked": false,
            "nidlock_locked": false,
            "spidlock_locked": false,
            "spnidlock_locked": false
        }
    },
    "success": true
}
"""
      )
    )

    result = device.getSecurityStatus(show_trustzone_status=True)
    self.assertIsNotNone(result)
    self.assertFalse(result.trustzone_config.debug_lock_locked)
    self.assertFalse(result.trustzone_config.debug_port_locked)
    self.assertFalse(result.trustzone_config.nidlock_locked)
    self.assertFalse(result.trustzone_config.spidlock_locked)
    self.assertFalse(result.trustzone_config.spnidlock_locked)
    self.assertFalse(result.trustzone_state.debug_lock_locked)
    self.assertFalse(result.trustzone_state.nidlock_locked)
    self.assertFalse(result.trustzone_state.spidlock_locked)
    self.assertFalse(result.trustzone_state.spnidlock_locked)

  def test_target_getSecurityStatus_with_trustzone_missing_fields(self):
    """Trustzone dicts present but individual keys missing -- .get() defaults to False."""
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(
      RunnerResult(
        0,
        '{"result": {"security": {}, "trustzone": true, "trustzone_config": {}, "trustzone_state": {}}, "success": true}'
      )
    )

    result = device.getSecurityStatus(show_trustzone_status=True)
    self.assertIsNotNone(result)
    self.assertFalse(result.trustzone_config.debug_lock_locked)
    self.assertFalse(result.trustzone_config.debug_port_locked)
    self.assertFalse(result.trustzone_config.nidlock_locked)
    self.assertFalse(result.trustzone_config.spidlock_locked)
    self.assertFalse(result.trustzone_config.spnidlock_locked)
    self.assertFalse(result.trustzone_state.debug_lock_locked)
    self.assertFalse(result.trustzone_state.nidlock_locked)
    self.assertFalse(result.trustzone_state.spidlock_locked)
    self.assertFalse(result.trustzone_state.spnidlock_locked)

  def test_target_getSecurityStatus_with_trustzone_missing_trustzone_key(self):
    """show_trustzone_status=True but 'trustzone' key missing from result -- returns None."""
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(
      RunnerResult(
        0,
"""
{
    "result": {
        "security": {
            "boot_status": 0,
            "boot_status_str": "SE_BOOT_OK",
            "command_key_installed": false,
            "debug_lock": "Disabled",
            "device_erase": "Disabled",
            "se_firmware_version": "2.2.6",
            "secure_boot_enabled": false,
            "secure_debug_unlock": "Disabled",
            "serial_number": "000000000000000014c86ee7a33c3185",
            "sign_key_installed": false,
            "tamper_ok": true
        }
    },
    "success": true
}
"""
      )
    )

    self.assertIsNone(device.getSecurityStatus(show_trustzone_status=True))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "status", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--trustzone", "--json"]
    ])

  def test_target_getSecurityStatus_without_trustzone_omits_flag(self):
    """show_trustzone_status=False (default) should not pass --trustzone and should leave trustzone fields as None."""
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(
      RunnerResult(0, '{"result": {"security": {}}, "success": true}')
    )

    result = device.getSecurityStatus(show_trustzone_status=False)
    self.assertIsNotNone(result)
    self.assertIsNone(result.trustzone_config)
    self.assertIsNone(result.trustzone_state)
    self.assertNotIn("--trustzone", commander._runner.logged_commands[0])

  def test_target_generateGblDecryptionKey(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    file = Path("/tmp/gbl_key.txt")
    self.assertTrue(device.generateGblDecryptionKey(outfile=file))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "util", "genkey", "--device", "EFR32MG24B020F1536IM48", "--type", "aes-ccm", "--outfile", str(file), "--json"]
    ])

  def test_target_generateGblDecryptionKey_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Key generation failed"}'))

    file = Path("/tmp/gbl_key.txt")
    self.assertFalse(device.generateGblDecryptionKey(outfile=file))

  def test_target_writeGblDecryptionKey(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    tf = tempfile.NamedTemporaryFile(dir=".", suffix=".key", delete=False)
    self.addCleanup(os.remove, tf.name)
    tf.close()

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertTrue(device.writeGblDecryptionKey(key_file=Path(tf.name)))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "writekey", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--decrypt", str(tf.name), "--json"]
    ])

  def test_target_writeGblDecryptionKey_confirm(self):
    """confirm=True should add --noprompt to the command."""
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    tf = tempfile.NamedTemporaryFile(dir=".", suffix=".key", delete=False)
    self.addCleanup(os.remove, tf.name)
    tf.close()

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertTrue(device.writeGblDecryptionKey(key_file=Path(tf.name), confirm=True))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "writekey", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--decrypt", str(tf.name), "--noprompt", "--json"]
    ])

  def test_target_writeGblDecryptionKey_file_not_found(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    with self.assertRaises(FileNotFoundError):
      device.writeGblDecryptionKey(key_file=Path("/nonexistent/key.key"))
    self.assertEqual(commander._runner.logged_commands, [])

  def test_target_writeGblDecryptionKey_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    tf = tempfile.NamedTemporaryFile(dir=".", suffix=".key", delete=False)
    self.addCleanup(os.remove, tf.name)
    tf.close()

    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Write key failed"}'))

    self.assertFalse(device.writeGblDecryptionKey(key_file=Path(tf.name)))

  def test_target_readPublicSigningKey(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    sign_key_hex = "fb2470314c0710f5a72e89a30d2af607770187568f80cffa7fc6516f61e0dc258a8606fe664a097eb94d3ea29e1b87262babdb969842da31512bdc7b9c63f4f6"

    device._commander._runner.queue_result(
      RunnerResult(
        0,
        '{"result": {"sign_key": "' + sign_key_hex + '"}, "success": true}'
      )
    )

    result = device.readPublicSigningKey()
    self.assertIsNotNone(result)
    self.assertIsInstance(result, bytes)
    self.assertEqual(result, sign_key_hex.encode())
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "readkey", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--sign", "--json"]
    ])

  def test_target_readPublicSigningKey_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Read key failed"}'))

    self.assertIsNone(device.readPublicSigningKey())
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "readkey", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--sign", "--json"]
    ])

  def test_target_writePublicSigningKey(self):
    """No existing key in OTP -- should read first, then write."""
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    tf = tempfile.NamedTemporaryFile(dir=".", suffix=".pem", delete=False)
    self.addCleanup(os.remove, tf.name)
    tf.close()

    device._commander._runner.queue_result(RunnerResult(0, '{"result": {}, "success": true}'))
    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertTrue(device.writePublicSigningKey(key_file=Path(tf.name)))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "readkey", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--sign", "--json"],
      ["mock", "security", "writekey", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--sign", str(tf.name), "--json"],
    ])

  def test_target_writePublicSigningKey_confirm(self):
    """confirm=True should add --noprompt to the writekey command."""
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    tf = tempfile.NamedTemporaryFile(dir=".", suffix=".pem", delete=False)
    self.addCleanup(os.remove, tf.name)
    tf.close()

    device._commander._runner.queue_result(RunnerResult(0, '{"result": {}, "success": true}'))
    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertTrue(device.writePublicSigningKey(key_file=Path(tf.name), confirm=True))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "readkey", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--sign", "--json"],
      ["mock", "security", "writekey", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--sign", str(tf.name), "--noprompt", "--json"],
    ])

  def test_target_writePublicSigningKey_already_exists(self):
    """Existing signing key in OTP -- should raise RuntimeError without writing."""
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    tf = tempfile.NamedTemporaryFile(dir=".", suffix=".pem", delete=False)
    self.addCleanup(os.remove, tf.name)
    tf.close()

    sign_key_hex = "fb2470314c0710f5a72e89a30d2af607770187568f80cffa7fc6516f61e0dc258a8606fe664a097eb94d3ea29e1b87262babdb969842da31512bdc7b9c63f4f6"
    device._commander._runner.queue_result(
      RunnerResult(0, '{"result": {"sign_key": "' + sign_key_hex + '"}, "success": true}')
    )

    with self.assertRaises(RuntimeError) as ctx:
      device.writePublicSigningKey(key_file=Path(tf.name))
    self.assertIn("already exists", str(ctx.exception))
    self.assertEqual(len(commander._runner.logged_commands), 1)
    self.assertIn("readkey", commander._runner.logged_commands[0])

  def test_target_writePublicSigningKey_file_not_found(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    with self.assertRaises(FileNotFoundError):
      device.writePublicSigningKey(key_file=Path("/nonexistent/key.pem"))
    self.assertEqual(commander._runner.logged_commands, [])

  def test_target_writePublicSigningKey_failed(self):
    """No existing key, but writekey command fails."""
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    tf = tempfile.NamedTemporaryFile(dir=".", suffix=".pem", delete=False)
    self.addCleanup(os.remove, tf.name)
    tf.close()

    device._commander._runner.queue_result(RunnerResult(0, '{"result": {}, "success": true}'))
    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Write key failed"}'))

    self.assertFalse(device.writePublicSigningKey(key_file=Path(tf.name)))

  def test_target_generateSigningKeys(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    pubkey_file = Path("/tmp/pubkey.pem")
    privkey_file = Path("/tmp/privkey.pem")
    self.assertTrue(device.generateSigningKeys(
      pubkey_file=pubkey_file,
      privkey_file=privkey_file,
    ))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "util", "genkey", "--device", "EFR32MG24B020F1536IM48", "--type", "ecc-p256", "--pubkey", str(pubkey_file), "--privkey", str(privkey_file), "--json"]
    ])

  def test_target_generateSigningKeys_with_tokenfile(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    pubkey_file = Path("/tmp/pubkey.pem")
    privkey_file = Path("/tmp/privkey.pem")
    tokenfile = Path("/tmp/token.txt")
    self.assertTrue(device.generateSigningKeys(
      pubkey_file=pubkey_file,
      privkey_file=privkey_file,
      tokenfile=tokenfile,
    ))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "util", "genkey", "--device", "EFR32MG24B020F1536IM48", "--type", "ecc-p256", "--pubkey", str(pubkey_file), "--privkey", str(privkey_file), "--tokenfile", str(tokenfile), "--json"]
    ])

  def test_target_generateSigningKeys_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Key generation failed"}'))

    pubkey_file = Path("/tmp/pubkey.pem")
    privkey_file = Path("/tmp/privkey.pem")
    self.assertFalse(device.generateSigningKeys(
      pubkey_file=pubkey_file,
      privkey_file=privkey_file,
    ))

  def test_target_readPublicSigningKey_missing_sign_key(self):
    """Result is successful but the 'sign_key' key is missing from the response."""
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(
      RunnerResult(0, '{"result": {}, "success": true}')
    )

    self.assertIsNone(device.readPublicSigningKey())
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "readkey", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--sign", "--json"]
    ])

  def test_target_generateCommandKeys(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    pubkey_file = Path("/tmp/cmd_pubkey.pem")
    privkey_file = Path("/tmp/cmd_privkey.pem")
    self.assertTrue(device.generateCommandKeys(
      pubkey_file=pubkey_file,
      privkey_file=privkey_file,
    ))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "util", "genkey", "--device", "EFR32MG24B020F1536IM48", "--type", "ecc-p256", "--pubkey", str(pubkey_file), "--privkey", str(privkey_file), "--json"]
    ])

  def test_target_generateCommandKeys_with_tokenfile(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    pubkey_file = Path("/tmp/cmd_pubkey.pem")
    privkey_file = Path("/tmp/cmd_privkey.pem")
    tokenfile = Path("/tmp/cmd_token.txt")

    self.assertTrue(device.generateCommandKeys(
      pubkey_file=pubkey_file,
      privkey_file=privkey_file,
      tokenfile=tokenfile,
    ))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "util", "genkey", "--device", "EFR32MG24B020F1536IM48", "--type", "ecc-p256", "--pubkey", str(pubkey_file), "--privkey", str(privkey_file), "--tokenfile", str(tokenfile), "--json"]
    ])

  def test_target_generateCommandKeys_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Key generation failed"}'))

    pubkey_file = Path("/tmp/cmd_pubkey.pem")
    privkey_file = Path("/tmp/cmd_privkey.pem")
    self.assertFalse(device.generateCommandKeys(
      pubkey_file=pubkey_file,
      privkey_file=privkey_file,
    ))

  def test_target_readPublicCommandKey(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    command_key_hex = "a218c9615321567527e94ac1f01230604e231f1eabe699fb1d751af3e28d00feaa3dd823540a2452baa40dfb3475d3bb786b41e7880881b5a5427e71542694a2"

    device._commander._runner.queue_result(
      RunnerResult(0, '{"result": {"command_key": "' + command_key_hex + '"}, "success": true}')
    )

    result = device.readPublicCommandKey()
    self.assertIsNotNone(result)
    self.assertIsInstance(result, bytes)
    self.assertEqual(result, command_key_hex.encode())
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "readkey", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--command", "--json"]
    ])

  def test_target_readPublicCommandKey_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Read key failed"}'))

    self.assertIsNone(device.readPublicCommandKey())
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "readkey", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--command", "--json"]
    ])

  def test_target_readPublicCommandKey_missing_command_key(self):
    """Result is successful but the 'command_key' key is missing from the response."""
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(
      RunnerResult(0, '{"result": {}, "success": true}')
    )

    self.assertIsNone(device.readPublicCommandKey())

  def test_target_writePublicCommandKey(self):
    """No existing key in OTP -- should read first, then write."""
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    tf = tempfile.NamedTemporaryFile(dir=".", suffix=".pem", delete=False)
    self.addCleanup(os.remove, tf.name)
    tf.close()

    device._commander._runner.queue_result(RunnerResult(0, '{"result": {}, "success": true}'))
    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertTrue(device.writePublicCommandKey(key_file=Path(tf.name)))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "readkey", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--command", "--json"],
      ["mock", "security", "writekey", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--command", str(tf.name), "--json"],
    ])

  def test_target_writePublicCommandKey_confirm(self):
    """confirm=True should add --noprompt to the writekey command."""
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    tf = tempfile.NamedTemporaryFile(dir=".", suffix=".pem", delete=False)
    self.addCleanup(os.remove, tf.name)
    tf.close()

    device._commander._runner.queue_result(RunnerResult(0, '{"result": {}, "success": true}'))
    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertTrue(device.writePublicCommandKey(key_file=Path(tf.name), confirm=True))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "readkey", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--command", "--json"],
      ["mock", "security", "writekey", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--command", str(tf.name), "--noprompt", "--json"],
    ])

  def test_target_writePublicCommandKey_already_exists(self):
    """Existing command key in OTP -- should raise RuntimeError without writing."""
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    tf = tempfile.NamedTemporaryFile(dir=".", suffix=".pem", delete=False)
    self.addCleanup(os.remove, tf.name)
    tf.close()

    command_key_hex = "a218c9615321567527e94ac1f01230604e231f1eabe699fb1d751af3e28d00feaa3dd823540a2452baa40dfb3475d3bb786b41e7880881b5a5427e71542694a2"
    device._commander._runner.queue_result(
      RunnerResult(0, '{"result": {"command_key": "' + command_key_hex + '"}, "success": true}')
    )

    with self.assertRaises(RuntimeError) as ctx:
      device.writePublicCommandKey(key_file=Path(tf.name))
    self.assertIn("already exists", str(ctx.exception))
    self.assertEqual(len(commander._runner.logged_commands), 1)
    self.assertIn("readkey", commander._runner.logged_commands[0])

  def test_target_writePublicCommandKey_file_not_found(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    with self.assertRaises(FileNotFoundError):
      device.writePublicCommandKey(key_file=Path("/nonexistent/key.pem"))
    self.assertEqual(commander._runner.logged_commands, [])

  def test_target_writePublicCommandKey_failed(self):
    """No existing key, but writekey command fails."""
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    tf = tempfile.NamedTemporaryFile(dir=".", suffix=".pem", delete=False)
    self.addCleanup(os.remove, tf.name)
    tf.close()

    device._commander._runner.queue_result(RunnerResult(0, '{"result": {}, "success": true}'))
    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Write key failed"}'))

    self.assertFalse(device.writePublicCommandKey(key_file=Path(tf.name)))

  def test_target_lockDebugAccess(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertEqual(device.lockDebugAccess(), True)
    self.assertEqual(commander._runner.logged_commands, [["mock", "security", "lock", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_target_lockDebugAccess_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Failed to lock the device"}'))

    self.assertEqual(device.lockDebugAccess(), False)
    self.assertEqual(commander._runner.logged_commands, [["mock", "security", "lock", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_target_lockDebugAccess_noreset(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertTrue(device.lockDebugAccess(allow_reset=False))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "lock", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--noreset", "--json"]
    ])

  def test_target_lockDebugAccess_with_trustzone(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertTrue(device.lockDebugAccess(trustzone="0101"))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "lock", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--trustzone", "0101", "--json"]
    ])

  def test_target_lockDebugAccess_with_invalid_trustzone(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    with self.assertRaises(ValueError):
      device.lockDebugAccess(trustzone="0") # Too short
    with self.assertRaises(ValueError):
      device.lockDebugAccess(trustzone="01010") # Too long
    with self.assertRaises(ValueError):
      device.lockDebugAccess(trustzone="nope") # Invalid character

  def test_target_lockDebugAccess_disable_device_erase(self):
    """Lock succeeds, then disabledeviceerase is called with confirm=True (noprompt)."""
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))
    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertTrue(device.lockDebugAccess(disable_device_erase=True, confirm=True))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "lock", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"],
      ["mock", "security", "disabledeviceerase", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--noprompt", "--json"],
    ])

  def test_target_lockDebugAccess_disable_device_erase_no_confirm(self):
    """Lock succeeds, disabledeviceerase called without noprompt (confirm=False)."""
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))
    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertTrue(device.lockDebugAccess(disable_device_erase=True, confirm=False))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "lock", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"],
      ["mock", "security", "disabledeviceerase", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"],
    ])

  def test_target_lockDebugAccess_disable_device_erase_lock_fails(self):
    """Lock fails -- disabledeviceerase should not be called."""
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Lock failed"}'))

    self.assertFalse(device.lockDebugAccess(disable_device_erase=True, confirm=True))
    self.assertEqual(len(commander._runner.logged_commands), 1)
    self.assertIn("lock", commander._runner.logged_commands[0])

  def test_target_lockDebugAccess_disable_device_erase_failed(self):
    """Lock succeeds but disabledeviceerase fails."""
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))
    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Disable erase failed"}'))

    self.assertFalse(device.lockDebugAccess(disable_device_erase=True, confirm=True))
    self.assertEqual(len(commander._runner.logged_commands), 2)

  def test_target_lockDebugAccess_disable_device_erase_noreset(self):
    """Lock with noreset and disable_device_erase -- both commands get noreset."""
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))
    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertTrue(device.lockDebugAccess(allow_reset=False, disable_device_erase=True, confirm=True))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "lock", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--noreset", "--json"],
      ["mock", "security", "disabledeviceerase", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--noreset", "--noprompt", "--json"],
    ])

  def test_target_unlockDebugAccess(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertEqual(device.unlockDebugAccess(), True)
    self.assertEqual(commander._runner.logged_commands, [["mock", "security", "unlock", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_target_unlockDebugAccess_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Failed to unlock the device"}'))

    self.assertEqual(device.unlockDebugAccess(), False)
    self.assertEqual(commander._runner.logged_commands, [["mock", "security", "unlock", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--json"]])

  def test_target_unlockDebugAccess_noreset(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertTrue(device.unlockDebugAccess(allow_reset=False))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "unlock", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--noreset", "--json"]
    ])

  def test_target_unlockDebugAccess_with_certificate(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertTrue(device.unlockDebugAccess(
      certificate_file=Path("/path/to/cert.pem"),
      certificate_private_key=Path("/path/to/cert_privkey.pem"),
      certificate_public_key=Path("/path/to/cert_pubkey.pem"),
      certificate_signature=Path("/path/to/cert_sig.bin"),
    ))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "unlock",
       "--serialno", "123456789",
       "--device", "EFR32MG24B020F1536IM48",
       "--cert", "/path/to/cert.pem",
       "--cert-privkey", "/path/to/cert_privkey.pem",
       "--cert-signature", "/path/to/cert_sig.bin",
       "--cert-pubkey", "/path/to/cert_pubkey.pem",
       "--json"]
    ])

  def test_target_unlockDebugAccess_with_command_key(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertTrue(device.unlockDebugAccess(
      command_key=Path("/path/to/command_key.pem"),
      command_signature=Path("/path/to/command_sig.bin"),
    ))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "unlock",
       "--serialno", "123456789",
       "--device", "EFR32MG24B020F1536IM48",
       "--command-key", "/path/to/command_key.pem",
       "--command-signature", "/path/to/command_sig.bin",
       "--json"]
    ])

  def test_target_unlockDebugAccess_with_authorization(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertTrue(device.unlockDebugAccess(
      authorization="auth_token_abc",
      unlock_param="param_xyz",
    ))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "unlock",
       "--serialno", "123456789",
       "--device", "EFR32MG24B020F1536IM48",
       "--authorization", "auth_token_abc",
       "--unlock-param", "param_xyz",
       "--json"]
    ])

  def test_target_unlockDebugAccess_with_all_options(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertTrue(device.unlockDebugAccess(
      allow_reset=False,
      certificate_file=Path("/cert.pem"),
      certificate_private_key=Path("/cert_privkey.pem"),
      certificate_public_key=Path("/cert_pubkey.pem"),
      certificate_signature=Path("/cert_sig.bin"),
      command_key=Path("/cmd_key.pem"),
      command_signature=Path("/cmd_sig.bin"),
      authorization="auth_data",
      unlock_param="unlock_data",
    ))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "unlock",
       "--serialno", "123456789",
       "--device", "EFR32MG24B020F1536IM48",
       "--noreset",
       "--cert", "/cert.pem",
       "--cert-privkey", "/cert_privkey.pem",
       "--command-key", "/cmd_key.pem",
       "--cert-signature", "/cert_sig.bin",
       "--command-signature", "/cmd_sig.bin",
       "--authorization", "auth_data",
       "--cert-pubkey", "/cert_pubkey.pem",
       "--unlock-param", "unlock_data",
       "--json"]
    ])

  def test_target_enableSecureDebugUnlock(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertTrue(device.enableSecureDebugUnlock())
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "lockconfig", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--secure-debug-unlock", "enable", "--json"]
    ])

  def test_target_enableSecureDebugUnlock_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Failed"}'))

    self.assertFalse(device.enableSecureDebugUnlock())

  def test_target_enableSecureDebugUnlock_noreset(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertTrue(device.enableSecureDebugUnlock(allow_reset=False))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "lockconfig", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--noreset", "--secure-debug-unlock", "enable", "--json"]
    ])

  def test_target_disableSecureDebugUnlock(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertTrue(device.disableSecureDebugUnlock())
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "lockconfig", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--secure-debug-unlock", "disable", "--json"]
    ])

  def test_target_disableSecureDebugUnlock_confirm(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertTrue(device.disableSecureDebugUnlock(confirm=True))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "lockconfig", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--secure-debug-unlock", "disable", "--noprompt", "--json"]
    ])

  def test_target_disableSecureDebugUnlock_noreset(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(0, '{"success": true}'))

    self.assertTrue(device.disableSecureDebugUnlock(allow_reset=False))
    self.assertEqual(commander._runner.logged_commands, [
      ["mock", "security", "lockconfig", "--serialno", "123456789", "--device", "EFR32MG24B020F1536IM48", "--noreset", "--secure-debug-unlock", "disable", "--json"]
    ])

  def test_target_disableSecureDebugUnlock_failed(self):
    commander = MockCommander(serial_number="123456789")
    device = Target(part_number="EFR32MG24B020F1536IM48", commander=commander)

    device._commander._runner.queue_result(RunnerResult(254, '{"success": false, "error": "Failed"}'))

    self.assertFalse(device.disableSecureDebugUnlock())
