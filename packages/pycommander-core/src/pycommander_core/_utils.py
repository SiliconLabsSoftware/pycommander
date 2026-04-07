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

def sanitize_args(args: list[str | int | float | None]) -> list[str]:
  # NOTE: We do NOT want to split any args that contain whitespace into multiple args.
  #       There might be filenames or other arguments that have whitespace in them.

  sanitized_args : list[str] = []
  for arg in args:
    # Remove any empty or None elements
    if arg is None:
      continue

    # Stringify any non-string elements
    if not isinstance(arg, str):
      arg = str(arg)

    # Remove any whitespace-only elements
    if arg.strip() == "":
      continue

    # Trim leading and trailing whitespace
    arg = arg.strip()

    sanitized_args.append(arg)

  return sanitized_args
