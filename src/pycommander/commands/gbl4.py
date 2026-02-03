from pycommander.commands._base import BaseCommand

class Gbl4Command(BaseCommand):

  def _get_general_args(self) -> list[str]:
    args = []
    args += self._get_device_args()
    args += self._get_flags()
    return args

  def create(self,
             outfile: str,
             config: str | None = None,
             data: list[str] = [],
             seupgrade: str | None = None,
             encrypt_keyfile: str | None = None,
             compress: str | None = None,
             certificate: str | None = None,
             sign_keyfile: str | None = None,
             extsign: bool = False,
             productid: str | None = None,
             bundleversion: str | None = None,
             minversion: str | None = None) -> dict:
    args = self._get_general_args()
    if config is not None:
      args += ["--config", config]
    if data:
      for d in data:
        args += ["--data", d]
    if seupgrade is not None:
      args += ["--seupgrade", seupgrade]
    if encrypt_keyfile is not None:
      args += ["--encrypt", encrypt_keyfile]
    if compress is not None:
      args += ["--compress", compress]
    if certificate is not None:
      args += ["--certificate", certificate]
    if sign_keyfile is not None:
      args += ["--sign", sign_keyfile]
    if extsign:
      args += ["--extsign"]
    if productid is not None:
      args += ["--productid", productid]
    if bundleversion is not None:
      args += ["--bundleversion", bundleversion]
    if minversion is not None:
      args += ["--minversion", minversion]
    return self._run("gbl4", "create", outfile, *args).output

  def createconfig(self, outfile: str) -> dict:
    args = self._get_general_args()
    args += ["--outfile", outfile]
    return self._run("gbl4", "createconfig", *args).output

  def info(self, filename: str) -> dict:
    return self._run("gbl4", "info", filename, *self._get_general_args()).output

  def parse(self,
            infile: str,
            seupgrade: str | None = None,
            outfile: str | None = None) -> dict:
    args = self._get_general_args()
    if seupgrade is not None:
      args += ["--seupgrade", seupgrade]
    if outfile is not None:
      args += ["--outfile", outfile]
    return self._run("gbl4", "parse", infile, *args).output

  def sign(self,
           infile: str,
           signature: str,
           outfile: str,
           verify_keyfile: str | None = None) -> dict:
    args = self._get_general_args()
    args += ["--signature", signature]
    args += ["--outfile", outfile]
    if verify_keyfile is not None:
      args += ["--verify", verify_keyfile]
    return self._run("gbl4", "sign", infile, *args).output
