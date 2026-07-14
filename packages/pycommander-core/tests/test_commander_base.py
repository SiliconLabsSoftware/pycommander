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

import unittest
import shutil

from pathlib import Path

from .mock_commander import MockCommander

from pycommander_core.commander_base import CommanderBase, CommanderResult
from pycommander_core.types import CommanderVersionInfo, BasicAdapterInfo
from pycommander_core.runner import RunnerResult

class TestCommanderBase(unittest.TestCase):

  def test_commander_base_get_kwargs(self):
    commander = MockCommander()
    self.assertEqual(commander._get_kwargs(), [])
    self.assertEqual(commander._get_kwargs(serial_number="123456789"), ["--serialno", "123456789"])
    self.assertEqual(commander._get_kwargs(ip_address="192.168.1.100"), ["--ip", "192.168.1.100"])
    self.assertEqual(commander._get_kwargs(serial_port="/dev/tty.usbmodem141101"), ["--identifybyserialport", "/dev/tty.usbmodem141101"])
    self.assertEqual(commander._get_kwargs(debug_speed=1000000), ["--speed", "1000000"])
    self.assertEqual(commander._get_kwargs(debug_tif="SWD"), ["--tif", "SWD"])
    self.assertEqual(commander._get_kwargs(debug_irpre=1000000), ["--irpre", "1000000"])
    self.assertEqual(commander._get_kwargs(debug_drpre=1000000), ["--drpre", "1000000"])
    self.assertEqual(commander._get_kwargs(target_device="123456789"), ["--device", "123456789"])
    self.assertEqual(commander._get_kwargs(force=True), ["--force"])
    self.assertEqual(commander._get_kwargs(target_device=None), [])
    self.assertEqual(commander._get_kwargs(force=False), [])
    self.assertEqual(commander._get_kwargs(devicexml="/Applications/Commander.app/Contents/Resources/jlink/"), ["--devicexml", "/Applications/Commander.app/Contents/Resources/jlink/"])
    self.assertEqual(commander._get_kwargs(devicexml=None), [])
    self.assertEqual(commander._get_kwargs(devicexml=""), [])

    self.assertEqual(commander._get_kwargs(
      serial_number="123456789",
      ip_address="192.168.1.100",
      serial_port="/dev/tty.usbmodem141101",
      debug_speed=1000000,
      debug_tif="SWD",
      debug_irpre=1000000,
      debug_drpre=1000000,
      target_device="123456789",
      force=True,
      devicexml="/Applications/Commander.app/Contents/Resources/jlink/",
    ), [
      "--serialno", "123456789",
      "--ip", "192.168.1.100",
      "--identifybyserialport", "/dev/tty.usbmodem141101",
      "--speed", "1000000",
      "--tif", "SWD",
      "--irpre", "1000000",
      "--drpre", "1000000",
      "--device", "123456789",
      "--force", "--devicexml", "/Applications/Commander.app/Contents/Resources/jlink/",])

  def test_commander_base_executable_path_and_cli_true(self):
    command = shutil.which("echo")
    if command is None:
      self.fail("echo command not found")
    commander = CommanderBase(executable_path=Path(command), cli=True)
    self.assertEqual(commander._executable_path, Path(command))

  def test_commander_base_executable_path_and_cli_false(self):
    command = shutil.which("echo")
    if command is None:
      self.fail("echo command not found")
    commander = CommanderBase(executable_path=Path(command), cli=False)
    self.assertEqual(commander._executable_path, Path(command))

  def test_commander_base_nonstring_executable_path(self):
    command = shutil.which("echo")
    if command is None:
      self.fail("echo command not found")
    commander = CommanderBase(executable_path=str(Path(command)))
    self.assertEqual(commander._executable_path, Path(command))

  def test_commander_base_nonexistent_executable_path(self):
    with self.assertRaisesRegex(FileNotFoundError, f"Executable not found: {str(Path('mock'))}"):
      CommanderBase(executable_path=Path("mock"))

  def test_commander_base_no_executable_path_and_missing_cli(self):
    with self.assertRaisesRegex(ValueError, "cli must be provided if executable_path is not provided"):
      CommanderBase(cli=None)

  def test_commander_base_getVersion(self):
    commander = MockCommander()

    commander._runner.queue_result(RunnerResult(0, 
"""
{
  "result": {
    "version": {
      "emdll_version": "7v8p9b1011",
      "jlink_dll_version": "8.94",
      "mbed_tls_version": "0.0.0",
      "qt_version": "5.15.2",
      "simplicity_commander_version": "1v2p3b456"
    }
  },
  "success": true
}
"""
    , ""))

    expected_version_info = CommanderVersionInfo(
      simplicity_commander_version="1v2p3b456",
      jlink_dll_version="8.94",
      emdll_version="7v8p9b1011",
      mbed_tls_version="0.0.0",
      qt_version="5.15.2",
    )

    self.assertEqual(commander.getVersion(), expected_version_info)
    self.assertEqual(commander._runner.logged_commands, [["mock", "--version", "--json"]])

  def test_commander_base_getVersion_failed(self):
    commander = MockCommander()
    commander._runner.queue_result(RunnerResult(1, "", ""))
    self.assertEqual(commander.getVersion(), None)
    self.assertEqual(commander._runner.logged_commands, [["mock", "--version", "--json"]])

  def test_commander_base_getVersion_missing_result(self):
    commander = MockCommander()
    commander._runner.queue_result(RunnerResult(0, '{"success": true}', ""))
    self.assertEqual(commander.getVersion(), None)
    self.assertEqual(commander._runner.logged_commands, [["mock", "--version", "--json"]])

  def test_commander_base_getVersion_missing_version(self):
    commander = MockCommander()
    commander._runner.queue_result(RunnerResult(0, '{"result": ""}', ""))
    self.assertEqual(commander.getVersion(), None)
    self.assertEqual(commander._runner.logged_commands, [["mock", "--version", "--json"]])

  def test_commander_base_listAvailableAdapters_network(self):
    commander = MockCommander()
    commander._runner.queue_result(RunnerResult(0, '{"result": {"devices": [{"adapter_ip": "192.168.1.100", "serial_number": "123456789", "adapter_nickname": "Adapter 1"}]}}', ""))
    self.assertEqual(commander.listAvailableAdapters(list_usb_adapters=False, list_network_adapters=True), [BasicAdapterInfo(jlink_serial_number="123456789", ip_address="192.168.1.100", nickname="Adapter 1")])
    self.assertEqual(commander._runner.logged_commands, [["mock", "adapter", "list", "--noconnect", "--net", "--json"]])

  def test_commander_base_listAvailableAdapters_usb(self):
    commander = MockCommander()
    commander._runner.queue_result(RunnerResult(0, '{"result": {"devices": [{"adapter_ip": "192.168.1.100", "serial_number": "123456789", "adapter_nickname": "Adapter 1"}]}}', ""))
    self.assertEqual(commander.listAvailableAdapters(list_usb_adapters=True, list_network_adapters=False), [BasicAdapterInfo(jlink_serial_number="123456789", ip_address="192.168.1.100", nickname="Adapter 1")])
    self.assertEqual(commander._runner.logged_commands, [["mock", "adapter", "list", "--noconnect", "--json"]])

  def test_commander_base_listAvailableAdapters_both(self):
    commander = MockCommander()
    with self.assertRaises(ValueError):
      commander.listAvailableAdapters(list_usb_adapters=True, list_network_adapters=True)
    self.assertEqual(commander._runner.logged_commands, [])

  def test_commander_base_listAvailableAdapters_none(self):
    commander = MockCommander()
    with self.assertRaises(ValueError):
      commander.listAvailableAdapters(list_usb_adapters=False, list_network_adapters=False)
    self.assertEqual(commander._runner.logged_commands, [])

  def test_commander_base_listAvailableAdapters_no_adapters(self):
    commander = MockCommander()
    commander._runner.queue_result(RunnerResult(0, '{"result": {"devices": []}}', ""))
    self.assertEqual(commander.listAvailableAdapters(list_usb_adapters=False, list_network_adapters=True), [])
    self.assertEqual(commander._runner.logged_commands, [["mock", "adapter", "list", "--noconnect", "--net", "--json"]])

  def test_commander_base_listAvailableAdapters_failed(self):
    commander = MockCommander()
    commander._runner.queue_result(RunnerResult(1, "", ""))
    self.assertEqual(commander.listAvailableAdapters(list_usb_adapters=False, list_network_adapters=True), None)
    self.assertEqual(commander._runner.logged_commands, [["mock", "adapter", "list", "--noconnect", "--net", "--json"]])

  def test_commander_base_listAvailableAdapters_missing_result(self):
    commander = MockCommander()
    commander._runner.queue_result(RunnerResult(0, '{"success": true}', ""))
    self.assertEqual(commander.listAvailableAdapters(list_usb_adapters=False, list_network_adapters=True), None)
    self.assertEqual(commander._runner.logged_commands, [["mock", "adapter", "list", "--noconnect", "--net", "--json"]])

  def test_commander_base_listAvailableAdapters_missing_devices(self):
    commander = MockCommander()
    commander._runner.queue_result(RunnerResult(0, '{"result": ""}', ""))
    self.assertEqual(commander.listAvailableAdapters(list_usb_adapters=False, list_network_adapters=True), None)
    self.assertEqual(commander._runner.logged_commands, [["mock", "adapter", "list", "--noconnect", "--net", "--json"]])

  def test_commander_base_listAvailableAdapters_missing_adapter_ip(self):
    commander = MockCommander()
    commander._runner.queue_result(RunnerResult(0, '{"result": {"devices": [{"serial_number": "123456789", "adapter_nickname": "Adapter 1"}]}}', ""))
    self.assertEqual(commander.listAvailableAdapters(list_usb_adapters=False, list_network_adapters=True), [BasicAdapterInfo(jlink_serial_number="123456789", ip_address=None, nickname="Adapter 1")])
    self.assertEqual(commander._runner.logged_commands, [["mock", "adapter", "list", "--noconnect", "--net", "--json"]])

  def test_commander_base_listAvailableAdapters_missing_serial_number(self):
    commander = MockCommander()
    commander._runner.queue_result(RunnerResult(0, '{"result": {"devices": [{"adapter_ip": "192.168.1.100", "adapter_nickname": "Adapter 1"}]}}', ""))
    self.assertEqual(commander.listAvailableAdapters(list_usb_adapters=False, list_network_adapters=True), [BasicAdapterInfo(jlink_serial_number=None, ip_address="192.168.1.100", nickname="Adapter 1")])
    self.assertEqual(commander._runner.logged_commands, [["mock", "adapter", "list", "--noconnect", "--net", "--json"]])

  def test_commander_base_listAvailableAdapters_missing_nickname(self):
    commander = MockCommander()
    commander._runner.queue_result(RunnerResult(0, '{"result": {"devices": [{"adapter_ip": "192.168.1.100", "serial_number": "123456789"}]}}', ""))
    self.assertEqual(commander.listAvailableAdapters(list_usb_adapters=False, list_network_adapters=True), [BasicAdapterInfo(jlink_serial_number="123456789", ip_address="192.168.1.100", nickname=None)])
    self.assertEqual(commander._runner.logged_commands, [["mock", "adapter", "list", "--noconnect", "--net", "--json"]])

  def test_commander_base_listAvailableAdapters_multiple_devices(self):
    commander = MockCommander()
    commander._runner.queue_result(RunnerResult(0, '{"result": {"devices": [{"adapter_ip": "192.168.1.100", "serial_number": "123456789", "adapter_nickname": "Adapter 1"}, {"adapter_ip": "192.168.1.101", "serial_number": "123456790", "adapter_nickname": "Adapter 2"}]}}', ""))
    self.assertEqual(commander.listAvailableAdapters(list_usb_adapters=False, list_network_adapters=True), [BasicAdapterInfo(jlink_serial_number="123456789", ip_address="192.168.1.100", nickname="Adapter 1"), BasicAdapterInfo(jlink_serial_number="123456790", ip_address="192.168.1.101", nickname="Adapter 2")])
    self.assertEqual(commander._runner.logged_commands, [["mock", "adapter", "list", "--noconnect", "--net", "--json"]])

  def test_commander_base_runCommand(self):
    commander = MockCommander()
    self.assertEqual(commander.runCommand("command", "arg1", "arg2"), {"result": {}})
    self.assertEqual(commander._runner.logged_commands, [["mock", "command", "arg1", "arg2", "--json"]])

  def test_commander_base_runCommand_empty_args(self):
    commander = MockCommander()
    self.assertEqual(commander.runCommand("command", "", "arg2"), {"result": {}})
    self.assertEqual(commander._runner.logged_commands, [["mock", "command", "arg2", "--json"]])

  def test_commander_base_runCommand_none_args(self):
    commander = MockCommander()
    self.assertEqual(commander.runCommand("command", "arg1", None, "arg3"), {"result": {}})
    self.assertEqual(commander._runner.logged_commands, [["mock", "command", "arg1", "arg3", "--json"]])

  def test_commander_base_runCommand_whitespace_args(self):
    commander = MockCommander()
    self.assertEqual(commander.runCommand("command", "arg 1", "arg 2"), {"result": {}})
    self.assertEqual(commander._runner.logged_commands, [["mock", "command", "arg 1", "arg 2", "--json"]])

  def test_commander_base_runCommand_json_formatted_output_false(self):
    commander = MockCommander()
    self.assertEqual(commander.runCommand("command", "arg1", "arg2", json_formatted_output=False), CommanderResult(0, "", ""))
    self.assertEqual(commander._runner.logged_commands, [["mock", "command", "arg1", "arg2"]])

  def test_commander_base_runCommand_json_formatted_output_true(self):
    commander = MockCommander()
    self.assertEqual(commander.runCommand("command", "arg1", "arg2", json_formatted_output=True), {"result": {}})
    self.assertEqual(commander._runner.logged_commands, [["mock", "command", "arg1", "arg2", "--json"]])
    commander._runner.logged_commands.clear()

  def test_get_serial_number_option(self):
    commander = MockCommander(serial_number="123456789")
    self.assertEqual(commander._get_serial_number_option(), ["--serialno", "123456789"])

  def test_get_serial_number_option_none(self):
    commander = MockCommander(serial_number=None)
    self.assertEqual(commander._get_serial_number_option(), [])

  def test_get_serial_number_option_empty(self):
    commander = MockCommander(serial_number="")
    self.assertEqual(commander._get_serial_number_option(), [])

  def test_get_ip_address_option(self):
    commander = MockCommander(ip_address="192.168.1.100")
    self.assertEqual(commander._get_ip_address_option(), ["--ip", "192.168.1.100"])

  def test_get_ip_address_option_none(self):
    commander = MockCommander(ip_address=None)
    self.assertEqual(commander._get_ip_address_option(), [])

  def test_get_ip_address_option_empty(self):
    commander = MockCommander(ip_address="")
    self.assertEqual(commander._get_ip_address_option(), [])

  def test_get_serial_port_option(self):
    commander = MockCommander(serial_port="/dev/tty.usbmodem141101")
    self.assertEqual(commander._get_serial_port_option(), ["--identifybyserialport", "/dev/tty.usbmodem141101"])

  def test_get_serial_port_option_none(self):
    commander = MockCommander(serial_port=None)
    self.assertEqual(commander._get_serial_port_option(), [])

  def test_get_serial_port_option_empty(self):
    commander = MockCommander(serial_port="")
    self.assertEqual(commander._get_serial_port_option(), [])

  def test_get_debug_speed_option(self):
    commander = MockCommander(debug_speed=1000000)
    self.assertEqual(commander._get_debug_speed_option(), ["--speed", "1000000"])

  def test_get_debug_speed_option_none(self):
    commander = MockCommander(debug_speed=None)
    self.assertEqual(commander._get_debug_speed_option(), [])

  def test_get_debug_speed_option_empty(self):
    commander = MockCommander(debug_speed="")
    self.assertEqual(commander._get_debug_speed_option(), [])

  def test_get_debug_tif_option(self):
    commander = MockCommander(debug_tif="SWD")
    self.assertEqual(commander._get_debug_tif_option(), ["--tif", "SWD"])

  def test_get_debug_tif_option_none(self):
    commander = MockCommander(debug_tif=None)
    self.assertEqual(commander._get_debug_tif_option(), [])

  def test_get_debug_tif_option_empty(self):
    commander = MockCommander(debug_tif="")
    self.assertEqual(commander._get_debug_tif_option(), [])

  def test_get_debug_irpre_option(self):
    commander = MockCommander(debug_irpre=1000000)
    self.assertEqual(commander._get_debug_irpre_option(), ["--irpre", "1000000"])

  def test_get_debug_irpre_option_none(self):
    commander = MockCommander(debug_irpre=None)
    self.assertEqual(commander._get_debug_irpre_option(), [])

  def test_get_debug_irpre_option_empty(self):
    commander = MockCommander(debug_irpre="")
    self.assertEqual(commander._get_debug_irpre_option(), [])

  def test_get_debug_drpre_option(self):
    commander = MockCommander(debug_drpre=1000000)
    self.assertEqual(commander._get_debug_drpre_option(), ["--drpre", "1000000"])

  def test_get_debug_drpre_option_none(self):
    commander = MockCommander(debug_drpre=None)
    self.assertEqual(commander._get_debug_drpre_option(), [])

  def test_get_debug_drpre_option_empty(self):
    commander = MockCommander(debug_drpre="")
    self.assertEqual(commander._get_debug_drpre_option(), [])
