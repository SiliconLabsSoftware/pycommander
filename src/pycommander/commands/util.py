"""Util commands: app info, ELF info, key/cert utilities, RPS info, usage, verify."""

from typing import Any

from pycommander.commands._base import BaseCommand


class UtilCommand(BaseCommand):
  """Utility commands (appinfo, elfinfo, extractkeys, gencert, genkey, etc.)."""

  def _get_general_args(self, **kwargs: Any) -> list[str]:
    args = []
    args += self._get_kwargs(**kwargs)
    return args

  def appinfo(self, filename: str, **kwargs: Any) -> dict:
    """Show all available info about an application.

    Args:
      filename (str): File to get info about.

    Returns:
      Command output as parsed JSON (dict).
    """
    return self._run("util", "appinfo", filename, *self._get_general_args(**kwargs)).output

  def elfinfo(self, filename: str, **kwargs: Any) -> dict:
    """Show information about the file's ELF sections.

    Args:
      filename (str): File to get ELF section info about.

    Returns:
      Command output as parsed JSON (dict).
    """
    return self._run("util", "elfinfo", filename, *self._get_general_args(**kwargs)).output

  def extractkeys(self, filename: str, dir: str, **kwargs: Any) -> dict:
    """Extract cryptographic keys from a JSON config file into a directory.

    Args:
      filename (str): JSON configuration file from which keys will be extracted.
      dir (str): Directory to store the extracted keys in.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    args += ["--dir", dir]
    return self._run("util", "extractkeys", filename, *args).output

  def gencert(self,
              outfile: str,
              cert_version: int,
              cert_type: str,
              cert_pubkey: str,
              sign_keyfile: str | None = None,
              extsign: bool = False,
              **kwargs: Any) -> dict:
    """Create a delegate certificate.

    Args:
      outfile (str): The file to write output to.
      cert_version (int): Running certificate version number; used for rollback
        prevention (device will not allow a lower cert than seen).
      cert_type (str): Type of certificate (e.g. gbl, secureboot).
      cert_pubkey (str): Public key file to be included in the certificate.
      sign_keyfile (str): Private key file used to sign the certificate.
      extsign (bool): If True, generate an unsigned certificate to be signed later
        via signcert.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
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
             tokenfile: str | None = None,
             **kwargs: Any) -> dict:
    """Generate a key for encrypt/decrypt or a key pair for signing.

    Args:
      type (str): Algorithm: "ecc-p256" (key pair for signing) or "aes-ccm"
        (key for encrypting/decrypting; requires outfile).
      pubkey (str): Filename to write the public key to; required with ecc-p256.
      privkey (str): Filename to write the private key to; required with ecc-p256.
      outfile (str): Output file (e.g. for aes-ccm key).
      tokenfile (str): Optional token file to write public key to (ecc-p256).

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
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

  def genkeyconfig(self, outfile: str, **kwargs: Any) -> dict:
    """Generate key configuration for SiWx91x devices.

    Args:
      outfile (str): The file to write output to.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    args += ["--outfile", outfile]
    return self._run("util", "genkeyconfig", *args).output

  def keytotoken(self,
                 keyfile: str,
                 outfile: str | None = None,
                 key_type: str | None = None,
                 **kwargs: Any) -> dict:
    """Convert a public key in PEM format to a token file for flashing.

    Args:
      keyfile (str): Input PEM public key file.
      outfile (str): The file to write output to.
      key_type (str): Key type (optional).

    Returns:
      Command output as parsed JSON (dict).
    """
    args = [keyfile] + self._get_general_args(**kwargs)
    if outfile is not None:
      args += ["--outfile", outfile]
    if key_type is not None:
      args += ["--type", key_type]
    return self._run("util", "keytotoken", *args).output

  def rpsinfo(self, filename: str, **kwargs: Any) -> dict:
    """Show information about an RPS application/key file.

    Args:
      filename (str): RPS file to get information about.

    Returns:
      Command output as parsed JSON (dict).
    """
    return self._run("util", "rpsinfo", filename, *self._get_general_args(**kwargs)).output

  def signcert(self,
               filename: str,
               signature: str,
               cert_type: str,
               outfile: str,
               verify_keyfile: str | None = None,
               **kwargs: Any) -> dict:
    """Sign a delegate certificate using a signature from an external party.

    Args:
      filename (str): Input certificate file.
      signature (str): Certificate signature (file or data).
      cert_type (str): Type of certificate (e.g. gbl, secureboot).
      outfile (str): The file to write output to.
      verify_keyfile (str): Public key file to verify the signature.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
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
            exclude_sections: list[str] = [],
            **kwargs: Any) -> dict:
    """Show flash and RAM usage of an ELF application.

    Args:
      filename (str): ELF file to get usage info about.
      map_filename (str): .map file to get the device memory layout from.
      include_sections (list[str]): ELF section names to include in usage statistics.
      exclude_sections (list[str]): ELF section names to exclude from usage statistics.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if map_filename is not None:
      args += ["--map", map_filename]
    if include_sections:
      args += self._get_include_sections(include_sections)
    if exclude_sections:
      args += self._get_exclude_sections(exclude_sections)
    return self._run("util", "usage", filename, *args).output

  def verifysign(self, filename: str, verify_keyfile: str, **kwargs: Any) -> dict:
    """Verify the signature of a file.

    Args:
      filename (str): File whose signature is to be verified.
      verify_keyfile (str): Public key file to verify the signature.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    args += ["--verify", verify_keyfile]
    return self._run("util", "verifysign", filename, *args).output
