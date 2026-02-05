"""GBLv4 commands: create, createconfig, info, parse, sign."""

from pycommander.commands._base import BaseCommand


class Gbl4Command(BaseCommand):
  """GBLv4 commands."""

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
    """Create a GBLv4 file.

    Args:
      outfile (str): Output GBLv4 file path.
      config (str): Config YAML describing GBL (other options ignored if set).
      data (list[str]): Application or bootloader image(s); can be repeated.
      seupgrade (str): Secure Engine upgrade image.
      encrypt_keyfile (str): AES key to encrypt update data (util genkey aes-ccm).
      compress (str): Compression for data: lz4 or lzma.
      certificate (str): Certificate to add.
      sign_keyfile (str): ECC-P256 PEM private key to sign.
      extsign (bool): Output for external signature, then gbl4 sign.
      productid (str): 128-bit product/vendor ID (hex).
      bundleversion (str): Bundle version (smaller rejected).
      minversion (str): Minimum previous version for partial DFU.

    Returns:
      Command output as parsed JSON (dict).
    """
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
    """Create template config YAML file for GBLv4 input.

    Args:
      outfile (str): Output config file path.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args()
    args += ["--outfile", outfile]
    return self._run("gbl4", "createconfig", *args).output

  def info(self, filename: str) -> dict:
    """Parse and show info about a GBLv4 file.

    Args:
      filename (str): Input GBLv4 file.

    Returns:
      Command output as parsed JSON (dict).
    """
    return self._run("gbl4", "info", filename, *self._get_general_args()).output

  def parse(self,
            infile: str,
            seupgrade: str | None = None,
            outfile: str | None = None) -> dict:
    """Parse a GBLv4 file; export updates and/or SE upgrade to files.

    Args:
      infile (str): Input GBLv4 file.
      seupgrade (str): Output filename for SE upgrade image.
      outfile (str): Output for updates (multiple get index suffix, e.g. file_0.s37).

    Returns:
      Command output as parsed JSON (dict).
    """
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
    """Sign a GBLv4 file using external signature (from create --extsign).

    Args:
      infile (str): Input unsigned GBLv4 file (from gbl4 create --extsign).
      signature (str): ECDSA signature of .manifest file in DER format.
      outfile (str): Output signed file path.
      verify_keyfile (str): ECC-P256 PEM public key to verify.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args()
    args += ["--signature", signature]
    args += ["--outfile", outfile]
    if verify_keyfile is not None:
      args += ["--verify", verify_keyfile]
    return self._run("gbl4", "sign", infile, *args).output
