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
import sys
import unittest

from pycommander_core.consolestream import ConsoleStream

from .mock_commander import MockCommander
from .mock_runner import assert_command_with_outfile


class _TestConsoleStream(ConsoleStream):
  _STREAM_NAME = "TestConsoleStream"
  _COMMAND = ("test", "stream")
  _INCLUDE_CONNECTION_OPTIONS = False
  _INCLUDE_DEBUG_OPTIONS = False


class _FakeOutfile:
  def __init__(self, output: bytes):
    self._buffer = io.BytesIO(output)

  def connect(self, should_abort):
    return None

  def read(self, n: int = 4096) -> bytes:
    return self._buffer.read(n)

  def close(self):
    return None


class _FakeStdout:
  def __init__(self, output: str):
    self._buffer = io.StringIO(output)

  def readline(self) -> str:
    return self._buffer.readline()


class _FakeProcess:
  def __init__(self, stdout: str = ""):
    self.stdout = _FakeStdout(stdout)

  def poll(self):
    return 0


class TestConsoleStream(unittest.TestCase):
  def test_init_args(self):
    stream = _TestConsoleStream(commander=MockCommander())
    self.assertEqual(stream._args, ["test", "stream"])
    self.assertIsNone(stream._process)
    self.assertIsNone(stream._outfile)

  def test_open_appends_outfile(self):
    commander = MockCommander()
    stream = _TestConsoleStream(commander=commander)
    stream.open()
    self.addCleanup(stream.close)
    assert_command_with_outfile(self, commander._runner.logged_commands[0], ["mock", "test", "stream"])
    self.assertIsNotNone(stream._process)
    self.assertIsNotNone(stream._outfile)
    if sys.platform != "win32":
      self.assertEqual(len(commander._runner.last_pass_fds), 1)
    else:
      self.assertEqual(commander._runner.last_pass_fds, ())

  def test_open_already_open(self):
    stream = _TestConsoleStream(commander=MockCommander())
    stream._process = 1
    with self.assertRaises(RuntimeError):
      stream.open()

  def test_close(self):
    stream = _TestConsoleStream(commander=MockCommander())
    stream._process = 1
    stream.close()
    self.assertIsNone(stream._process)
    self.assertIsNone(stream._outfile)

  def test_close_not_open(self):
    stream = _TestConsoleStream(commander=MockCommander())
    stream.close()

  def test_next_not_open(self):
    stream = _TestConsoleStream(commander=MockCommander())
    with self.assertRaises(RuntimeError):
      next(stream)

  def test_iter_yields_device_data_and_ignores_status(self):
    stream = _TestConsoleStream(commander=MockCommander())
    stream._process = _FakeProcess(
      "RTT successfully initialized.\n"
      "WARNING: Channel 8 may be used internally\n"
      "DONE\n"
    )
    stream._outfile = _FakeOutfile(b"Hello from target\n\nMore data")

    self.assertEqual(list(stream), ["Hello from target\n\nMore data"])

  def test_iter_yields_data_without_line_endings(self):
    stream = _TestConsoleStream(commander=MockCommander())
    stream._process = _FakeProcess()
    stream._outfile = _FakeOutfile(b"Hello from target")

    self.assertEqual(list(stream), ["Hello from target"])

  def test_iter_raises_on_error_line(self):
    stream = _TestConsoleStream(commander=MockCommander())
    stream._process = _FakeProcess("ERROR: Could not initialize RTT connection over JLink!\n")
    stream._outfile = _FakeOutfile(b"")

    with self.assertRaises(RuntimeError) as context:
      next(stream)
    self.assertIn("ERROR:", str(context.exception))

  def test_is_error_line(self):
    stream = _TestConsoleStream(commander=MockCommander())
    self.assertTrue(stream._is_error_line("ERROR: Failed to open JLink"))
    self.assertFalse(stream._is_error_line("Hello from target"))
