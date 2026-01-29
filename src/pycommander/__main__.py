"""
License
Copyright 2025 Silicon Laboratories Inc. www.silabs.com
*******************************************************************************
The licensor of this software is Silicon Laboratories Inc. Your use of this
software is governed by the terms of Silicon Labs Master Software License
Agreement (MSLA) available at
www.silabs.com/about-us/legal/master-software-license-agreement. This
software is distributed to you in Source Code format and is governed by the
sections of the MSLA applicable to Source Code.
*******************************************************************************
"""

# Entry point for `pycommander` command and `python3 -m pycommander`

import sys

from ._ensure_commander import ensure_commander
from .cli import main

if __name__ == "__main__":
    if not ensure_commander():
        sys.exit(1)

    sys.exit(main())
