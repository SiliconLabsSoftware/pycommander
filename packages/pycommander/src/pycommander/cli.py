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

from pycommander_core.cli import PyCommanderCLI

try:
  from pycommander_gui import Commander
  CLI = False

except ImportError:
  try:
    from pycommander_cli import Commander
    CLI = True

  except ImportError:
    raise ImportError(
      "No version of Simplicity Commander is installed.\n\n"
      "Install either of the following packages:\n"
      "  pip install silabs-pycommander-cli\n"
      "  pip install silabs-pycommander-gui\n"
    )

def main() -> int:
  cli = PyCommanderCLI(cli=CLI)
  args = sys.argv[1:]  # Skip the script name
  return cli.run(*args)

if __name__ == "__main__":
  raise SystemExit(main())
