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

from pycommander_core.launcher import CommanderLauncher

class PyCommanderCLI(CommanderLauncher):
  def __init__(self, executable_path: Path | None = None):
    super().__init__(cli=True, executable_path=executable_path)
