"""NVM3 commands: delete, deletedevice, dump, initfile, parse, readdevice, set, writedevice."""

from typing import Any

from pycommander_core.commands._base import BaseCommand


class Nvm3Command(BaseCommand):
  """NVM3 commands (Non-Volatile Memory storage)."""

  def _get_on_device_args(self, **kwargs: Any) -> list[str]:
    args = self._get_offline_args(**kwargs)
    args += self._get_adapter_connection_args()
    args += self._get_debug_args()
    return args

  def _get_offline_args(self, **kwargs: Any) -> list[str]:
    args = []
    args += self._get_kwargs(**kwargs)
    return args

  def delete(self,
             filename: str,
             outfile: str,
             object_keys: list[str] | None = None,
             delete_all: bool = False,
             address: int | None = None,
             range: tuple[int, int] | None = None,
             **kwargs: Any) -> dict:
    """Delete NVM3 objects from file; write result to outfile.

    Args:
      filename (str): Input NVM3 file.
      outfile (str): Output file path after deletion.
      object_keys (list[str]): Object keys to delete.
      delete_all (bool): Delete all objects.
      address (int): NVM3 base address.
      range (tuple[int,int]): NVM3 memory range.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_offline_args(**kwargs)
    if object_keys:
      for k in object_keys:
        args += ["--key", k]
    if delete_all:
      args += ["--all"]
    if address is not None:
      args += ["--address", self._get_address_string(address)]
    if range is not None:
      args += self._get_ranges([range])
    args += ["--outfile", outfile]
    return self._run("nvm3", "delete", filename, *args).output

  def deletedevice(self,
                   object_keys: list[str] | None = None,
                   delete_all: bool = False,
                   range: tuple[int, int] | None = None,
                   **kwargs: Any) -> dict:
    """Delete NVM3 objects on device.

    Args:
      object_keys (list[str]): Object keys to delete.
      delete_all (bool): Delete all objects.
      range (tuple[int,int]): NVM3 memory range on device.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_on_device_args(**kwargs)
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
           range: tuple[int, int] | None = None,
           **kwargs: Any) -> dict:
    """Dump NVM3 contents from device to file.

    Args:
      outfile (str): Output file path.
      range (tuple[int,int]): NVM3 memory range.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_offline_args(**kwargs)
    args += ["--outfile", outfile]
    if range is not None:
      args += self._get_ranges([range])
    return self._run("nvm3", "dump", *args).output

  def initfile(self,
               outfile: str,
               size_bytes: int,
               device: str,
               address: int | None = None,
               range: tuple[int, int] | None = None,
               **kwargs: Any) -> dict:
    """Create an initialized NVM3 file.

    Args:
      outfile (str): Output NVM3 file path.
      size_bytes (int): NVM3 storage size in bytes.
      device (str): Device/device family.
      address (int): Base address.
      range (tuple[int,int]): Memory range.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_offline_args(**kwargs)
    args += ["--outfile", outfile]
    args += ["--size", str(size_bytes)]
    args += ["--device", device]
    if address is not None:
      args += ["--address", self._get_address_string(address)]
    if range is not None:
      args += self._get_ranges([range])
    return self._run("nvm3", "initfile", *args).output

  def parse(self,
            filename: str,
            object_keys: list[str] | None = None,
            nvm3file: str | None = None,
            address: int | None = None,
            range: tuple[int, int] | None = None,
            **kwargs: Any) -> dict:
    """Parse NVM3 file and optionally export objects.

    Args:
      filename (str): Input NVM3 file.
      object_keys (list[str]): Keys to export.
      nvm3file (str): Output NVM3 file for exported data.
      address (int): Base address.
      range (tuple[int,int]): Memory range.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_offline_args(**kwargs)
    if object_keys:
      for k in object_keys:
        args += ["--key", k]
    if nvm3file is not None:
      args += ["--nvm3file", nvm3file]
    if address is not None:
      args += ["--address", self._get_address_string(address)]
    if range is not None:
      args += self._get_ranges([range])
    return self._run("nvm3", "parse", filename, *args).output

  def readdevice(self,
                 object_keys: list[str] | None = None,
                 nvm3file: str | None = None,
                 range: tuple[int, int] | None = None,
                 **kwargs: Any) -> dict:
    """Read NVM3 objects from device.

    Args:
      object_keys (list[str]): Keys to read.
      nvm3file (str): Output file for read data.
      range (tuple[int,int]): NVM3 range on device.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_on_device_args(**kwargs)
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
          nvm3file: str | None = None,
          **kwargs: Any) -> dict:
    """Set NVM3 objects/counters in file; write to outfile.

    Args:
      filename (str): Input NVM3 file.
      outfile (str): Output file path.
      address (int): Base address.
      range (tuple[int,int]): Memory range.
      objects (list[str]): Object key:value entries.
      counters (list[str]): Counter key:value entries.
      nvm3file (str): NVM3 file for object data.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_offline_args(**kwargs)
    args += ["--outfile", outfile]
    if address is not None:
      args += ["--address", self._get_address_string(address)]
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
                  nvm3file: str | None = None,
                  **kwargs: Any) -> dict:
    """Write NVM3 objects/counters to device.

    Args:
      range (tuple[int,int]): NVM3 range on device.
      objects (list[str]): Object key:value entries.
      counters (list[str]): Counter key:value entries.
      nvm3file (str): NVM3 file with data to write.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_on_device_args(**kwargs)
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
