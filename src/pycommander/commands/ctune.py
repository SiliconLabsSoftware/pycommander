"""CTUNE commands: autoset, get, set."""

from pycommander.commands._base import BaseCommand


class CtuneCommand(BaseCommand):
  """CTUNE commands (get/set crystal tuning value)."""

  def _get_general_args(self) -> list[str]:
    args = []
    args += self._get_adapter_connection_args()
    args += self._get_device_args()
    args += self._get_debug_args()
    args += self._get_flags()
    return args

  def autoset(self) -> dict:
    """Get CTUNE value from board and set it to the CTUNE token.

    Returns:
      Command output as parsed JSON (dict).
    """
    return self._run("ctune", "autoset", *self._get_general_args()).output

  def get(self) -> dict:
    """Get CTUNE value from DI, board and token.

    Returns:
      Command output as parsed JSON (dict).
    """
    return self._run("ctune", "get", *self._get_general_args()).output

  def set(self, value_hex_string: str) -> dict:
    """Set value to the CTUNE token.

    Args:
      value_hex_string (str): Value to set (hex form, bytes).

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args()
    args += ["--value", value_hex_string]
    return self._run("ctune", "set", *args).output
