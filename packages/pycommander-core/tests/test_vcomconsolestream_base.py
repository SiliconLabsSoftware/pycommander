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

from pycommander_core.vcomconsolestream_base import VcomConsoleStreamBase

from .mock_commander import MockCommander
from .mock_runner import assert_command_with_outfile


class TestVcomConsoleStreamBase(unittest.TestCase):
  def test_vcomconsolestream_base_init_serial_number(self):
    commander = MockCommander(
      serial_number="123456789",
      target_device="EFR32MG24",
      debug_speed=1000000,
      debug_tif="SWD",
      debug_irpre=1,
      debug_drpre=2,
    )
    vcomconsolestream = VcomConsoleStreamBase(
      commander=commander,
      hex_output=True,
      restartinisp=True,
      lineending="lf",
      command=["Hello, World!", "Goodbye, World!"],
    )
    self.assertEqual(vcomconsolestream._commander, commander)
    self.assertEqual(vcomconsolestream._runner, commander._runner)
    self.assertEqual(vcomconsolestream._process, None)
    self.assertEqual(vcomconsolestream._args, [
      "vcom", "connect",
      "--serialno", "123456789",
      "--device", "EFR32MG24",
      "--hex",
      "--restartinisp",
      "--lineending", "lf",
      "--command", "Hello, World!",
      "--command", "Goodbye, World!",
    ])

  def test_vcomconsolestream_base_init_ip_address(self):
    commander = MockCommander(ip_address="192.168.1.100")
    vcomconsolestream = VcomConsoleStreamBase(
      commander=commander,
      command="status",
    )
    self.assertEqual(vcomconsolestream._args, [
      "vcom", "connect",
      "--ip", "192.168.1.100",
      "--command", "status",
    ])

  def test_vcomconsolestream_base_init_serial_port(self):
    commander = MockCommander(serial_port="/dev/tty.usbmodem141101")
    vcomconsolestream = VcomConsoleStreamBase(commander=commander, restartinisp=True)
    self.assertEqual(vcomconsolestream._args, [
      "vcom", "connect",
      "--identifybyserialport", "/dev/tty.usbmodem141101",
      "--restartinisp",
    ])

  def test_vcomconsolestream_base_init_defaults(self):
    commander = MockCommander()
    vcomconsolestream = VcomConsoleStreamBase(commander=commander)
    self.assertEqual(vcomconsolestream._args, ["vcom", "connect"])

  def test_vcomconsolestream_base_forwards_explicit_empty_lineending(self):
    commander = MockCommander()
    vcomconsolestream = VcomConsoleStreamBase(commander=commander, lineending="")
    self.assertEqual(vcomconsolestream._args, [
      "vcom", "connect",
      "--lineending", "",
    ])

  def test_open(self):
    commander = MockCommander()
    vcomconsolestream = VcomConsoleStreamBase(commander=commander)

    self.assertEqual(vcomconsolestream._process, None)
    vcomconsolestream.open()
    self.addCleanup(vcomconsolestream.close)
    assert_command_with_outfile(self, commander._runner.logged_commands[0], ["mock", "vcom", "connect"])

  def test_open_already_open(self):
    commander = MockCommander()
    vcomconsolestream = VcomConsoleStreamBase(commander=commander)

    vcomconsolestream._process = 1 # Just not None
    with self.assertRaises(RuntimeError):
      vcomconsolestream.open()

  def test_close(self):
    commander = MockCommander()
    vcomconsolestream = VcomConsoleStreamBase(commander=commander)

    vcomconsolestream._process = 1 # Just not None
    vcomconsolestream.close()
    self.assertEqual(vcomconsolestream._process, None)

  def test_close_not_open(self):
    commander = MockCommander()
    vcomconsolestream = VcomConsoleStreamBase(commander=commander)

    # It's okay
    vcomconsolestream.close()

  def test_next_not_open(self):
    commander = MockCommander()
    vcomconsolestream = VcomConsoleStreamBase(commander=commander)

    with self.assertRaises(RuntimeError):
      next(vcomconsolestream)
