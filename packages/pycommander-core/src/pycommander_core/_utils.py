def sanitize_args(args: list[str]) -> list[str]:
  # NOTE: We do NOT want to split any args that contain whitespace into multiple args.
  #       There might be filenames or other arguments that have whitespace in them.

  sanitized_args : list[str] = []
  for arg in args:
    # Remove any empty or None elements
    if not arg:
      continue

    # Remove any whitespace-only elements
    if arg.strip() == "":
      continue

    # Trim leading and trailing whitespace
    sanitized_args.append(arg.strip())

  return sanitized_args
