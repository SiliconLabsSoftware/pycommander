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

from pathlib import Path

from pycommander_core.commander_base import CommanderBase
from pycommander_core.commands._base import BaseCommand

from .mock_runner import MockRunner


class MockCommander(CommanderBase):
  """Commander that uses MockRunner instead of Runner.

  In tests, use commander._runner.logged_commands to inspect the full
  command lines that were "run" (without actually executing them).
  """

  def __init__(
    self,
    serial_number: str | None = None,
    ip_address: str | None = None,
    serial_port: str | None = None,
    target_device: str | None = None,
    debug_speed: int | None = None,
    debug_tif: str | None = None,
    debug_irpre: int | None = None,
    debug_drpre: int | None = None,
    log_file_path: Path | None = None,
    executable_path: Path | None = None,
  ):
    executable_path = executable_path or Path("mock")

    self._runner = MockRunner(
      executable_path,
      log_file_path=log_file_path,
      timeout_s=CommanderBase.default_timeout_s,
    )

    self._serial_number = serial_number
    self._ip_address    = ip_address
    self._serial_port   = serial_port
    self._target_device = target_device
    self._debug_speed   = debug_speed
    self._debug_tif     = debug_tif
    self._debug_irpre   = debug_irpre
    self._debug_drpre   = debug_drpre

    from pycommander_core import commands
    for name in commands.__all__:
      command_class = getattr(commands, name)
      attribute_name = name.removesuffix("Command").lower()
      command = command_class(self)
      command._runner = self._runner
      setattr(self, attribute_name, command)
