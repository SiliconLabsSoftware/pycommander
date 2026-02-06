"""Serial commands: getopn, load, lock, unlock."""

from typing import Any

from pycommander.commands._base import BaseCommand


class SerialCommand(BaseCommand):
  """Serial commands."""

  def _get_general_args(self, **kwargs: Any) -> list[str]:
    args = []
    args += self._get_adapter_connection_args()
    args += self._get_kwargs(**kwargs)
    return args

  def getopn(self, serialport: str = "", **kwargs: Any) -> dict:
    """Get OPN (Ordering Part Number) via serial.

    Args:
      serialport (str): Serial port to use.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if serialport:
      args += ["--serialport", serialport]
    return self._run("serial", "getopn", *args).output

  def load(self, filename: str, fixedspeed: bool = False, serialport: str = "", **kwargs: Any) -> dict:
    """Load image via serial.

    Args:
      filename (str): File to load.
      fixedspeed (bool): Use fixed speed.
      serialport (str): Serial port to use.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if fixedspeed:
      args += ["--fixedspeed"]
    if serialport:
      args += ["--serialport", serialport]
    return self._run("serial", "load", filename, *args).output

  def lock(self, 
           token_file: str = "",
           key_file: str = "",
           userdata: str = "",
           serialport: str = "",
           **kwargs: Any) -> dict:
    """Lock device via serial.

    Args:
      token_file (str): Token file path.
      key_file (str): Key file path.
      userdata (str): User data.
      serialport (str): Serial port to use.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if token_file:
      args += ["--token", token_file]
    if key_file:
      args += ["--key", key_file]
    if userdata:
      args += ["--userdata", userdata]
    if serialport:
      args += ["--serialport", serialport]
    return self._run("serial", "lock", *args).output

  def unlock(self,
             token_file: str = "",
             key_file: str = "",
             userdata: str = "",
             serialport: str = "",
             **kwargs: Any) -> dict:
    """Unlock device via serial.

    Args:
      token_file (str): Token file path.
      key_file (str): Key file path.
      userdata (str): User data.
      serialport (str): Serial port to use.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if token_file:
      args += ["--token", token_file]
    if key_file:
      args += ["--key", key_file]
    if userdata:
      args += ["--userdata", userdata]
    if serialport:
      args += ["--serialport", serialport]
    return self._run("serial", "unlock", *args).output
