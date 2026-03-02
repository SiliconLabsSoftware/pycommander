import unittest

from pycommander_core._utils import sanitize_args

class TestUtils(unittest.TestCase):
  def test_sanitize_args(self):
    self.assertEqual(sanitize_args(["command", "arg1", "arg2"]), ["command", "arg1", "arg2"])
    self.assertEqual(sanitize_args(["command", "arg 1", "arg 2"]), ["command", "arg 1", "arg 2"])
    self.assertEqual(sanitize_args(["command", "", " ", " arg2 "]), ["command", "arg2"])
    self.assertEqual(sanitize_args(["command", None, "arg3"]), ["command", "arg3"])
    self.assertEqual(sanitize_args(["command", "arg1", None, "arg3"]), ["command", "arg1", "arg3"])
    self.assertEqual(sanitize_args(["command", "arg1", "arg2", "arg3"]), ["command", "arg1", "arg2", "arg3"])
