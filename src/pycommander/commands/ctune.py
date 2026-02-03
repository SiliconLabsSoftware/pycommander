from pycommander.commands._base import BaseCommand

class CtuneCommand(BaseCommand):

  def _get_general_args(self) -> list[str]:
    args = []
    args += self._get_adapter_connection_args()
    args += self._get_device_args()
    args += self._get_debug_args()
    args += self._get_flags()
    return args

  def autoset(self) -> dict:
    return self._run("ctune", "autoset", *self._get_general_args()).output

  def get(self) -> dict:
    return self._run("ctune", "get", *self._get_general_args()).output

  def set(self, value_hex_string: str) -> dict:
    args = self._get_general_args()
    args += ["--value", value_hex_string]
    return self._run("ctune", "set", *args).output
