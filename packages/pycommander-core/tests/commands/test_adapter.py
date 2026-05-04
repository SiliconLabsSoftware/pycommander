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

from ..mock_commander import MockCommander


class TestAdapter(unittest.TestCase):
  def test_get_general_args(self):
    # Initialized with serial number
    commander = MockCommander(serial_number="123456789")
    args = commander.adapter._get_general_args()
    self.assertEqual(args, ["--serialno", "123456789"])

    # Initialized with ip address
    commander = MockCommander(ip_address="192.168.1.100")
    args = commander.adapter._get_general_args()
    self.assertEqual(args, ["--ip", "192.168.1.100"])

    # Initialized with serial port
    commander = MockCommander(serial_port="/dev/tty.usbmodem141101")
    args = commander.adapter._get_general_args()
    self.assertEqual(args, ["--identifybyserialport", "/dev/tty.usbmodem141101"])

    # Serial number as kwarg
    commander = MockCommander()
    args = commander.adapter._get_general_args(serial_number="123456789")
    self.assertEqual(args, ["--serialno", "123456789"])

    # Ip address as kwarg
    commander = MockCommander()
    args = commander.adapter._get_general_args(ip_address="192.168.1.100")
    self.assertEqual(args, ["--ip", "192.168.1.100"])

    # Serial port as kwarg
    commander = MockCommander()
    args = commander.adapter._get_general_args(serial_port="/dev/tty.usbmodem141101")
    self.assertEqual(args, ["--identifybyserialport", "/dev/tty.usbmodem141101"])

  def test_adapter_dbgmode_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.adapter.dbgmode()
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected_command = ["mock", "adapter", "dbgmode", "--serialno", "123456789", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected_command)
    commander._runner.logged_commands.clear()

    commander.adapter.dbgmode("MCU")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected_command = ["mock", "adapter", "dbgmode", "MCU", "--serialno", "123456789", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected_command)

  def test_adapter_drivermode_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.adapter.drivermode()
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected_command = ["mock", "adapter", "drivermode", "--serialno", "123456789", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected_command)
    commander._runner.logged_commands.clear()

    commander.adapter.drivermode("winusb")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected_command = ["mock", "adapter", "drivermode", "winusb", "--serialno", "123456789", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected_command)

  def test_adapter_fwupgrade_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.adapter.fwupgrade()
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected_command = ["mock", "adapter", "fwupgrade", "--serialno", "123456789", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected_command)
    commander._runner.logged_commands.clear()

    commander.adapter.fwupgrade("firmware.emz", False)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected_command = ["mock", "adapter", "fwupgrade", "firmware.emz", "--serialno", "123456789", "--nocheck", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected_command)

  def test_adapter_fwupgradecheck_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.adapter.fwupgradecheck()
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected_command = ["mock", "adapter", "fwupgradecheck", "--serialno", "123456789", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected_command)

  def test_adapter_ip_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.adapter.ip()
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected_command = ["mock", "adapter", "ip", "--serialno", "123456789", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected_command)
    commander._runner.logged_commands.clear()

    commander.adapter.ip(dhcp=True, addr="192.168.1.100", dns="192.168.1.1", gw="192.168.1.1")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected_command = ["mock", "adapter", "ip", "--serialno", "123456789", "--dhcp", "--addr", "192.168.1.100", "--dns", "192.168.1.1", "--gw", "192.168.1.1", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected_command)
    commander._runner.logged_commands.clear()

  def test_adapter_list_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.adapter.list()
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected_command = ["mock", "adapter", "list", "--serialno", "123456789", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected_command)
    commander._runner.logged_commands.clear()

    commander.adapter.list(net=True, filter_regex=".*", connect=False)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected_command = ["mock", "adapter", "list", "--serialno", "123456789", "--net", "--filter", ".*", "--noconnect", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected_command)

  def test_adapter_nick_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.adapter.nick()
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected_command = ["mock", "adapter", "nick", "--serialno", "123456789", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected_command)
    commander._runner.logged_commands.clear()

    commander.adapter.nick("My Adapter")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected_command = ["mock", "adapter", "nick", "My Adapter", "--serialno", "123456789", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected_command)
    commander._runner.logged_commands.clear()

    commander.adapter.nick(clear=True)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected_command = ["mock", "adapter", "nick", "--serialno", "123456789", "--clear", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected_command)

  def test_adapter_power_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.adapter.power()
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected_command = ["mock", "adapter", "power", "--serialno", "123456789", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected_command)
    commander._runner.logged_commands.clear()

    commander.adapter.power("on")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected_command = ["mock", "adapter", "power", "on", "--serialno", "123456789", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected_command)

  def test_adapter_probe_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.adapter.probe()
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected_command = ["mock", "adapter", "probe", "--serialno", "123456789", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected_command)
    commander._runner.logged_commands.clear()

    commander.adapter.probe(fw=True, kit=True, boards=True)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected_command = ["mock", "adapter", "probe", "--serialno", "123456789", "--fw", "--kit", "--boards", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected_command)

  def test_adapter_reset_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.adapter.reset()
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected_command = ["mock", "adapter", "reset", "--serialno", "123456789", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected_command)

  def test_adapter_voltage_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.adapter.voltage()
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected_command = ["mock", "adapter", "voltage", "--serialno", "123456789", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected_command)
    commander._runner.logged_commands.clear()

    commander.adapter.voltage("3.3", False)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected_command = ["mock", "adapter", "voltage", "3.3", "--serialno", "123456789", "--nocalibrate", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected_command)
