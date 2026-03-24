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
