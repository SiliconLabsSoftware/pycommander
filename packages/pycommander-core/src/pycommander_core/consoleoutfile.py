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
import uuid
from collections.abc import Callable


if sys.platform == "win32":
  import ctypes
  import msvcrt
  from ctypes import wintypes

  _KERNEL32 = ctypes.WinDLL("kernel32", use_last_error=True)

  _PIPE_ACCESS_INBOUND = 0x00000001
  _PIPE_TYPE_BYTE = 0x00000000
  _PIPE_READMODE_BYTE = 0x00000000
  _PIPE_WAIT = 0x00000000
  _PIPE_REJECT_REMOTE_CLIENTS = 0x00000008
  _ERROR_PIPE_CONNECTED = 535
  _INVALID_HANDLE_VALUE = wintypes.HANDLE(-1).value

  _CreateNamedPipeW = _KERNEL32.CreateNamedPipeW
  _CreateNamedPipeW.argtypes = [
    wintypes.LPCWSTR,
    wintypes.DWORD,
    wintypes.DWORD,
    wintypes.DWORD,
    wintypes.DWORD,
    wintypes.DWORD,
    wintypes.DWORD,
    wintypes.LPVOID,
  ]
  _CreateNamedPipeW.restype = wintypes.HANDLE

  _ConnectNamedPipe = _KERNEL32.ConnectNamedPipe
  _ConnectNamedPipe.argtypes = [wintypes.HANDLE, wintypes.LPVOID]
  _ConnectNamedPipe.restype = wintypes.BOOL

  _CloseHandle = _KERNEL32.CloseHandle
  _CloseHandle.argtypes = [wintypes.HANDLE]
  _CloseHandle.restype = wintypes.BOOL


class ConsoleOutfile:
  """Device-output sink passed to Commander via ``--outfile``.

  On POSIX this is an anonymous pipe whose write end is inherited as a numeric
  file descriptor. On Windows this is a local named pipe at ``\\\\.\\pipe\\...``.
  """

  def __init__(self,
               path: str,
               read_fd: int | None = None,
               pass_fds: tuple[int, ...] = (),
               write_fd: int | None = None,
               windows_handle: int | None = None):
    self.path : str = path
    self.pass_fds : tuple[int, ...] = pass_fds
    self._read_fd : int | None = read_fd
    self._write_fd : int | None = write_fd
    self._windows_handle : int | None = windows_handle
    self._windows_connected : bool = False
    self._lock = threading.Lock()

  @classmethod
  def create(cls) -> "ConsoleOutfile":
    if sys.platform == "win32":
      return cls._create_windows_named_pipe()
    return cls._create_posix_pipe()

  @classmethod
  def _create_posix_pipe(cls) -> "ConsoleOutfile":
    read_fd, write_fd = os.pipe()
    return cls(path=str(write_fd), read_fd=read_fd, pass_fds=(write_fd,), write_fd=write_fd)

  @classmethod
  def _create_windows_named_pipe(cls) -> "ConsoleOutfile":
    path = rf"\\.\pipe\pycommander-console-{os.getpid()}-{uuid.uuid4().hex}"
    handle = _CreateNamedPipeW(
      path,
      _PIPE_ACCESS_INBOUND,
      _PIPE_TYPE_BYTE | _PIPE_READMODE_BYTE | _PIPE_WAIT | _PIPE_REJECT_REMOTE_CLIENTS,
      1,
      65536,
      65536,
      5000,
      None,
    )
    if handle == _INVALID_HANDLE_VALUE:
      raise OSError(ctypes.get_last_error(), f"CreateNamedPipe failed for {path}")
    return cls(path=path, windows_handle=int(handle))

  def after_spawn(self) -> None:
    """Release the parent's copy of the write end after Commander has started."""
    if self._write_fd is not None:
      os.close(self._write_fd)
      self._write_fd = None

  def connect(self, should_abort: Callable[[], bool]) -> None:
    """Wait for Commander to open the Windows named pipe.

    ``should_abort`` is polled so a process that exits before opening the pipe
    does not block forever. POSIX pipes need no handshake.
    """
    if sys.platform != "win32" or self._windows_connected:
      return

    errors : list[BaseException] = []
    done = threading.Event()

    def _connect() -> None:
      try:
        self._adopt_windows_client()
      except BaseException as exc:
        errors.append(exc)
      finally:
        done.set()

    thread = threading.Thread(target=_connect, daemon=True)
    thread.start()
    while not done.wait(0.05):
      if should_abort():
        self._close_windows_handle()
        thread.join(timeout=1.0)
        return

    if errors and not should_abort():
      raise errors[0]

  def read(self, n: int = 4096) -> bytes:
    if self._read_fd is None:
      return b""
    return os.read(self._read_fd, n)

  def close(self) -> None:
    self._close_windows_handle()
    if self._write_fd is not None:
      try:
        os.close(self._write_fd)
      except OSError:
        pass
      self._write_fd = None
    if self._read_fd is not None:
      try:
        os.close(self._read_fd)
      except OSError:
        pass
      self._read_fd = None

  def _adopt_windows_client(self) -> None:
    with self._lock:
      handle = self._windows_handle
    if handle is None:
      return

    if not _ConnectNamedPipe(handle, None):
      error = ctypes.get_last_error()
      if error != _ERROR_PIPE_CONNECTED:
        raise OSError(error, f"ConnectNamedPipe failed: {error}")

    with self._lock:
      if self._windows_handle != handle:
        return
      self._read_fd = msvcrt.open_osfhandle(handle, os.O_RDONLY)
      self._windows_handle = None
      self._windows_connected = True

  def _close_windows_handle(self) -> None:
    with self._lock:
      handle = self._windows_handle
      self._windows_handle = None
    if handle is not None:
      _CloseHandle(handle)
