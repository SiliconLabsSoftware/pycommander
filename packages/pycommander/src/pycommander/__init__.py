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

try:
  from pycommander_gui import Commander, CommanderResult, Adapter, Target, AemStream, __version__
except ImportError:
  try:
    from pycommander_cli import Commander, CommanderResult, Adapter, Target, AemStream, __version__
  except ImportError:
    raise ImportError(
      "No version of Simplicity Commander is installed. Install one of the following packages:\n\n"
      "  pip install silabs-pycommander-cli\n"
      "  pip install silabs-pycommander-gui\n"
    )

__all__ = [
  "Commander",
  "CommanderResult",
  "Adapter",
  "Target",
  "AemStream",
  "__version__",
]
