from pycommander.commands._base import BaseCommand

class SerialCommand(BaseCommand):

  def _get_general_args(self) -> list[str]:
    args = []
    args += self._get_adapter_connection_args()
    args += self._get_device_args()
    args += self._get_flags()
    return args

  def getopn(self, serialport: str = "") -> dict:
    args = self._get_general_args()
    if serialport:
      args += ["--serialport", serialport]
    return self._run("serial", "getopn", *args).output

  def load(self, filename: str, fixedspeed: bool = False, serialport: str = "") -> dict:
    args = self._get_general_args()
    if fixedspeed:
      args += ["--fixedspeed"]
    if serialport:
      args += ["--serialport", serialport]
    return self._run("serial", "load", filename, *args).output

  def lock(self, 
           token_file: str = "",
           key_file: str = "",
           userdata: str = "",
           serialport: str = "") -> dict:
    args = self._get_general_args()
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
             serialport: str = "") -> dict:
    args = self._get_general_args()
    if token_file:
      args += ["--token", token_file]
    if key_file:
      args += ["--key", key_file]
    if userdata:
      args += ["--userdata", userdata]
    if serialport:
      args += ["--serialport", serialport]
    return self._run("serial", "unlock", *args).output
