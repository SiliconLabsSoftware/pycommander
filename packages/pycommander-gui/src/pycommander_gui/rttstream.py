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

from pycommander_core.rttstream_base import RttStreamBase

from pycommander_gui.commander import Commander

class RttStream(RttStreamBase):
  """
  High-level read-only interface for RTT (Real Time Transfer) captures.
  This class can be used in a context manager to simplify the handling
  of opening and closing the RttStream. The stream works with any adapter
  that exposes a debug connection (Silicon Labs adapters and generic J-Link).

  Startup commands can be sent once after connect via ``command``. The stream
  itself does not accept further input.

  Args:
    serial_number: Serial number of the adapter
    ip_address: IP address of the adapter
    target_device: Target device part number
    timeout_s: Seconds without RTT data before the capture ends. Default is to never time out.
    endmarker: Stop the capture after this string is found in the RTT stream.
    blockaddress: Address of the RTT control block. If omitted, Commander searches automatically.
    readbuffer: RTT up-buffer index or name to read from. Defaults to 0.
    writebuffer: RTT down-buffer index or name used when sending ``command``. Defaults to 0.
    terminal: Virtual RTT terminal to read from (0-15). Only valid with the Terminal/0 read buffer.
    noreset: If True, do not reset the target when the RTT connection is opened.
    lineending: Line ending appended to ``command``: ``cr``, ``lf``, ``crlf``, or ``none``. Defaults to ``crlf``.
    command: Command(s) sent to the target immediately after connecting.

  Examples:
    with RttStream(serial_number="123456789", timeout_s=5, endmarker="DONE", command="status") as stream:
      for line in stream:
        print(line, end="", flush=True)
  """
  def __init__(self,
               serial_number: str | None = None,
               ip_address: str | None = None,
               target_device: str | None = None,
               timeout_s: float | None = None,
               endmarker: str | None = None,
               blockaddress: int | str | None = None,
               readbuffer: int | str | None = None,
               writebuffer: int | str | None = None,
               terminal: int | None = None,
               noreset: bool = False,
               lineending: str | None = None,
               command: str | list[str] | None = None):

    commander = Commander(serial_number=serial_number,
                          ip_address=ip_address,
                          target_device=target_device)

    super().__init__(commander=commander,
                     timeout_s=timeout_s,
                     endmarker=endmarker,
                     blockaddress=blockaddress,
                     readbuffer=readbuffer,
                     writebuffer=writebuffer,
                     terminal=terminal,
                     noreset=noreset,
                     lineending=lineending,
                     command=command)
