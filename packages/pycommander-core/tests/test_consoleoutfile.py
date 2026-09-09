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

import os
import sys
import threading
import unittest

from pycommander_core.consoleoutfile import ConsoleOutfile


class TestConsoleOutfile(unittest.TestCase):
  def test_create_posix_pipe_roundtrip(self):
    if sys.platform == "win32":
      self.skipTest("POSIX pipe sink")

    sink = ConsoleOutfile.create()
    self.addCleanup(sink.close)

    self.assertTrue(sink.path.isdigit())
    self.assertEqual(sink.pass_fds, (int(sink.path),))

    os.write(sink.pass_fds[0], b"Hello from target")
    sink.after_spawn()
    self.assertEqual(sink.read(32), b"Hello from target")
    self.assertEqual(sink.read(1), b"")

  def test_create_windows_named_pipe_roundtrip(self):
    if sys.platform != "win32":
      self.skipTest("Windows named pipe sink")

    import ctypes
    from ctypes import wintypes

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    CreateFileW = kernel32.CreateFileW
    CreateFileW.argtypes = [
      wintypes.LPCWSTR,
      wintypes.DWORD,
      wintypes.DWORD,
      wintypes.LPVOID,
      wintypes.DWORD,
      wintypes.DWORD,
      wintypes.HANDLE,
    ]
    CreateFileW.restype = wintypes.HANDLE
    WriteFile = kernel32.WriteFile
    WriteFile.argtypes = [
      wintypes.HANDLE,
      wintypes.LPCVOID,
      wintypes.DWORD,
      ctypes.POINTER(wintypes.DWORD),
      wintypes.LPVOID,
    ]
    WriteFile.restype = wintypes.BOOL
    CloseHandle = kernel32.CloseHandle
    GENERIC_WRITE = 0x40000000
    OPEN_EXISTING = 3
    INVALID_HANDLE_VALUE = wintypes.HANDLE(-1).value

    sink = ConsoleOutfile.create()
    self.addCleanup(sink.close)
    self.assertTrue(sink.path.lower().startswith(r"\\.\pipe\pycommander-console-"))
    self.assertEqual(sink.pass_fds, ())

    errors : list[BaseException] = []

    def client() -> None:
      try:
        handle = CreateFileW(sink.path, GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, None)
        if handle == INVALID_HANDLE_VALUE:
          raise OSError(ctypes.get_last_error(), "CreateFile failed")
        written = wintypes.DWORD(0)
        if not WriteFile(handle, b"Hello from target", 17, ctypes.byref(written), None):
          raise OSError(ctypes.get_last_error(), "WriteFile failed")
        CloseHandle(handle)
      except BaseException as exc:
        errors.append(exc)

    thread = threading.Thread(target=client)
    thread.start()
    sink.connect(lambda: False)
    payload = sink.read(32)
    thread.join(timeout=5)
    self.assertEqual(errors, [])
    self.assertEqual(payload, b"Hello from target")

  def test_close_is_idempotent(self):
    sink = ConsoleOutfile.create()
    sink.close()
    sink.close()
