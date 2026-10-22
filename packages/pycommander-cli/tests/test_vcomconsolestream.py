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

from pycommander_cli.vcomconsolestream import VcomConsoleStream

class TestVcomConsoleStream(unittest.TestCase):
  def test_vcomconsolestream_init_serial_number(self):
    stream = VcomConsoleStream(serial_number="123456789")
    self.assertEqual(stream._commander._serial_number, "123456789")
    self.assertEqual(stream._commander._runner, stream._runner)
    self.assertEqual(stream._process, None)
    self.assertEqual(stream._args, ["vcom", "connect", "--serialno", "123456789"])

  def test_vcomconsolestream_init_ip_address(self):
    stream = VcomConsoleStream(ip_address="192.168.1.100")
    self.assertEqual(stream._commander._ip_address, "192.168.1.100")
    self.assertEqual(stream._commander._runner, stream._runner)
    self.assertEqual(stream._process, None)
    self.assertEqual(stream._args, ["vcom", "connect", "--ip", "192.168.1.100"])

  def test_vcomconsolestream_init_options(self):
    stream = VcomConsoleStream(
      serial_number="123456789",
      hex_output=True,
      restartinisp=True,
      lineending="none",
      command="status",
    )
    self.assertEqual(stream._args, [
      "vcom", "connect",
      "--serialno", "123456789",
      "--hex",
      "--restartinisp",
      "--lineending", "none",
      "--command", "status",
    ])
