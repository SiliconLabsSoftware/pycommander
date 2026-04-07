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

import sys

from pathlib import Path

if sys.platform == "win32":
  EXECUTABLE_PATH_CLI = Path("Simplicity Commander CLI") / "commander-cli.exe"
  EXECUTABLE_PATH_GUI = Path("Simplicity Commander")     / "commander.exe"
elif sys.platform == "darwin":
  EXECUTABLE_PATH_CLI = Path("Commander-cli.app") / "Contents" / "MacOS" / "commander-cli"
  EXECUTABLE_PATH_GUI = Path("Commander.app")     / "Contents" / "MacOS" / "commander"
elif sys.platform == "linux":
  EXECUTABLE_PATH_CLI = Path("commander-cli") / "commander-cli"
  EXECUTABLE_PATH_GUI = Path("commander")     / "commander"
else:
  raise ValueError(f"Unsupported platform: {sys.platform}")
