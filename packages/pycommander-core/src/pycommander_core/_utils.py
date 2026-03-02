def sanitize_args(args: list[str]) -> list[str]:
  sanitized_args : list[str] = []
  for arg in args:
    # Strip away any empty or None elements
    if not arg:
      continue

    sanitized_args.append(arg)
  return sanitized_args
