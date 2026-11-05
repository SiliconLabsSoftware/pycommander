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

from pycommander_cli.launcher import PyCommanderCLI

try:
  from pycommander_gui.launcher import PyCommanderGUI
  GUI = True
except ImportError:
  GUI = False


def main() -> int:
  args = sys.argv[1:]  # Skip the script name

  # Launch the GUI executable only if we need the GUI explicitly
  if GUI and (len(args) == 0 or args[0] == "gui"):
    return PyCommanderGUI().run(*args)
  else:
    return PyCommanderCLI().run(*args)

if __name__ == "__main__":
  raise SystemExit(main())
