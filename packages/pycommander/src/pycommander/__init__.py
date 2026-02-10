try:
  from pycommander_gui import Commander, Adapter, Device
except ImportError:
  from pycommander_cli import Commander, Adapter, Device

__all__ = [
  "Commander",
  "Adapter",
  "Device",
]
