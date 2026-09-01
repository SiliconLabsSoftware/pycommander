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

from pycommander_cli.vuartstream import VuartStream

class TestVuartStream(unittest.TestCase):
  def test_vuartstream_init_ip_address(self):
    stream = VuartStream(ip_address="192.168.1.100")
    self.assertEqual(stream._commander._serial_number, None)
    self.assertEqual(stream._commander._ip_address, None)
    self.assertEqual(stream._commander._runner, stream._runner)
    self.assertEqual(stream._process, None)
    self.assertEqual(stream._args, ["vuart", "connect", "192.168.1.100"])

  def test_vuartstream_init_options(self):
    stream = VuartStream(
      ip_address="192.168.1.100",
      timeout_s=5,
      endmarker="DONE",
      lineending="none",
      command="status",
    )
    self.assertEqual(stream._args, [
      "vuart", "connect",
      "192.168.1.100",
      "--timeout", "5",
      "--endmarker", "DONE",
      "--lineending", "none",
      "--command", "status",
    ])

  def test_vuartstream_requires_ip_address(self):
    with self.assertRaises(TypeError):
      VuartStream()
