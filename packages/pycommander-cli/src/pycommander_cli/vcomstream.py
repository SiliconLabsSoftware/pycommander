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

from pycommander_core.vcomstream_base import VcomStreamBase

from pycommander_cli.commander import Commander

class VcomStream(VcomStreamBase):
  """
  High-level read-only interface for VCOM (Virtual COM port) captures.
  This class can be used in a context manager to simplify the handling
  of opening and closing the VcomStream. The stream works with Silicon
  Labs adapters that expose a serial VCOM port.

  Startup commands can be sent once after connect via ``command``. The stream
  itself does not accept further input. Adapter VCOM baudrate and handshake
  are configured separately (for example via ``Commander.vcom.config``).

  Args:
    serial_number: Serial number of the adapter
    ip_address: IP address of the adapter
    hex_output: If True, yield hexadecimal strings.
    restartinisp: If True, restart the target in ISP mode upon connecting. Only supported on select SiWx91x boards.
    lineending: Line ending appended to ``command``: ``cr``, ``lf``, ``crlf``, or ``none``. Defaults to ``crlf``. Ignored if ``hex_output`` is True.
    command: Command(s) sent to the target immediately after connecting.

  Examples:
    with VcomStream(serial_number="123456789", command="status") as stream:
      for line in stream:
        print(line, end="", flush=True)
  """
  def __init__(self,
               serial_number: str | None = None,
               ip_address: str | None = None,
               hex_output: bool = False,
               restartinisp: bool = False,
               lineending: str | None = None,
               command: str | list[str] | None = None):

    commander = Commander(serial_number=serial_number,
                          ip_address=ip_address)

    super().__init__(commander=commander,
                     hex_output=hex_output,
                     restartinisp=restartinisp,
                     lineending=lineending,
                     command=command)
