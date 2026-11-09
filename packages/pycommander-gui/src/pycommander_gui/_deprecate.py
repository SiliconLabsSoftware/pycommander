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

import warnings

_warned = False

def warn_deprecated_api() -> None:
  """Warn once that the pycommander_gui Python API is deprecated.

  stacklevel points at the caller of this function, which is either
  pycommander_gui.__getattr__ or a compatibility shim. Python then attributes
  the warning to the script that imported the API.
  """
  global _warned
  if _warned:
    return
  _warned = True
  warnings.warn(
    "Importing the Python API from pycommander_gui is deprecated and will be removed in a future release. "
    "Import from pycommander instead.",
    DeprecationWarning,
    stacklevel=3,
  )
