import unittest

import os
import sys
import subprocess
import tempfile
import shutil
import re

from pathlib import Path

from pycommander_core.runner import Runner
from pycommander_core.errors import PyCommanderInputError, PyCommanderRuntimeError, PyCommanderError

class TestRunner(unittest.TestCase):
  def test_runner_init(self):
    command = shutil.which("echo")
    if command is None:
      self.fail("echo command not found")

    runner = Runner(executable=command)
    self.assertEqual(runner._executable, command)
    self.assertEqual(runner._log_file_path, None)
    self.assertEqual(runner._timeout_s, 300)

    if sys.platform == "win32":
      self.assertIn("creationflags", runner._common_subprocess_kwargs)
      self.assertEqual(runner._common_subprocess_kwargs["creationflags"], subprocess.CREATE_NO_WINDOW)
    else:
      self.assertNotIn("creationflags", runner._common_subprocess_kwargs)

  def test_runner_init_missing_executable(self):
    with self.assertRaisesRegex(FileNotFoundError, f"Commander executable not found: {Path('mock')}"):
      Runner(executable=Path("mock"))

  def test_runner_init_not_a_file(self):
    temp_dir = Path(tempfile.mkdtemp(dir="."))

    with self.assertRaisesRegex(ValueError, f"Commander executable is not a file: {re.escape(str(temp_dir))}"):
      Runner(executable=temp_dir)

    temp_dir.rmdir()

  def test_runner_run_command_no_json(self):
    # Find the path to the echo command
    command = shutil.which("echo")
    if command is None:
      self.fail("echo command not found")

    runner = Runner(executable=command)
    result = runner.run("command", "arg1", "arg2", json_format=False)
    self.assertEqual(result.returncode, 0)
    self.assertEqual(result.output, "command arg1 arg2\n")

  def test_runner_run_command_json(self):
    # Find the path to the echo command
    command = shutil.which("echo")
    if command is None:
      self.fail("echo command not found")

    runner = Runner(executable=command)
    result = runner.run("command", "arg1", "arg2", json_format=True)
    self.assertEqual(result.returncode, 0)
    self.assertEqual(result.output, 'command arg1 arg2 --json\n')

  def test_runner_run_command_timeout(self):
    # Find the path to the sleep command
    command = shutil.which("sleep")
    if command is None:
      self.fail("sleep command not found")

    runner = Runner(executable=command, timeout_s=1)
    expected_command_line = [command, "3"]
    with self.assertRaisesRegex(TimeoutError, f"Command timed out: {re.escape(str(expected_command_line))}"):
      runner.run("3", json_format=False)

  def test_runner_run_command_input_error(self):
    command = shutil.which("bash")
    if command is None:
      self.fail("bash command not found")

    runner = Runner(executable=command)
    with self.assertRaises(PyCommanderInputError):
      runner.run("-c", "exit 255", json_format=False)

  def test_runner_run_command_runtime_error(self):
    command = shutil.which("bash")
    if command is None:
      self.fail("bash command not found")

    runner = Runner(executable=command)
    with self.assertRaises(PyCommanderRuntimeError):
      runner.run("-c", "exit 254", json_format=False)

  def test_runner_run_command_error(self):
    command = shutil.which("bash")
    if command is None:
      self.fail("bash command not found")

    runner = Runner(executable=command)
    with self.assertRaises(PyCommanderError):
      runner.run("-c", "exit 1", json_format=False)

  def test_runner_log_file_on_success(self):
    command = shutil.which("echo")
    if command is None:
      self.fail("echo command not found")

    tf = tempfile.NamedTemporaryFile(dir=".", suffix=".log", delete=False)
    self.addCleanup(os.remove, tf.name)

    runner = Runner(executable=command, log_file_path=Path(tf.name))
    runner.run("command", "arg1", "arg2", json_format=False)
    with open(tf.name, "r") as f:
      self.assertIn("command arg1 arg2", f.read())


  def test_runner_log_file_on_error(self):
    command = shutil.which("bash")
    if command is None:
      self.fail("bash command not found")

    tf =  tempfile.NamedTemporaryFile(dir=".", suffix=".log", delete=False)
    self.addCleanup(os.remove, tf.name)

    runner = Runner(executable=command, log_file_path=Path(tf.name))
    with self.assertRaises(PyCommanderInputError):
      runner.run("-c", "exit 255", json_format=False)
    with open(tf.name, "r") as f:
      self.assertIn("Command failed with return code 255:", f.read())

  def test_runner_log_file_on_timeout(self):
    command = shutil.which("sleep")
    if command is None:
      self.fail("sleep command not found")

    tf = tempfile.NamedTemporaryFile(dir=".", suffix=".log", delete=False)
    self.addCleanup(os.remove, tf.name)
    
    runner = Runner(executable=command, timeout_s=1, log_file_path=Path(tf.name))
    with self.assertRaises(TimeoutError):
      runner.run("3", json_format=False)
    with open(tf.name, "r") as f:
      self.assertIn("Command timed out:", f.read())

  def test_runner_open(self):
    command = shutil.which("sleep")
    if command is None:
      self.fail("sleep command not found")

    runner = Runner(executable=command)
    process = runner.open("10")
    self.addCleanup(process.kill)
    self.addCleanup(process.wait)

    self.assertIsInstance(process, subprocess.Popen)
    self.assertIsNone(process.poll())

  def test_runner_isAlive(self):
    command = shutil.which("sleep")
    if command is None:
      self.fail("sleep command not found")

    runner = Runner(executable=command)
    process = runner.open("10")
    self.addCleanup(process.kill)
    self.addCleanup(process.wait)

    self.assertTrue(runner.isAlive(process))
    self.assertFalse(runner.isAlive(None))

    process.kill()
    process.wait()
    self.assertFalse(runner.isAlive(process))

  def test_runner_wait(self):
    command = shutil.which("bash")
    if command is None:
      self.fail("bash command not found")

    runner = Runner(executable=command)
    process = runner.open("-c", "exit 42")

    returncode = runner.wait(process)
    self.assertEqual(returncode, 42)

  def test_runner_wait_timeout(self):
    command = shutil.which("sleep")
    if command is None:
      self.fail("sleep command not found")

    runner = Runner(executable=command)
    process = runner.open("10")
    self.addCleanup(process.kill)
    self.addCleanup(process.wait)

    with self.assertRaises(subprocess.TimeoutExpired):
      runner.wait(process, timeout_s=1)

  def test_runner_terminate(self):
    command = shutil.which("sleep")
    if command is None:
      self.fail("sleep command not found")

    runner = Runner(executable=command)
    process = runner.open("10")

    self.assertTrue(runner.isAlive(process))
    runner.terminate(process)
    process.wait()
    self.assertFalse(runner.isAlive(process))

  def test_runner_kill(self):
    command = shutil.which("sleep")
    if command is None:
      self.fail("sleep command not found")

    runner = Runner(executable=command)
    process = runner.open("10")

    self.assertTrue(runner.isAlive(process))
    runner.kill(process)
    process.wait()
    self.assertFalse(runner.isAlive(process))

  def test_runner_sendCtrlC(self):
    command = shutil.which("sleep")
    if command is None:
      self.fail("sleep command not found")

    runner = Runner(executable=command)
    process = runner.open("10")

    self.assertTrue(runner.isAlive(process))
    runner.sendCtrlC(process)
    process.wait()
    self.assertFalse(runner.isAlive(process))

  def test_runner_close(self):
    command = shutil.which("sleep")
    if command is None:
      self.fail("sleep command not found")

    runner = Runner(executable=command)
    process = runner.open("10")

    self.assertTrue(runner.isAlive(process))
    runner.close(process)
    self.assertFalse(runner.isAlive(process))
