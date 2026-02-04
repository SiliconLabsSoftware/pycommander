from pycommander.commands._base import BaseCommand

class VcomCommand(BaseCommand):

  def _get_general_args(self) -> list[str]:
    args = []
    args += self._get_adapter_connection_args()
    args += self._get_device_args()
    args += self._get_flags()
    return args

  def config(self,
             baudrate: int | None = None,
             handshake: str | None = None,
             store: bool = False) -> dict:
    args = self._get_general_args()
    if baudrate is not None:
      args += ["--baudrate", str(baudrate)]
    if handshake is not None:
      args += ["--handshake", handshake]
    if store:
      args += ["--store"]
    return self._run("vcom", "config", *args).output
