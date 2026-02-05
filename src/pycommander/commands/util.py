from pycommander.commands._base import BaseCommand

class UtilCommand(BaseCommand):

  def _get_general_args(self) -> list[str]:
    args = []
    args += self._get_device_args()
    args += self._get_flags()
    return args

  def appinfo(self, filename: str) -> dict:
    return self._run("util", "appinfo", filename, *self._get_general_args()).output

  def elfinfo(self, filename: str) -> dict:
    return self._run("util", "elfinfo", filename, *self._get_general_args()).output

  def extractkeys(self, filename: str, dir: str) -> dict:
    args = self._get_general_args()
    args += ["--dir", dir]
    return self._run("util", "extractkeys", filename, *args).output

  def gencert(self,
              outfile: str,
              cert_version: int,
              cert_type: str,
              cert_pubkey: str,
              sign_keyfile: str | None = None,
              extsign: bool = False) -> dict:
    args = self._get_general_args()
    args += ["--outfile", outfile]
    args += ["--cert-version", str(cert_version)]
    args += ["--cert-type", cert_type]
    args += ["--cert-pubkey", cert_pubkey]
    if sign_keyfile is not None:
      args += ["--sign", sign_keyfile]
    if extsign:
      args += ["--extsign"]
    return self._run("util", "gencert", *args).output

  def genkey(self,
             type: str,
             pubkey: str | None = None,
             privkey: str | None = None,
             outfile: str | None = None,
             tokenfile: str | None = None) -> dict:
    args = self._get_general_args()
    args += ["--type", type]
    if pubkey is not None:
      args += ["--pubkey", pubkey]
    if privkey is not None:
      args += ["--privkey", privkey]
    if outfile is not None:
      args += ["--outfile", outfile]
    if tokenfile is not None:
      args += self._get_tokenfiles([tokenfile])
    return self._run("util", "genkey", *args).output

  def genkeyconfig(self, outfile: str) -> dict:
    args = self._get_general_args()
    args += ["--outfile", outfile]
    return self._run("util", "genkeyconfig", *args).output

  def keytotoken(self,
                 keyfile: str,
                 outfile: str | None = None,
                 key_type: str | None = None) -> dict:
    args = [keyfile] + self._get_general_args()
    if outfile is not None:
      args += ["--outfile", outfile]
    if key_type is not None:
      args += ["--type", key_type]
    return self._run("util", "keytotoken", *args).output

  def rpsinfo(self, filename: str) -> dict:
    return self._run("util", "rpsinfo", filename, *self._get_general_args()).output

  def signcert(self,
               filename: str,
               signature: str,
               cert_type: str,
               outfile: str,
               verify_keyfile: str | None = None) -> dict:
    args = self._get_general_args()
    args += ["--signature", signature]
    args += ["--cert-type", cert_type]
    args += ["--outfile", outfile]
    if verify_keyfile is not None:
      args += ["--verify", verify_keyfile]
    return self._run("util", "signcert", filename, *args).output

  def usage(self,
            filename: str,
            map_filename: str | None = None,
            include_sections: list[str] = [],
            exclude_sections: list[str] = []) -> dict:
    args = self._get_general_args()
    if map_filename is not None:
      args += ["--map", map_filename]
    if include_sections:
      args += self._get_include_sections(include_sections)
    if exclude_sections:
      args += self._get_exclude_sections(exclude_sections)
    return self._run("util", "usage", filename, *args).output

  def verifysign(self, filename: str, verify_keyfile: str) -> dict:
    args = self._get_general_args()
    args += ["--verify", verify_keyfile]
    return self._run("util", "verifysign", filename, *args).output
