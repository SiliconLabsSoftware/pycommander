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

from pycommander_cli.rttconsolestream import RttConsoleStream

class TestRttConsoleStream(unittest.TestCase):
  def test_rttconsolestream_init_serial_number(self):
    stream = RttConsoleStream(serial_number="123456789")
    self.assertEqual(stream._commander._serial_number, "123456789")
    self.assertEqual(stream._commander._runner, stream._runner)
    self.assertEqual(stream._process, None)
    self.assertEqual(stream._args, ["rtt", "connect", "--serialno", "123456789"])

  def test_rttconsolestream_init_ip_address(self):
    stream = RttConsoleStream(ip_address="192.168.1.100")
    self.assertEqual(stream._commander._ip_address, "192.168.1.100")
    self.assertEqual(stream._commander._runner, stream._runner)
    self.assertEqual(stream._process, None)
    self.assertEqual(stream._args, ["rtt", "connect", "--ip", "192.168.1.100"])

  def test_rttconsolestream_init_options(self):
    stream = RttConsoleStream(
      serial_number="123456789",
      target_device="EFR32MG24",
      timeout_s=5,
      endmarker="DONE",
      blockaddress=0x20000000,
      readbuffer="Terminal",
      writebuffer=0,
      terminal=1,
      noreset=True,
      lineending="none",
      command="status",
    )
    self.assertEqual(stream._commander._target_device, "EFR32MG24")
    self.assertEqual(stream._args, [
      "rtt", "connect",
      "--serialno", "123456789",
      "--device", "EFR32MG24",
      "--timeout", "5",
      "--endmarker", "DONE",
      "--blockaddress", "0x20000000",
      "--readbuffer", "Terminal",
      "--writebuffer", "0",
      "--terminal", "1",
      "--noreset",
      "--lineending", "none",
      "--command", "status",
    ])
