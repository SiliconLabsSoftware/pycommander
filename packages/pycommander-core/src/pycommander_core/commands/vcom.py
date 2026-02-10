"""VCOM commands: configure adapter VCOM settings."""

from typing import Any

from pycommander_core.commands._base import BaseCommand


class VcomCommand(BaseCommand):
  """VCOM commands."""

  def _get_general_args(self, **kwargs: Any) -> list[str]:
    args = []
    args += self._get_adapter_connection_args()
    args += self._get_kwargs(**kwargs)
    return args

  def config(self,
             baudrate: int | None = None,
             handshake: str | None = None,
             store: bool = False,
             **kwargs: Any) -> dict:
    """Configure adapter board VCOM settings.

    Args:
      baudrate (int): VCOM baudrate.
      handshake (str): Handshake: none, rtscts, or aux.
      store (bool): Store adapter board VCOM settings.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if baudrate is not None:
      args += ["--baudrate", str(baudrate)]
    if handshake is not None:
      args += ["--handshake", handshake]
    if store:
      args += ["--store"]
    return self._run("vcom", "config", *args).output
