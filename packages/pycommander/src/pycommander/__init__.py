try:
  from pycommander_gui import Commander, Adapter, Device, __version__
except ImportError:
  try:
    from pycommander_cli import Commander, Adapter, Device, __version__
  except ImportError:
    raise ImportError(
      "No version of Simplicity Commander is installed.\n\n"
      "Install one of:\n"
      "  pip install silabs-pycommander[cli]\n"
      "  pip install silabs-pycommander[gui]\n"
    )

__all__ = [
  "Commander",
  "Adapter",
  "Device",
  "__version__",
]
