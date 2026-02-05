from pycommander.commands._base import BaseCommand

class RpsCommand(BaseCommand):

  def _get_general_args(self) -> list[str]:
    args = []
    args += self._get_device_args()
    args += self._get_flags()
    return args

  def create(self,
             outfile: str,
             encrypt_key: str | None = None,
             mic_key: str | None = None,
             iv_file: str | None = None,
             sign_keyfile: str | None = None,
             sha: str | None = None,
             extsign: bool = False,
             address: int | None = None,
             app: str | None = None,
             app_version: int | None = None,
             fw_info: int | None = None,
             include_sections: list[str] = [],
             exclude_sections: list[str] = [],
             map_file: str | None = None,
             combinedimage: bool = False,
             key_type: str | None = None,
             new_key: str | None = None,
             prev_key: str | None = None) -> dict:
    args = self._get_general_args()
    if encrypt_key is not None:
      args += ["--encrypt", encrypt_key]
    if mic_key is not None:
      args += ["--mic", mic_key]
    if iv_file is not None:
      args += ["--iv", iv_file]
    if sign_keyfile is not None:
      args += ["--sign", sign_keyfile]
    if sha is not None:
      args += ["--sha", sha]
    if extsign:
      args += ["--extsign"]
    if address is not None:
      args += ["--address", self._get_address_string(address)]
    if app is not None:
      args += ["--app", app]
    if app_version is not None:
      args += ["--app-version", str(app_version)]
    if fw_info is not None:
      args += ["--fw-info", str(fw_info)]
    if include_sections:
      args += self._get_include_sections(include_sections)
    if exclude_sections:
      args += self._get_exclude_sections(exclude_sections)
    if map_file is not None:
      args += ["--map", map_file]
    if combinedimage:
      args += ["--combinedimage"]
    if key_type is not None:
      args += ["--key-type", key_type]
    if new_key is not None:
      args += ["--new-key", new_key]
    if prev_key is not None:
      args += ["--prev-key", prev_key]
    return self._run("rps", "create", outfile, *args).output

  def convert(self,
              outfile: str,
              encrypt_key: str | None = None,
              mic_key: str | None = None,
              iv_file: str | None = None,
              sign_keyfile: str | None = None,
              sha: str | None = None,
              extsign: bool = False,
              app: str | None = None,
              nwpapp: str | None = None,
              app_version: int | None = None,
              fw_info: int | None = None,
              combinedimage: bool = False) -> dict:
    args = self._get_general_args()
    if encrypt_key is not None:
      args += ["--encrypt", encrypt_key]
    if mic_key is not None:
      args += ["--mic", mic_key]
    if iv_file is not None:
      args += ["--iv", iv_file]
    if sign_keyfile is not None:
      args += ["--sign", sign_keyfile]
    if sha is not None:
      args += ["--sha", sha]
    if extsign:
      args += ["--extsign"]
    if app is not None:
      args += ["--app", app]
    if nwpapp is not None:
      args += ["--nwpapp", nwpapp]
    if app_version is not None:
      args += ["--app-version", str(app_version)]
    if fw_info is not None:
      args += ["--fw-info", str(fw_info)]
    if combinedimage:
      args += ["--combinedimage"]
    return self._run("rps", "convert", outfile, *args).output

  def load(self, filename: str, eraseapp: bool = False) -> dict:
    args = self._get_general_args() + self._get_adapter_connection_args()
    if eraseapp:
      args += ["--eraseapp"]
    return self._run("rps", "load", filename, *args).output

  def sign(self,
           filename: str,
           signature: str,
           outfile: str | None = None) -> dict:
    args = [filename, "--signature", signature] + self._get_general_args()
    if outfile is not None:
      args += ["--outfile", outfile]
    return self._run("rps", "sign", *args).output
