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

import subprocess

from .commander_base import CommanderBase
from .runner import Runner
from .types import AemMeasurement

class AemStreamBase:
  def __init__(self,
               commander: CommanderBase,
               datarate_hz: int | None = None,
               duration_s: float | None = None,
               triggerabove_ma: float | None = None,
               triggerbelow_ma: float | None = None,
               triggertimeout_s: float | None = None,
               pretrigger_ms: int | None = None,
               calibrate: bool = False):

    self._commander : CommanderBase = commander
    self._runner : Runner = self._commander._runner
    self._process : subprocess.Popen | None = None

    self._args : list[str] = [
      "aem", "dump"
    ]

    self._args += self._commander._get_serial_number_option()
    self._args += self._commander._get_ip_address_option()
    self._args += self._commander._get_serial_port_option()

    if datarate_hz:
      self._args += ["--datarate", str(datarate_hz)]
    if duration_s:
      self._args += ["--duration", str(duration_s)]
    if triggerabove_ma is not None:
      self._args += ["--triggerabove", str(triggerabove_ma)]
    if triggerbelow_ma is not None:
      self._args += ["--triggerbelow", str(triggerbelow_ma)]
    if triggertimeout_s:
      self._args += ["--triggertimeout", str(triggertimeout_s)]
    if pretrigger_ms:
      self._args += ["--pretrigger", str(pretrigger_ms)]
    if calibrate:
      self._args += ["--calibrate"]

  def open(self) -> None:
    """
    Open the AemStream. This will start the underlying AEM data capture process.
    """
    if not self._process:
      self._process : subprocess.Popen = self._runner.open(*self._args)
    else:
      raise RuntimeError("AemStream was already opened. Call close() first, or, ideally, use the context manager syntax.")

  def close(self) -> None:
    """
    Close the AemStream. This will gracefully stop the underlying AEM data capture process.
    """
    if self._process:
      self._runner.close(self._process)
      self._process = None

  def __parse_line(self, line: str) -> AemMeasurement:
    parts = line.split(",")
    if len(parts) != 3:
      raise ValueError(f"Invalid line: {line}")
    timestamp_us = int(parts[0])
    current_ma = float(parts[1])
    voltage_v = float(parts[2])
    power_mw = current_ma * voltage_v
    return AemMeasurement(timestamp_us=timestamp_us, current_ma=current_ma, voltage_v=voltage_v, power_mw=power_mw)

  def __iter__(self):
    return self

  def __next__(self) -> AemMeasurement:
    if not self._process:
      raise RuntimeError("AemStream not open. Call open() first, or, ideally, use the context manager syntax.")

    while True:
      line = self._process.stdout.readline()
      if not line:
        if self._runner.isAlive(self._process):
          # Wait for more data
          continue
        else:
          # We're done
          raise StopIteration
      try:
        return self.__parse_line(line)
      except:
        # No bother
        continue

  def __enter__(self):
    self.open()
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    self.close()
