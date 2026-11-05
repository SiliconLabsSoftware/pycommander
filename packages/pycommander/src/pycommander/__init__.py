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
  from pycommander_cli import \
    Commander, \
    CommanderResult, \
    Adapter, \
    Target, \
    AemStream, \
    SwoConsoleStream, \
    RttConsoleStream, \
    VcomConsoleStream, \
    VuartConsoleStream, \
    __version__

except ImportError:
  raise ImportError(
    "The pycommander_cli package is not installed, but is required to use the Python API. Install the complete pycommander package:\n\n"
    "  pip install silabs-pycommander\n"
  )

__all__ = [
  "Commander",
  "CommanderResult",
  "Adapter",
  "Target",
  "AemStream",
  "SwoConsoleStream",
  "RttConsoleStream",
  "VcomConsoleStream",
  "VuartConsoleStream",
  "__version__",
]
