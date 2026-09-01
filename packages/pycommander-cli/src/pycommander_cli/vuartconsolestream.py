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

from pycommander_core.vuartconsolestream_base import VuartConsoleStreamBase

from pycommander_cli.commander import Commander

class VuartConsoleStream(VuartConsoleStreamBase):
  """
  High-level read-only interface for VUART captures.
  This class can be used in a context manager to simplify the handling
  of opening and closing the VuartConsoleStream. VUART is available only over IP.

  Startup commands can be sent once after connect via ``command``. The stream
  itself does not accept further input.

  Args:
    ip_address: IP address or hostname of the adapter
    timeout_s: Seconds without VUART data before the capture ends. Default is to never time out.
    endmarker: Stop the capture after this string is found in the VUART stream.
    lineending: Line ending appended to ``command``: ``cr``, ``lf``, ``crlf``, or ``none``. Defaults to ``crlf``.
    command: Command(s) sent to the target immediately after connecting.

  Examples:
    with VuartConsoleStream(ip_address="192.168.1.100", timeout_s=5, endmarker="DONE", command="status") as stream:
      for line in stream:
        print(line, end="", flush=True)
  """
  def __init__(self,
               ip_address: str,
               timeout_s: float | None = None,
               endmarker: str | None = None,
               lineending: str | None = None,
               command: str | list[str] | None = None):

    commander = Commander()

    super().__init__(commander=commander,
                     ip_address=ip_address,
                     timeout_s=timeout_s,
                     endmarker=endmarker,
                     lineending=lineending,
                     command=command)
