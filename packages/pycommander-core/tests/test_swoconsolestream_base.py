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

import io
import unittest

from pycommander_core.swoconsolestream_base import SwoConsoleStreamBase

from .mock_commander import MockCommander


class _FakeStdout:
  def __init__(self, output: str):
    self.buffer = io.BytesIO(output.encode("latin-1"))


class _FakeProcess:
  def __init__(self, output: str):
    self.stdout = _FakeStdout(output)

  def poll(self):
    return 0


class TestSwoConsoleStreamBase(unittest.TestCase):
  def test_swoconsolestream_base_init_serial_number(self):
    commander = MockCommander(
      serial_number="123456789",
      target_device="EFR32MG24",
      debug_speed=1000000,
      debug_tif="SWD",
      debug_irpre=1,
      debug_drpre=2,
    )
    swoconsolestream = SwoConsoleStreamBase(
      commander=commander,
      swospeed_hz=1000000,
      timeout_s=5,
      endmarker="--finished--",
      hex_output=True,
      noreset=True,
      channel=3,
      monitorall=True,
    )
    self.assertEqual(swoconsolestream._commander, commander)
    self.assertEqual(swoconsolestream._runner, commander._runner)
    self.assertEqual(swoconsolestream._process, None)
    self.assertEqual(swoconsolestream._args, [
      "swo", "read",
      "--serialno", "123456789",
      "--device", "EFR32MG24",
      "--speed", "1000000",
      "--tif", "SWD",
      "--irpre", "1",
      "--drpre", "2",
      "--swospeed", "1000000",
      "--timeout", "5",
      "--endmarker", "--finished--",
      "--hex",
      "--noreset",
      "--channel", "3",
      "--monitorall",
    ])

  def test_swoconsolestream_base_init_ip_address(self):
    commander = MockCommander(ip_address="192.168.1.100")
    swoconsolestream = SwoConsoleStreamBase(
      commander=commander,
      swospeed_hz=875000,
      timeout_s=1.5,
      endmarker="stop",
    )
    self.assertEqual(swoconsolestream._commander, commander)
    self.assertEqual(swoconsolestream._runner, commander._runner)
    self.assertEqual(swoconsolestream._process, None)
    self.assertEqual(swoconsolestream._args, [
      "swo", "read",
      "--ip", "192.168.1.100",
      "--swospeed", "875000",
      "--timeout", "1.5",
      "--endmarker", "stop",
    ])

  def test_swoconsolestream_base_init_serial_port(self):
    commander = MockCommander(serial_port="/dev/tty.usbmodem141101")
    swoconsolestream = SwoConsoleStreamBase(commander=commander, noreset=True)
    self.assertEqual(swoconsolestream._commander, commander)
    self.assertEqual(swoconsolestream._runner, commander._runner)
    self.assertEqual(swoconsolestream._process, None)
    self.assertEqual(swoconsolestream._args, [
      "swo", "read",
      "--identifybyserialport", "/dev/tty.usbmodem141101",
      "--noreset",
    ])

  def test_swoconsolestream_base_init_defaults(self):
    commander = MockCommander()
    swoconsolestream = SwoConsoleStreamBase(commander=commander)
    self.assertEqual(swoconsolestream._args, ["swo", "read"])

  def test_swoconsolestream_base_forwards_explicit_zero_and_empty_values(self):
    commander = MockCommander()
    swoconsolestream = SwoConsoleStreamBase(
      commander=commander,
      swospeed_hz=0,
      timeout_s=0,
      endmarker="",
    )
    self.assertEqual(swoconsolestream._args, [
      "swo", "read",
      "--swospeed", "0",
      "--timeout", "0",
      "--endmarker", "",
    ])

  def test_swoconsolestream_base_init_channel_zero(self):
    commander = MockCommander()
    swoconsolestream = SwoConsoleStreamBase(commander=commander, channel=0)
    self.assertEqual(swoconsolestream._args, ["swo", "read", "--channel", "0"])

  def test_is_status_line(self):
    commander = MockCommander()
    swoconsolestream = SwoConsoleStreamBase(commander=commander)

    self.assertTrue(swoconsolestream._is_status_line(""))
    self.assertTrue(swoconsolestream._is_status_line("   "))
    self.assertTrue(swoconsolestream._is_status_line("DONE"))
    self.assertTrue(swoconsolestream._is_status_line("SWO connection terminated."))
    self.assertTrue(swoconsolestream._is_status_line("CTRL+C entered, terminating SWO connection..."))
    self.assertTrue(swoconsolestream._is_status_line("Timeout: No SWO output for 1 seconds."))
    self.assertTrue(swoconsolestream._is_status_line("Timeout: No SWO output for 1 seconds on any channel."))
    self.assertTrue(swoconsolestream._is_status_line("End marker '--finished--' found."))
    self.assertTrue(swoconsolestream._is_status_line("End marker '--finished--' found on channel 3."))
    self.assertFalse(swoconsolestream._is_status_line("Hello from target"))

  def test_is_error_line(self):
    commander = MockCommander()
    swoconsolestream = SwoConsoleStreamBase(commander=commander)

    self.assertTrue(swoconsolestream._is_error_line("ERROR: Failed to open JLink"))
    self.assertTrue(swoconsolestream._is_error_line("ERROR: Failed to connect to SWO."))
    self.assertFalse(swoconsolestream._is_error_line("Hello from target"))

  def test_iter_yields_data_and_skips_status(self):
    commander = MockCommander()
    swoconsolestream = SwoConsoleStreamBase(commander=commander)
    swoconsolestream._process = _FakeProcess(
      "Hello from target\n"
      "\n"
      "WARNING: Channel 8 may be used internally\n"
      "SWO connection terminated.\n"
      "End marker 'DONE' found.\n"
      "DONE\n"
    )

    self.assertEqual(list(swoconsolestream), ["Hello from target\n"])

  def test_iter_yields_data_without_line_endings(self):
    commander = MockCommander()
    swoconsolestream = SwoConsoleStreamBase(commander=commander)
    swoconsolestream._process = _FakeProcess("Hello from target")

    self.assertEqual(list(swoconsolestream), ["Hello from target"])

  def test_iter_raises_on_error_line(self):
    commander = MockCommander()
    swoconsolestream = SwoConsoleStreamBase(commander=commander)
    swoconsolestream._process = _FakeProcess("ERROR: Unsupported device part number: EFR32\n")

    with self.assertRaises(RuntimeError) as context:
      next(swoconsolestream)
    self.assertIn("ERROR:", str(context.exception))

  def test_open(self):
    commander = MockCommander()
    swoconsolestream = SwoConsoleStreamBase(commander=commander)

    self.assertEqual(swoconsolestream._process, None)
    swoconsolestream.open()
    self.assertEqual(commander._runner.logged_commands[0], ["mock", "swo", "read"])

  def test_open_already_open(self):
    commander = MockCommander()
    swoconsolestream = SwoConsoleStreamBase(commander=commander)

    swoconsolestream._process = 1 # Just not None
    with self.assertRaises(RuntimeError):
      swoconsolestream.open()

  def test_close(self):
    commander = MockCommander()
    swoconsolestream = SwoConsoleStreamBase(commander=commander)

    swoconsolestream._process = 1 # Just not None
    swoconsolestream.close()
    self.assertEqual(swoconsolestream._process, None)

  def test_close_not_open(self):
    commander = MockCommander()
    swoconsolestream = SwoConsoleStreamBase(commander=commander)

    # It's okay
    swoconsolestream.close()

  def test_next_not_open(self):
    commander = MockCommander()
    swoconsolestream = SwoConsoleStreamBase(commander=commander)

    with self.assertRaises(RuntimeError):
      next(swoconsolestream)
