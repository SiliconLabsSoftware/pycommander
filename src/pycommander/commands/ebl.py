from pycommander.commands._base import BaseCommand

class EblCommand(BaseCommand):

  def _get_general_args(self) -> list[str]:
    args = []
    args += self._get_device_args()
    args += self._get_flags()
    return args

  def aat_usageinfo(self) -> dict:
    return self._run("ebl", "aat-usageinfo", *self._get_general_args()).output

  def create(self,
             outfile: str,
             app: str | None = None,
             sign_keyfile: str | None = None,
             encrypt_keyfile: str | None = None,
             extsign: bool = False,
             signature: str | None = None,
             verify_keyfile: str | None = None) -> dict:
    args = self._get_general_args()
    if app is not None:
      args += ["--app", app]
    if sign_keyfile is not None:
      args += ["--sign", sign_keyfile]
    if encrypt_keyfile is not None:
      args += ["--encrypt", encrypt_keyfile]
    if extsign:
      args += ["--extsign"]
    if signature is not None:
      args += ["--signature", signature]
    if verify_keyfile is not None:
      args += ["--verify", verify_keyfile]
    return self._run("ebl", "create", outfile, *args).output

  def keyconvert(self,
                 infile: str,
                 type: str | None = None,
                 outfile: str | None = None) -> dict:
    args = self._get_general_args()
    if type is not None:
      args += ["--type", type]
    if outfile is not None:
      args += ["--outfile", outfile]
    return self._run("ebl", "keyconvert", infile, *args).output

  def keygen(self,
             type: str,
             outfile: str | None = None) -> dict:
    args = ["--type", type] + self._get_general_args()
    if outfile is not None:
      args += ["--outfile", outfile]
    return self._run("ebl", "keygen", *args).output

  def parse(self,
            infile: str,
            app: str | None = None,
            verify_keyfile: str | None = None,
            decrypt_keyfile: str | None = None) -> dict:
    args = self._get_general_args()
    if app is not None:
      args += ["--app", app]
    if verify_keyfile is not None:
      args += ["--verify", verify_keyfile]
    if decrypt_keyfile is not None:
      args += ["--decrypt", decrypt_keyfile]
    return self._run("ebl", "parse", infile, *args).output

  def print(self, filename: str) -> dict:
    """Print information about an EBL file. Named print_info to avoid shadowing built-in print."""
    return self._run("ebl", "print", filename, *self._get_general_args()).output
