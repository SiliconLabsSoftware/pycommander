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

from pycommander_core.vuartconsolestream_base import VuartConsoleStreamBase

from .mock_commander import MockCommander


class _FakeStdout:
  def __init__(self, output: str):
    self.buffer = io.BytesIO(output.encode("latin-1"))


class _FakeProcess:
  def __init__(self, output: str):
    self.stdout = _FakeStdout(output)

  def poll(self):
    return 0


class TestVuartConsoleStreamBase(unittest.TestCase):
  def test_vuartconsolestream_base_init(self):
    commander = MockCommander(
      serial_number="123456789",
      target_device="EFR32MG24",
      debug_speed=1000000,
      debug_tif="SWD",
      debug_irpre=1,
      debug_drpre=2,
    )
    vuartconsolestream = VuartConsoleStreamBase(
      commander=commander,
      ip_address="192.168.1.100",
      timeout_s=9.5,
      endmarker="STOP",
      lineending="lf",
      command=["Hello, World!", "Goodbye, World!"],
    )
    self.assertEqual(vuartconsolestream._commander, commander)
    self.assertEqual(vuartconsolestream._runner, commander._runner)
    self.assertEqual(vuartconsolestream._process, None)
    self.assertEqual(vuartconsolestream._args, [
      "vuart", "connect",
      "192.168.1.100",
      "--timeout", "9.5",
      "--endmarker", "STOP",
      "--lineending", "lf",
      "--command", "Hello, World!",
      "--command", "Goodbye, World!",
    ])

  def test_vuartconsolestream_base_init_defaults(self):
    commander = MockCommander()
    vuartconsolestream = VuartConsoleStreamBase(commander=commander, ip_address="1.2.3.4")
    self.assertEqual(vuartconsolestream._args, ["vuart", "connect", "1.2.3.4"])

  def test_vuartconsolestream_base_forwards_explicit_empty_values(self):
    commander = MockCommander()
    vuartconsolestream = VuartConsoleStreamBase(
      commander=commander,
      ip_address="1.2.3.4",
      timeout_s=0,
      endmarker="",
      lineending="",
    )
    self.assertEqual(vuartconsolestream._args, [
      "vuart", "connect", "1.2.3.4",
      "--timeout", "0",
      "--endmarker", "",
      "--lineending", "",
    ])

  def test_vuartconsolestream_base_init_command_string(self):
    commander = MockCommander()
    vuartconsolestream = VuartConsoleStreamBase(commander=commander, ip_address="1.2.3.4", command="status")
    self.assertEqual(vuartconsolestream._args, ["vuart", "connect", "1.2.3.4", "--command", "status"])

  def test_vuartconsolestream_base_requires_ip_address(self):
    commander = MockCommander()
    with self.assertRaises(ValueError):
      VuartConsoleStreamBase(commander=commander, ip_address="")

  def test_is_status_line(self):
    commander = MockCommander()
    vuartconsolestream = VuartConsoleStreamBase(commander=commander, ip_address="1.2.3.4")

    self.assertTrue(vuartconsolestream._is_status_line(""))
    self.assertTrue(vuartconsolestream._is_status_line("DONE"))
    self.assertTrue(vuartconsolestream._is_status_line("Connection established!"))
    self.assertTrue(vuartconsolestream._is_status_line("Attempting to connect to IP 192.168.1.100 at port 4900..."))
    self.assertTrue(vuartconsolestream._is_status_line("Socket was disconnected."))
    self.assertTrue(vuartconsolestream._is_status_line("Connection terminated by user."))
    self.assertTrue(vuartconsolestream._is_status_line("End marker 'STOP' found."))
    self.assertTrue(vuartconsolestream._is_status_line("Timeout: No data received for 5 seconds."))
    self.assertFalse(vuartconsolestream._is_status_line("Hello from target"))

  def test_is_error_line(self):
    commander = MockCommander()
    vuartconsolestream = VuartConsoleStreamBase(commander=commander, ip_address="1.2.3.4")

    self.assertTrue(vuartconsolestream._is_error_line("ERROR: Connection failed."))
    self.assertFalse(vuartconsolestream._is_error_line("Hello from target"))

  def test_iter_yields_data_and_skips_status(self):
    commander = MockCommander()
    vuartconsolestream = VuartConsoleStreamBase(commander=commander, ip_address="1.2.3.4")
    vuartconsolestream._process = _FakeProcess(
      "Attempting to connect to IP 192.168.1.100 at port 4900...\n"
      "Connection established!\n"
      "Hello from target\n"
      "\n"
      "End marker 'DONE' found.\n"
      "DONE\n"
    )

    self.assertEqual(list(vuartconsolestream), ["Hello from target\n"])

  def test_iter_yields_data_without_line_endings(self):
    commander = MockCommander()
    vuartconsolestream = VuartConsoleStreamBase(commander=commander, ip_address="1.2.3.4")
    vuartconsolestream._process = _FakeProcess("Hello from target")

    self.assertEqual(list(vuartconsolestream), ["Hello from target"])

  def test_iter_raises_on_error_line(self):
    commander = MockCommander()
    vuartconsolestream = VuartConsoleStreamBase(commander=commander, ip_address="1.2.3.4")
    vuartconsolestream._process = _FakeProcess("ERROR: Connection failed.\n")

    with self.assertRaises(RuntimeError) as context:
      next(vuartconsolestream)
    self.assertIn("ERROR:", str(context.exception))

  def test_open(self):
    commander = MockCommander()
    vuartconsolestream = VuartConsoleStreamBase(commander=commander, ip_address="1.2.3.4")

    self.assertEqual(vuartconsolestream._process, None)
    vuartconsolestream.open()
    self.assertEqual(commander._runner.logged_commands[0], ["mock", "vuart", "connect", "1.2.3.4"])

  def test_open_already_open(self):
    commander = MockCommander()
    vuartconsolestream = VuartConsoleStreamBase(commander=commander, ip_address="1.2.3.4")

    vuartconsolestream._process = 1 # Just not None
    with self.assertRaises(RuntimeError):
      vuartconsolestream.open()

  def test_close(self):
    commander = MockCommander()
    vuartconsolestream = VuartConsoleStreamBase(commander=commander, ip_address="1.2.3.4")

    vuartconsolestream._process = 1 # Just not None
    vuartconsolestream.close()
    self.assertEqual(vuartconsolestream._process, None)

  def test_close_not_open(self):
    commander = MockCommander()
    vuartconsolestream = VuartConsoleStreamBase(commander=commander, ip_address="1.2.3.4")

    # It's okay
    vuartconsolestream.close()

  def test_next_not_open(self):
    commander = MockCommander()
    vuartconsolestream = VuartConsoleStreamBase(commander=commander, ip_address="1.2.3.4")

    with self.assertRaises(RuntimeError):
      next(vuartconsolestream)
