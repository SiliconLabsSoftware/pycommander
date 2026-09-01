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

from pycommander_core.swostream_base import SwoStreamBase

from pycommander_cli.commander import Commander

class SwoStream(SwoStreamBase):
  """
  High-level interface for continuous SWO (Serial Wire Output) captures.
  This class can be used in a context manager to simplify the handling
  of opening and closing the SwoStream. The stream works with any adapter
  that exposes a debug connection (Silicon Labs adapters and generic J-Link).

  Args:
    serial_number: Serial number of the adapter
    ip_address: IP address of the adapter
    target_device: Target device part number
    swospeed_hz: SWO speed in Hz. Must match the target application. Defaults to 875000.
    timeout_s: Seconds without SWO data before the capture ends. Default is to never time out.
    endmarker: Stop the capture after this string is found in the SWO stream.
    hex_output: If True, yield hexadecimal strings. ``endmarker`` must then also be hex-encoded.
    noreset: If True, do not reset the target when the SWO connection is opened.
    channel: SWO channel to read from (0-31). Defaults to 0.
    monitorall: If True, watch all channels for the end marker and timeout. Has no effect unless ``endmarker`` or ``timeout_s`` is set.

  Examples:
    with SwoStream(serial_number="123456789", timeout_s=5, endmarker="DONE") as stream:
      for line in stream:
        print(line, end="", flush=True)
  """
  def __init__(self,
               serial_number: str | None = None,
               ip_address: str | None = None,
               target_device: str | None = None,
               swospeed_hz: int | None = None,
               timeout_s: float | None = None,
               endmarker: str | None = None,
               hex_output: bool = False,
               noreset: bool = False,
               channel: int | None = None,
               monitorall: bool = False):

    commander = Commander(serial_number=serial_number,
                          ip_address=ip_address,
                          target_device=target_device)

    super().__init__(commander=commander,
                     swospeed_hz=swospeed_hz,
                     timeout_s=timeout_s,
                     endmarker=endmarker,
                     hex_output=hex_output,
                     noreset=noreset,
                     channel=channel,
                     monitorall=monitorall)
