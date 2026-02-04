from pycommander.commands._base import BaseCommand

class LittlefsCommand(BaseCommand):

  def _get_general_args(self) -> list[str]:
    args = []
    args += self._get_adapter_connection_args()
    args += self._get_device_args()
    args += self._get_debug_args()
    args += self._get_flags()
    return args

  def _add_location_args(self,
                         address: int | None = None,
                         range: tuple[int, int] | None = None,
                         infile: str | None = None) -> list[str]:
    args = []
    if address is not None:
      args += ["--address", self._get_address_string(address)]
    if range is not None:
      args += self._get_ranges([range])
    if infile is not None:
      args += ["--infile", infile]
    return args

  def _get_file_paths(self, file_paths: list[str]) -> list[str]:
    args = []
    for file_path in file_paths:
      args += ["--file", file_path]
    return args

  def _get_dir_paths(self, dir_paths: list[str]) -> list[str]:
    args = []
    for dir_path in dir_paths:
      args += ["--dir", dir_path]
    return args

  def add(self,
          outfile: str,
          file_paths: list[str] = [],
          dir_paths: list[str] = [],
          address: int | None = None,
          range: tuple[int, int] | None = None,
          infile: str | None = None) -> dict:
    args = self._get_general_args()
    args += self._add_location_args(address, range, infile)
    if file_paths:
      args += self._get_file_paths(file_paths)
    if dir_paths:
      args += self._get_dir_paths(dir_paths)
    args += ["--outfile", outfile]
    return self._run("littlefs", "add", *args).output

  def dump(self,
           outfile: str,
           address: int | None = None,
           range: tuple[int, int] | None = None,
           infile: str | None = None) -> dict:
    args = self._get_general_args()
    args += self._add_location_args(address, range, infile)
    args += ["--outfile", outfile]
    return self._run("littlefs", "dump", *args).output

  def extract(self,
              dest_dir: str | None = None,
              zip_dir: str | None = None,
              file_paths: list[str] = [],
              dir_paths: list[str] = [],
              address: int | None = None,
              range: tuple[int, int] | None = None,
              infile: str | None = None) -> dict:
    args = self._get_general_args()
    args += self._add_location_args(address, range, infile)
    if file_paths:
      args += self._get_file_paths(file_paths)
    if dir_paths:
      args += self._get_dir_paths(dir_paths)
    if dest_dir is not None:
      args += ["--dest", dest_dir]
    if zip_dir is not None:
      args += ["--zip", zip_dir]
    return self._run("littlefs", "extract", *args).output

  def info(self,
           address: int | None = None,
           range: tuple[int, int] | None = None,
           infile: str | None = None) -> dict:
    args = self._get_general_args()
    args += self._add_location_args(address, range, infile)
    return self._run("littlefs", "info", *args).output

  def init(self,
           outfile: str,
           device: str,
           size: int | None = None,
           address: int | None = None,
           range: tuple[int, int] | None = None) -> dict:
    # Don't include the device argument from the PyCommander instance here
    args  = self._get_adapter_connection_args()
    args += self._get_debug_args()
    args += self._get_flags()

    if address is not None:
      args += ["--address", self._get_address_string(address)]
    if range is not None:
      args += self._get_ranges([range])
    if size is not None:
      args += ["--size", str(size)]

    args += ["--device", device]
    args += ["--outfile", outfile]
    return self._run("littlefs", "init", *args).output

  def list_files(self,
           address: int | None = None,
           range: tuple[int, int] | None = None,
           infile: str | None = None) -> dict:
    args = self._get_general_args()
    args += self._add_location_args(address, range, infile)
    return self._run("littlefs", "list", *args).output

  def remove(self,
             file_paths: list[str] = [],
             dir_paths: list[str] = [],
             address: int | None = None,
             range: tuple[int, int] | None = None,
             infile: str | None = None) -> dict:
    args = self._get_general_args()
    args += self._add_location_args(address, range, infile)
    if file_paths:
      args += self._get_file_paths(file_paths)
    if dir_paths:
      args += self._get_dir_paths(dir_paths)
    return self._run("littlefs", "remove", *args).output
