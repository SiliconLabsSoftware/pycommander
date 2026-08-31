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

from pycommander_cli.swostream import SwoStream

class TestSwoStream(unittest.TestCase):
  def test_swostream_init_serial_number(self):
    stream = SwoStream(serial_number="123456789")
    self.assertEqual(stream._commander._serial_number, "123456789")
    self.assertEqual(stream._commander._runner, stream._runner)
    self.assertEqual(stream._process, None)
    self.assertEqual(stream._args, ["swo", "read", "--serialno", "123456789"])

  def test_swostream_init_ip_address(self):
    stream = SwoStream(ip_address="192.168.1.100")
    self.assertEqual(stream._commander._ip_address, "192.168.1.100")
    self.assertEqual(stream._commander._runner, stream._runner)
    self.assertEqual(stream._process, None)
    self.assertEqual(stream._args, ["swo", "read", "--ip", "192.168.1.100"])

  def test_swostream_init_options(self):
    stream = SwoStream(
      serial_number="123456789",
      target_device="EFR32MG24",
      swospeed_hz=1000000,
      timeout_s=2,
      endmarker="cafeface",
      hex_output=True,
      noreset=True,
      channel=3,
      monitorall=True,
    )
    self.assertEqual(stream._commander._target_device, "EFR32MG24")
    self.assertEqual(stream._args, [
      "swo", "read",
      "--serialno", "123456789",
      "--device", "EFR32MG24",
      "--swospeed", "1000000",
      "--timeout", "2",
      "--endmarker", "cafeface",
      "--hex",
      "--noreset",
      "--channel", "3",
      "--monitorall",
    ])
