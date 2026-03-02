"""RPS commands: create, convert, load, sign."""

from typing import Any

from pycommander_core.commands._base import BaseCommand


class RpsCommand(BaseCommand):
  """Generate RPS files."""

  def _get_general_args(self, **kwargs: Any) -> list[str]:
    args = []
    args += self._get_kwargs(**kwargs)
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
             prev_key: str | None = None,
             **kwargs: Any) -> dict:
    """Create RPS file.

    Args:
      outfile (str): Output RPS file path.
      encrypt_key (str): Encryption key file.
      mic_key (str): MIC key file.
      iv_file (str): IV file.
      sign_keyfile (str): Signing key file.
      sha (str): SHA option.
      extsign (bool): Output for external signing.
      address (int): Flash address.
      app (str): Application image.
      app_version (int): Application version.
      fw_info (int): Firmware info.
      include_sections (list[str]): ELF sections to include.
      exclude_sections (list[str]): ELF sections to exclude.
      map_file (str): Map file path.
      combinedimage (bool): Combined image flag.
      key_type (str): Key type.
      new_key (str): New key.
      prev_key (str): Previous key.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if encrypt_key:
      args += ["--encrypt", encrypt_key]
    if mic_key:
      args += ["--mic", mic_key]
    if iv_file:
      args += ["--iv", iv_file]
    if sign_keyfile:
      args += ["--sign", sign_keyfile]
    if sha:
      args += ["--sha", sha]
    if extsign:
      args += ["--extsign"]
    if address is not None:
      args += ["--address", self._get_address_string(address)]
    if app:
      args += ["--app", app]
    if app_version is not None:
      args += ["--app-version", str(app_version)]
    if fw_info is not None:
      args += ["--fw-info", str(fw_info)]
    if include_sections:
      args += self._get_include_sections(include_sections)
    if exclude_sections:
      args += self._get_exclude_sections(exclude_sections)
    if map_file:
      args += ["--map", map_file]
    if combinedimage:
      args += ["--combinedimage"]
    if key_type:
      args += ["--key-type", key_type]
    if new_key:
      args += ["--new-key", new_key]
    if prev_key:
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
              combinedimage: bool = False,
              **kwargs: Any) -> dict:
    """Convert to RPS file.

    Args:
      outfile (str): Output file path.
      encrypt_key (str): Encryption key.
      mic_key (str): MIC key.
      iv_file (str): IV file.
      sign_keyfile (str): Signing key file.
      sha (str): SHA option.
      extsign (bool): External signing.
      app (str): Application image.
      nwpapp (str): NWP application image.
      app_version (int): Application version.
      fw_info (int): Firmware info.
      combinedimage (bool): Combined image.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if encrypt_key:
      args += ["--encrypt", encrypt_key]
    if mic_key:
      args += ["--mic", mic_key]
    if iv_file:
      args += ["--iv", iv_file]
    if sign_keyfile:
      args += ["--sign", sign_keyfile]
    if sha:
      args += ["--sha", sha]
    if extsign:
      args += ["--extsign"]
    if app:
      args += ["--app", app]
    if nwpapp:
      args += ["--nwpapp", nwpapp]
    if app_version is not None:
      args += ["--app-version", str(app_version)]
    if fw_info is not None:
      args += ["--fw-info", str(fw_info)]
    if combinedimage:
      args += ["--combinedimage"]
    return self._run("rps", "convert", outfile, *args).output

  def load(self, filename: str, eraseapp: bool = False, **kwargs: Any) -> dict:
    """Load RPS file to device.

    Args:
      filename (str): RPS file to load.
      eraseapp (bool): Erase application before load.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs) + self._get_adapter_connection_args()
    if eraseapp:
      args += ["--eraseapp"]
    return self._run("rps", "load", filename, *args).output

  def sign(self,
           filename: str,
           signature: str,
           outfile: str | None = None,
           **kwargs: Any) -> dict:
    """Sign RPS file with external signature.

    Args:
      filename (str): Input RPS file.
      signature (str): Signature file.
      outfile (str): Output signed file path.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = [filename, "--signature", signature] + self._get_general_args(**kwargs)
    if outfile:
      args += ["--outfile", outfile]
    return self._run("rps", "sign", *args).output
