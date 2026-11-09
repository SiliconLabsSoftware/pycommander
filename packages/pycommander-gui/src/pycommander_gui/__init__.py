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

# The GUI package ships the GUI executable. The Python API lives in the CLI
# package and is imported only when a script asks for it, so launching the GUI
# does not require pycommander_cli to be installed.

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

def __getattr__(name: str):
  if name not in __all__:
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

  from ._deprecate import warn_deprecated_api
  warn_deprecated_api()

  try:
    import pycommander_cli
  except ImportError:
    raise ImportError(
      "The pycommander_cli package is not installed, but is required to use the Python API. Install the pycommander package:\n\n"
      "  pip install silabs-pycommander\n"
    )

  value = getattr(pycommander_cli, name)
  globals()[name] = value
  return value

def __dir__():
  return sorted(set(globals()) | set(__all__))
