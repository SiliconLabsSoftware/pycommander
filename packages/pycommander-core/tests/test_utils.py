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

from pycommander_core._utils import sanitize_args

class TestUtils(unittest.TestCase):
  def test_sanitize_args(self):
    self.assertEqual(sanitize_args(["command", "arg1", "arg2"]), ["command", "arg1", "arg2"])
    self.assertEqual(sanitize_args(["command", "arg 1", "arg 2"]), ["command", "arg 1", "arg 2"])
    self.assertEqual(sanitize_args(["command", "", " ", " arg2 "]), ["command", "arg2"])
    self.assertEqual(sanitize_args(["command", None, "arg3"]), ["command", "arg3"])
    self.assertEqual(sanitize_args(["command", "arg1", None, "None"]), ["command", "arg1", "None"])
    self.assertEqual(sanitize_args(["command", "arg1", "arg2", "arg3"]), ["command", "arg1", "arg2", "arg3"])
    self.assertEqual(sanitize_args(["command", 0, 0.0, 1, 2, 3.0, 4.5]), ["command", "0", "0.0", "1", "2", "3.0", "4.5"])
