"""CTUNE commands: autoset, get, set."""

from typing import Any

from pycommander_core.commands._base import BaseCommand


class CtuneCommand(BaseCommand):
  """CTUNE commands (get/set crystal tuning value)."""

  def _get_general_args(self, **kwargs: Any) -> list[str]:
    args = []
    args += self._get_adapter_connection_args()
    args += self._get_debug_args()
    args += self._get_kwargs(**kwargs)
    return args

  def autoset(self, **kwargs: Any) -> dict:
    """Get CTUNE value from board and set it to the CTUNE token.

    Returns:
      Command output as parsed JSON (dict).
    """
    return self._run("ctune", "autoset", *self._get_general_args(**kwargs)).output

  def get(self, **kwargs: Any) -> dict:
    """Get CTUNE value from DI, board and token.

    Returns:
      Command output as parsed JSON (dict).
    """
    return self._run("ctune", "get", *self._get_general_args(**kwargs)).output

  def set(self, value_hex_string: str, **kwargs: Any) -> dict:
    """Set value to the CTUNE token.

    Args:
      value_hex_string (str): Value to set (hex form, bytes).

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    args += ["--value", value_hex_string]
    return self._run("ctune", "set", *args).output
