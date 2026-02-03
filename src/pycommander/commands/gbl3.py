from pycommander.commands._base import BaseCommand

class Gbl3Command(BaseCommand):

  def _get_general_args(self) -> list[str]:
    args = []
    args += self._get_device_args()
    args += self._get_flags()
    return args

  def aat_usageinfo(self) -> dict:
    return self._run("gbl3", "aat-usageinfo", *self._get_general_args()).output

  def create(self,
             outfile: str,
             app: str | None = None,
             bootloader: str | None = None,
             seupgrade: str | None = None,
             metadata: str | None = None,
             compress: str | None = None,
             certificate: str | None = None,
             include_sections: list[str] = [],
             exclude_sections: list[str] = [],
             seunencrypted: bool = False,
             dep_app: str | None = None,
             dep_boot: str | None = None,
             dep_se: str | None = None,
             delta_app: str | None = None,
             sign_keyfile: str | None = None,
             encrypt_keyfile: str | None = None,
             extsign: bool = False,
             signature: str | None = None,
             verify_keyfile: str | None = None) -> dict:
    args = self._get_general_args()
    if app is not None:
      args += ["--app", app]
    if bootloader is not None:
      args += ["--bootloader", bootloader]
    if seupgrade is not None:
      args += ["--seupgrade", seupgrade]
    if metadata is not None:
      args += ["--metadata", metadata]
    if compress is not None:
      args += ["--compress", compress]
    if certificate is not None:
      args += ["--certificate", certificate]
    if include_sections:
      args += self._get_include_sections(include_sections)
    if exclude_sections:
      args += self._get_exclude_sections(exclude_sections)
    if seunencrypted:
      args += ["--seunencrypted"]
    if dep_app is not None:
      args += ["--dep-app", dep_app]
    if dep_boot is not None:
      args += ["--dep-boot", dep_boot]
    if dep_se is not None:
      args += ["--dep-se", dep_se]
    if delta_app is not None:
      args += ["--delta-app", delta_app]
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
    return self._run("gbl3", "create", outfile, *args).output

  def keyconvert(self,
                 infile: str,
                 type: str | None = None,
                 outfile: str | None = None) -> dict:
    args = self._get_general_args()
    if type is not None:
      args += ["--type", type]
    if outfile is not None:
      args += ["--outfile", outfile]
    return self._run("gbl3", "keyconvert", infile, *args).output

  def keygen(self,
             type: str,
             outfile: str | None = None) -> dict:
    args = ["--type", type] + self._get_general_args()
    if outfile is not None:
      args += ["--outfile", outfile]
    return self._run("gbl3", "keygen", *args).output

  def parse(self,
            infile: str,
            app: str | None = None,
            bootloader: str | None = None,
            seupgrade: str | None = None,
            metadata: str | None = None,
            verify_keyfile: str | None = None,
            decrypt_keyfile: str | None = None) -> dict:
    args = self._get_general_args()
    if app is not None:
      args += ["--app", app]
    if bootloader is not None:
      args += ["--bootloader", bootloader]
    if seupgrade is not None:
      args += ["--seupgrade", seupgrade]
    if metadata is not None:
      args += ["--metadata", metadata]
    if verify_keyfile is not None:
      args += ["--verify", verify_keyfile]
    if decrypt_keyfile is not None:
      args += ["--decrypt", decrypt_keyfile]
    return self._run("gbl3", "parse", infile, *args).output

  def sign(self,
           infile: str,
           outfile: str,
           signature: str,
           verify_keyfile: str | None = None) -> dict:
    args = self._get_general_args()
    args += ["--outfile", outfile]
    args += ["--signature", signature]
    if verify_keyfile is not None:
      args += ["--verify", verify_keyfile]
    return self._run("gbl3", "sign", infile, *args).output
