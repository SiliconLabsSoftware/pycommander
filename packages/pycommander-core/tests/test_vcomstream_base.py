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

from pycommander_core.vcomstream_base import VcomStreamBase

from .mock_commander import MockCommander


class _FakeStdout:
  def __init__(self, output: str):
    self.buffer = io.BytesIO(output.encode("latin-1"))


class _FakeProcess:
  def __init__(self, output: str):
    self.stdout = _FakeStdout(output)

  def poll(self):
    return 0


class TestVcomStreamBase(unittest.TestCase):
  def test_vcomstream_base_init_serial_number(self):
    commander = MockCommander(
      serial_number="123456789",
      target_device="EFR32MG24",
      debug_speed=1000000,
      debug_tif="SWD",
      debug_irpre=1,
      debug_drpre=2,
    )
    vcomstream = VcomStreamBase(
      commander=commander,
      hex_output=True,
      restartinisp=True,
      lineending="lf",
      command=["Hello, World!", "Goodbye, World!"],
    )
    self.assertEqual(vcomstream._commander, commander)
    self.assertEqual(vcomstream._runner, commander._runner)
    self.assertEqual(vcomstream._process, None)
    self.assertEqual(vcomstream._args, [
      "vcom", "connect",
      "--serialno", "123456789",
      "--device", "EFR32MG24",
      "--hex",
      "--restartinisp",
      "--lineending", "lf",
      "--command", "Hello, World!",
      "--command", "Goodbye, World!",
    ])

  def test_vcomstream_base_init_ip_address(self):
    commander = MockCommander(ip_address="192.168.1.100")
    vcomstream = VcomStreamBase(
      commander=commander,
      command="status",
    )
    self.assertEqual(vcomstream._args, [
      "vcom", "connect",
      "--ip", "192.168.1.100",
      "--command", "status",
    ])

  def test_vcomstream_base_init_serial_port(self):
    commander = MockCommander(serial_port="/dev/tty.usbmodem141101")
    vcomstream = VcomStreamBase(commander=commander, restartinisp=True)
    self.assertEqual(vcomstream._args, [
      "vcom", "connect",
      "--identifybyserialport", "/dev/tty.usbmodem141101",
      "--restartinisp",
    ])

  def test_vcomstream_base_init_defaults(self):
    commander = MockCommander()
    vcomstream = VcomStreamBase(commander=commander)
    self.assertEqual(vcomstream._args, ["vcom", "connect"])

  def test_is_status_line(self):
    commander = MockCommander()
    vcomstream = VcomStreamBase(commander=commander)

    self.assertTrue(vcomstream._is_status_line(""))
    self.assertTrue(vcomstream._is_status_line("DONE"))
    self.assertTrue(vcomstream._is_status_line("Connection established!"))
    self.assertTrue(vcomstream._is_status_line("Attempting to connect to IP 192.168.1.100 at port 4901..."))
    self.assertTrue(vcomstream._is_status_line("Opening serial port 'tty.usbmodem141101'..."))
    self.assertTrue(vcomstream._is_status_line("Socket was disconnected."))
    self.assertTrue(vcomstream._is_status_line("Serial port was disconnected."))
    self.assertTrue(vcomstream._is_status_line("Connection terminated by user."))
    self.assertTrue(vcomstream._is_status_line("Target restarted in ISP mode."))
    self.assertFalse(vcomstream._is_status_line("Hello from target"))

  def test_is_error_line(self):
    commander = MockCommander()
    vcomstream = VcomStreamBase(commander=commander)

    self.assertTrue(vcomstream._is_error_line("ERROR: Error opening serial port: Device not found"))
    self.assertFalse(vcomstream._is_error_line("Hello from target"))

  def test_iter_yields_data_and_skips_status(self):
    commander = MockCommander()
    vcomstream = VcomStreamBase(commander=commander)
    vcomstream._process = _FakeProcess(
      "Opening serial port 'tty.usbmodem141101'...\n"
      "Connection established!\n"
      "Hello from target\n"
      "\n"
      "Connection terminated by user.\n"
      "DONE\n"
    )

    self.assertEqual(list(vcomstream), ["Hello from target\n"])

  def test_iter_yields_data_without_line_endings(self):
    commander = MockCommander()
    vcomstream = VcomStreamBase(commander=commander)
    vcomstream._process = _FakeProcess("Hello from target")

    self.assertEqual(list(vcomstream), ["Hello from target"])

  def test_iter_raises_on_error_line(self):
    commander = MockCommander()
    vcomstream = VcomStreamBase(commander=commander)
    vcomstream._process = _FakeProcess("ERROR: Error opening serial port: Device not found\n")

    with self.assertRaises(RuntimeError) as context:
      next(vcomstream)
    self.assertIn("ERROR:", str(context.exception))

  def test_open(self):
    commander = MockCommander()
    vcomstream = VcomStreamBase(commander=commander)

    self.assertEqual(vcomstream._process, None)
    vcomstream.open()
    self.assertEqual(commander._runner.logged_commands[0], ["mock", "vcom", "connect"])

  def test_open_already_open(self):
    commander = MockCommander()
    vcomstream = VcomStreamBase(commander=commander)

    vcomstream._process = 1 # Just not None
    with self.assertRaises(RuntimeError):
      vcomstream.open()

  def test_close(self):
    commander = MockCommander()
    vcomstream = VcomStreamBase(commander=commander)

    vcomstream._process = 1 # Just not None
    vcomstream.close()
    self.assertEqual(vcomstream._process, None)

  def test_close_not_open(self):
    commander = MockCommander()
    vcomstream = VcomStreamBase(commander=commander)

    # It's okay
    vcomstream.close()

  def test_next_not_open(self):
    commander = MockCommander()
    vcomstream = VcomStreamBase(commander=commander)

    with self.assertRaises(RuntimeError):
      next(vcomstream)
