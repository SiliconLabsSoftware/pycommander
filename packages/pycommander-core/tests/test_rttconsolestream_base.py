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

from pycommander_core.rttconsolestream_base import RttConsoleStreamBase

from .mock_commander import MockCommander


class _FakeStdout:
  def __init__(self, output: str):
    self.buffer = io.BytesIO(output.encode("latin-1"))


class _FakeProcess:
  def __init__(self, output: str):
    self.stdout = _FakeStdout(output)

  def poll(self):
    return 0


class TestRttConsoleStreamBase(unittest.TestCase):
  def test_rttconsolestream_base_init_serial_number(self):
    commander = MockCommander(
      serial_number="123456789",
      target_device="EFR32MG24",
      debug_speed=1000000,
      debug_tif="SWD",
      debug_irpre=1,
      debug_drpre=2,
    )
    rttconsolestream = RttConsoleStreamBase(
      commander=commander,
      timeout_s=12.7,
      endmarker="END",
      blockaddress=0x25011337,
      readbuffer=1,
      writebuffer=2,
      terminal=11,
      noreset=True,
      lineending="lf",
      command=["Hello, World!", "Goodbye, World!"],
    )
    self.assertEqual(rttconsolestream._commander, commander)
    self.assertEqual(rttconsolestream._runner, commander._runner)
    self.assertEqual(rttconsolestream._process, None)
    self.assertEqual(rttconsolestream._args, [
      "rtt", "connect",
      "--serialno", "123456789",
      "--device", "EFR32MG24",
      "--speed", "1000000",
      "--tif", "SWD",
      "--irpre", "1",
      "--drpre", "2",
      "--timeout", "12.7",
      "--endmarker", "END",
      "--blockaddress", "0x25011337",
      "--readbuffer", "1",
      "--writebuffer", "2",
      "--terminal", "11",
      "--noreset",
      "--lineending", "lf",
      "--command", "Hello, World!",
      "--command", "Goodbye, World!",
    ])

  def test_rttconsolestream_base_init_ip_address(self):
    commander = MockCommander(ip_address="192.168.1.100")
    rttconsolestream = RttConsoleStreamBase(
      commander=commander,
      readbuffer="Terminal",
      writebuffer="Terminal",
      command="status",
    )
    self.assertEqual(rttconsolestream._args, [
      "rtt", "connect",
      "--ip", "192.168.1.100",
      "--readbuffer", "Terminal",
      "--writebuffer", "Terminal",
      "--command", "status",
    ])

  def test_rttconsolestream_base_init_serial_port(self):
    commander = MockCommander(serial_port="/dev/tty.usbmodem141101")
    rttconsolestream = RttConsoleStreamBase(commander=commander, noreset=True)
    self.assertEqual(rttconsolestream._args, [
      "rtt", "connect",
      "--identifybyserialport", "/dev/tty.usbmodem141101",
      "--noreset",
    ])

  def test_rttconsolestream_base_init_defaults(self):
    commander = MockCommander()
    rttconsolestream = RttConsoleStreamBase(commander=commander)
    self.assertEqual(rttconsolestream._args, ["rtt", "connect"])

  def test_rttconsolestream_base_forwards_explicit_empty_values(self):
    commander = MockCommander()
    rttconsolestream = RttConsoleStreamBase(
      commander=commander,
      timeout_s=0,
      endmarker="",
      lineending="",
    )
    self.assertEqual(rttconsolestream._args, [
      "rtt", "connect",
      "--timeout", "0",
      "--endmarker", "",
      "--lineending", "",
    ])

  def test_rttconsolestream_base_init_blockaddress_hex_string(self):
    commander = MockCommander()
    rttconsolestream = RttConsoleStreamBase(commander=commander, blockaddress="0x20000000")
    self.assertEqual(rttconsolestream._args, ["rtt", "connect", "--blockaddress", "0x20000000"])

  def test_rttconsolestream_base_init_blockaddress_hex_number(self):
    commander = MockCommander()
    rttconsolestream = RttConsoleStreamBase(commander=commander, blockaddress=0x20000000)
    self.assertEqual(rttconsolestream._args, ["rtt", "connect", "--blockaddress", "0x20000000"])

  def test_rttconsolestream_base_init_blockaddress_decimal_string(self):
    commander = MockCommander()
    rttconsolestream = RttConsoleStreamBase(commander=commander, blockaddress="536870912")
    self.assertEqual(rttconsolestream._args, ["rtt", "connect", "--blockaddress", "0x20000000"])

  def test_rttconsolestream_base_init_blockaddress_decimal_number(self):
    commander = MockCommander()
    rttconsolestream = RttConsoleStreamBase(commander=commander, blockaddress=536870912)
    self.assertEqual(rttconsolestream._args, ["rtt", "connect", "--blockaddress", "0x20000000"])

  def test_rttconsolestream_base_init_terminal_zero(self):
    commander = MockCommander()
    rttconsolestream = RttConsoleStreamBase(commander=commander, terminal=0)
    self.assertEqual(rttconsolestream._args, ["rtt", "connect", "--terminal", "0"])

  def test_is_status_line(self):
    commander = MockCommander()
    rttconsolestream = RttConsoleStreamBase(commander=commander)

    self.assertTrue(rttconsolestream._is_status_line(""))
    self.assertTrue(rttconsolestream._is_status_line("DONE"))
    self.assertTrue(rttconsolestream._is_status_line("RTT successfully initialized."))
    self.assertTrue(rttconsolestream._is_status_line("RTT block address: 0x20000000"))
    self.assertTrue(rttconsolestream._is_status_line("RTT console connected, enter CTRL+C to terminate."))
    self.assertTrue(rttconsolestream._is_status_line("Connection terminated by user."))
    self.assertTrue(rttconsolestream._is_status_line("End marker 'END' found."))
    self.assertTrue(rttconsolestream._is_status_line("Timeout: No data received for 5 seconds."))
    self.assertTrue(rttconsolestream._is_status_line("RTT read buffer 'Terminal' found."))
    self.assertFalse(rttconsolestream._is_status_line("Hello from target"))

  def test_is_error_line(self):
    commander = MockCommander()
    rttconsolestream = RttConsoleStreamBase(commander=commander)

    self.assertTrue(rttconsolestream._is_error_line("ERROR: Could not initialize RTT connection over JLink!"))
    self.assertFalse(rttconsolestream._is_error_line("Hello from target"))

  def test_iter_yields_data_and_skips_status(self):
    commander = MockCommander()
    rttconsolestream = RttConsoleStreamBase(commander=commander)
    rttconsolestream._process = _FakeProcess(
      "RTT successfully initialized.\n"
      "RTT console connected, enter CTRL+C to terminate.\n"
      "Hello from target\n"
      "\n"
      "End marker 'DONE' found.\n"
      "DONE\n"
    )

    self.assertEqual(list(rttconsolestream), ["Hello from target\n"])

  def test_iter_yields_data_without_line_endings(self):
    commander = MockCommander()
    rttconsolestream = RttConsoleStreamBase(commander=commander)
    rttconsolestream._process = _FakeProcess("Hello from target")

    self.assertEqual(list(rttconsolestream), ["Hello from target"])

  def test_iter_raises_on_error_line(self):
    commander = MockCommander()
    rttconsolestream = RttConsoleStreamBase(commander=commander)
    rttconsolestream._process = _FakeProcess("ERROR: RTT block is invalid.\n")

    with self.assertRaises(RuntimeError) as context:
      next(rttconsolestream)
    self.assertIn("ERROR:", str(context.exception))

  def test_open(self):
    commander = MockCommander()
    rttconsolestream = RttConsoleStreamBase(commander=commander)

    self.assertEqual(rttconsolestream._process, None)
    rttconsolestream.open()
    self.assertEqual(commander._runner.logged_commands[0], ["mock", "rtt", "connect"])

  def test_open_already_open(self):
    commander = MockCommander()
    rttconsolestream = RttConsoleStreamBase(commander=commander)

    rttconsolestream._process = 1 # Just not None
    with self.assertRaises(RuntimeError):
      rttconsolestream.open()

  def test_close(self):
    commander = MockCommander()
    rttconsolestream = RttConsoleStreamBase(commander=commander)

    rttconsolestream._process = 1 # Just not None
    rttconsolestream.close()
    self.assertEqual(rttconsolestream._process, None)

  def test_close_not_open(self):
    commander = MockCommander()
    rttconsolestream = RttConsoleStreamBase(commander=commander)

    # It's okay
    rttconsolestream.close()

  def test_next_not_open(self):
    commander = MockCommander()
    rttconsolestream = RttConsoleStreamBase(commander=commander)

    with self.assertRaises(RuntimeError):
      next(rttconsolestream)
