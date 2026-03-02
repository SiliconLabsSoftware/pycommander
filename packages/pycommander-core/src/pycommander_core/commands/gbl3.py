"""GBL3 commands: create, parse, sign, keygen, keyconvert, aat-usageinfo."""

from typing import Any

from pycommander_core.commands._base import BaseCommand


class Gbl3Command(BaseCommand):
  """Create, parse and other handling for GBL3 files."""

  def _get_general_args(self, **kwargs: Any) -> list[str]:
    args = []
    args += self._get_kwargs(**kwargs)
    return args

  def aat_usageinfo(self, **kwargs: Any) -> dict:
    """Display flash and RAM usage from AAT data (Zigbee/Thread; RAM for EM3xx only).

    Returns:
      Command output as parsed JSON (dict).
    """
    return self._run("gbl3", "aat-usageinfo", *self._get_general_args(**kwargs)).output

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
             verify_keyfile: str | None = None,
             **kwargs: Any) -> dict:
    """Create a GBL3 file.

    Args:
      outfile (str): Output GBL3 file path.
      app (str): Application image for GBL3.
      bootloader (str): Bootloader image (with bootloader upgrade support).
      seupgrade (str): Secure Engine upgrade image.
      metadata (str): Metadata binary file.
      compress (str): Compression for app: lz4 or lzma.
      certificate (str): Certificate to add.
      include_sections (list[str]): ELF sections to include.
      exclude_sections (list[str]): ELF sections to exclude.
      seunencrypted (bool): Place SE upgrade outside encrypted area.
      dep_app (str): App version dependency (e.g. statement:version).
      dep_boot (str): Bootloader version dependency (major.minor.patch).
      dep_se (str): SE upgrade version dependency.
      delta_app (str): Create delta-upgrade GBL3 from this app (with --app).
      sign_keyfile (str): ECC-P256 PEM private key to sign.
      encrypt_keyfile (str): AES key file to encrypt (gbl3 keygen --type aes-ccm).
      extsign (bool): Output .extsign for external signature (then gbl3 sign).
      signature (str): DER ECDSA signature file.
      verify_keyfile (str): ECC-P256 PEM public key to verify.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if app:
      args += ["--app", app]
    if bootloader:
      args += ["--bootloader", bootloader]
    if seupgrade:
      args += ["--seupgrade", seupgrade]
    if metadata:
      args += ["--metadata", metadata]
    if compress:
      args += ["--compress", compress]
    if certificate:
      args += ["--certificate", certificate]
    if include_sections:
      args += self._get_include_sections(include_sections)
    if exclude_sections:
      args += self._get_exclude_sections(exclude_sections)
    if seunencrypted:
      args += ["--seunencrypted"]
    if dep_app:
      args += ["--dep-app", dep_app]
    if dep_boot:
      args += ["--dep-boot", dep_boot]
    if dep_se:
      args += ["--dep-se", dep_se]
    if delta_app:
      args += ["--delta-app", delta_app]
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
    return self._run("gbl3", "create", outfile, *args).output

  def keyconvert(self,
                 infile: str,
                 type: str | None = None,
                 outfile: str | None = None,
                 **kwargs: Any) -> dict:
    """Convert PEM public key to token file. Deprecated: use util keytotoken.

    Args:
      infile (str): Input PEM public key file.
      type (str): Algorithm: aes-ccm or ecc-p256.
      outfile (str): Output file path.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if type:
      args += ["--type", type]
    if outfile:
      args += ["--outfile", outfile]
    return self._run("gbl3", "keyconvert", infile, *args).output

  def keygen(self,
             type: str,
             outfile: str | None = None,
             **kwargs: Any) -> dict:
    """Generate key for encrypt/sign. Deprecated: use util genkey.

    Args:
      type (str): Algorithm: aes-ccm or ecc-p256.
      outfile (str): Output file path.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = ["--type", type] + self._get_general_args(**kwargs)
    if outfile:
      args += ["--outfile", outfile]
    return self._run("gbl3", "keygen", *args).output

  def parse(self,
            infile: str,
            app: str | None = None,
            bootloader: str | None = None,
            seupgrade: str | None = None,
            metadata: str | None = None,
            verify_keyfile: str | None = None,
            decrypt_keyfile: str | None = None,
            **kwargs: Any) -> dict:
    """Parse a GBL3 file.

    Args:
      infile (str): Input GBL3 file.
      app (str): File to write application image to.
      bootloader (str): File to write bootloader image to.
      seupgrade (str): File to write SE upgrade image to.
      metadata (str): File to write metadata binary to.
      verify_keyfile (str): ECC-P256 PEM public key to verify signature.
      decrypt_keyfile (str): AES key file to decrypt.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if app:
      args += ["--app", app]
    if bootloader:
      args += ["--bootloader", bootloader]
    if seupgrade:
      args += ["--seupgrade", seupgrade]
    if metadata:
      args += ["--metadata", metadata]
    if verify_keyfile:
      args += ["--verify", verify_keyfile]
    if decrypt_keyfile:
      args += ["--decrypt", decrypt_keyfile]
    return self._run("gbl3", "parse", infile, *args).output

  def sign(self,
           infile: str,
           outfile: str,
           signature: str,
           verify_keyfile: str | None = None,
           **kwargs: Any) -> dict:
    """Sign a GBL3 file using a signature from an external party.

    Args:
      infile (str): Input GBL3 file (e.g. .extsign from create --extsign).
      outfile (str): Output signed file path.
      signature (str): DER ECDSA signature file.
      verify_keyfile (str): ECC-P256 PEM public key to verify.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    args += ["--outfile", outfile]
    args += ["--signature", signature]
    if verify_keyfile:
      args += ["--verify", verify_keyfile]
    return self._run("gbl3", "sign", infile, *args).output
