from pycommander.commands._base import BaseCommand

class Nvm3Command(BaseCommand):

  def _get_on_device_args(self) -> list[str]:
    args = self._get_offline_args()
    args += self._get_adapter_connection_args()
    args += self._get_debug_args()
    return args

  def _get_offline_args(self) -> list[str]:
    args = []
    args += self._get_flags()
    return args

  def delete(self,
             filename: str,
             outfile: str,
             object_keys: list[str] | None = None,
             delete_all: bool = False,
             address: int | None = None,
             range: tuple[int, int] | None = None) -> dict:
    args = self._get_offline_args()
    if object_keys:
      for k in object_keys:
        args += ["--key", k]
    if delete_all:
      args += ["--all"]
    if address is not None:
      args += ["--address", self._get_address(address)]
    if range is not None:
      args += self._get_ranges([range])
    args += ["--outfile", outfile]
    return self._run("nvm3", "delete", filename, *args).output

  def deletedevice(self,
                   object_keys: list[str] | None = None,
                   delete_all: bool = False,
                   range: tuple[int, int] | None = None) -> dict:
    args = self._get_on_device_args()
    if object_keys:
      for k in object_keys:
        args += ["--key", k]
    if delete_all:
      args += ["--all"]
    if range is not None:
      args += self._get_ranges([range])
    return self._run("nvm3", "deletedevice", *args).output

  def dump(self,
           outfile: str,
           range: tuple[int, int] | None = None) -> dict:
    args = self._get_offline_args()
    args += ["--outfile", outfile]
    if range is not None:
      args += self._get_ranges([range])
    return self._run("nvm3", "dump", *args).output

  def initfile(self,
               outfile: str,
               size_bytes: int,
               device: str,
               address: int | None = None,
               range: tuple[int, int] | None = None) -> dict:
    args = self._get_offline_args() 
    args += ["--outfile", outfile]
    args += ["--size", str(size_bytes)]
    args += ["--device", device]
    if address is not None:
      args += ["--address", self._get_address(address)]
    if range is not None:
      args += self._get_ranges([range])
    return self._run("nvm3", "initfile", *args).output

  def parse(self,
            filename: str,
            object_keys: list[str] | None = None,
            nvm3file: str | None = None,
            address: int | None = None,
            range: tuple[int, int] | None = None) -> dict:
    args = self._get_offline_args()
    if object_keys:
      for k in object_keys:
        args += ["--key", k]
    if nvm3file is not None:
      args += ["--nvm3file", nvm3file]
    if address is not None:
      args += ["--address", self._get_address(address)]
    if range is not None:
      args += self._get_ranges([range])
    return self._run("nvm3", "parse", filename, *args).output

  def readdevice(self,
                 object_keys: list[str] | None = None,
                 nvm3file: str | None = None,
                 range: tuple[int, int] | None = None) -> dict:
    args = self._get_on_device_args()
    if object_keys:
      for k in object_keys:
        args += ["--key", k]
    if nvm3file is not None:
      args += ["--nvm3file", nvm3file]
    if range is not None:
      args += self._get_ranges([range])
    return self._run("nvm3", "readdevice", *args).output

  def set(self,
          filename: str,
          outfile: str,
          address: int | None = None,
          range: tuple[int, int] | None = None,
          objects: list[str] | None = None,
          counters: list[str] | None = None,
          nvm3file: str | None = None) -> dict:
    args = self._get_offline_args()
    args += ["--outfile", outfile]
    if address is not None:
      args += ["--address", self._get_address(address)]
    if range is not None:
      args += self._get_ranges([range])
    if objects:
      for o in objects:
        args += ["--object", o]
    if counters:
      for c in counters:
        args += ["--counter", c]
    if nvm3file is not None:
      args += ["--nvm3file", nvm3file]
    return self._run("nvm3", "set", filename, *args).output

  def writedevice(self,
                  range: tuple[int, int] | None = None,
                  objects: list[str] | None = None,
                  counters: list[str] | None = None,
                  nvm3file: str | None = None) -> dict:
    args = self._get_on_device_args()
    if range is not None:
      args += self._get_ranges([range])
    if objects:
      for o in objects:
        args += ["--object", o]
    if counters:
      for c in counters:
        args += ["--counter", c]
    if nvm3file is not None:
      args += ["--nvm3file", nvm3file]
    return self._run("nvm3", "writedevice", *args).output
