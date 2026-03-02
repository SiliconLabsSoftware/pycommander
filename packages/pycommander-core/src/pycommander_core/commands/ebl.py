"""EBL commands: create, parse, print, keygen, keyconvert, aat-usageinfo."""

from typing import Any

from pycommander_core.commands._base import BaseCommand


class EblCommand(BaseCommand):
  """Create, parse and other handling for EBL files."""

  def _get_general_args(self, **kwargs: Any) -> list[str]:
    args = []
    args += self._get_kwargs(**kwargs)
    return args

  def aat_usageinfo(self, **kwargs: Any) -> dict:
    """Display flash and RAM usage from AAT data (Zigbee/Thread; RAM for EM3xx only).

    Returns:
      Command output as parsed JSON (dict).
    """
    return self._run("ebl", "aat-usageinfo", *self._get_general_args(**kwargs)).output

  def create(self,
             outfile: str,
             app: str | None = None,
             sign_keyfile: str | None = None,
             encrypt_keyfile: str | None = None,
             extsign: bool = False,
             signature: str | None = None,
             verify_keyfile: str | None = None,
             **kwargs: Any) -> dict:
    """Create an EBL file.

    Args:
      outfile (str): Output EBL file path.
      app (str): Application image to use when generating EBL.
      sign_keyfile (str): ECC-P256 PEM private key to sign the EBL.
      encrypt_keyfile (str): AES key file to encrypt the EBL (e.g. ebl keygen --type aes-ccm).
      extsign (bool): Generate .extsign file for external signature, insert later with --signature.
      signature (str): DER ECDSA signature file for signing (e.g. with extsign).
      verify_keyfile (str): ECC-P256 PEM public key to verify signed EBL.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if app:
      args += ["--app", app]
    if sign_keyfile:
      args += ["--sign", sign_keyfile]
    if encrypt_keyfile:
      args += ["--encrypt", encrypt_keyfile]
    if extsign:
      args += ["--extsign"]
    if signature:
      args += ["--signature", signature]
    if verify_keyfile:
      args += ["--verify", verify_keyfile]
    return self._run("ebl", "create", outfile, *args).output

  def keyconvert(self,
                 infile: str,
                 type: str | None = None,
                 outfile: str | None = None,
                 **kwargs: Any) -> dict:
    """Convert PEM public key to token file for flashing. Deprecated: use util keytotoken.

    Args:
      infile (str): Input PEM public key file.
      type (str): Crypto algorithm: aes-ccm or ecc-p256.
      outfile (str): Output file path.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if type:
      args += ["--type", type]
    if outfile:
      args += ["--outfile", outfile]
    return self._run("ebl", "keyconvert", infile, *args).output

  def keygen(self,
             type: str,
             outfile: str | None = None,
             **kwargs: Any) -> dict:
    """Generate key for encrypt/decrypt or key pair for signing. Deprecated: use util genkey.

    Args:
      type (str): Algorithm: aes-ccm (encrypt/decrypt) or ecc-p256 (signing, Secure Boot).
      outfile (str): Output file path.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    args += ["--type", type]
    if outfile:
      args += ["--outfile", outfile]
    return self._run("ebl", "keygen", *args).output

  def parse(self,
            infile: str,
            app: str | None = None,
            verify_keyfile: str | None = None,
            decrypt_keyfile: str | None = None,
            **kwargs: Any) -> dict:
    """Parse an EBL file.

    Args:
      infile (str): Input EBL file.
      app (str): File to write the application image to.
      verify_keyfile (str): ECC-P256 PEM public key to verify signed EBL.
      decrypt_keyfile (str): AES key file to decrypt the EBL.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if app:
      args += ["--app", app]
    if verify_keyfile:
      args += ["--verify", verify_keyfile]
    if decrypt_keyfile:
      args += ["--decrypt", decrypt_keyfile]
    return self._run("ebl", "parse", infile, *args).output

  def print(self, filename: str, **kwargs: Any) -> dict:
    """Print information about an EBL file.

    Args:
      filename (str): EBL file to print info about.

    Returns:
      Command output as parsed JSON (dict).
    """
    return self._run("ebl", "print", filename, *self._get_general_args(**kwargs)).output
