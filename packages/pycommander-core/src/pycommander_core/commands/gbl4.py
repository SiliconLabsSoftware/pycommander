"""
License
Copyright 2026 Silicon Laboratories Inc. www.silabs.com
*******************************************************************************
The licensor of this software is Silicon Laboratories Inc. Your use of this
software is governed by the terms of Silicon Labs Master Software License
Agreement (MSLA) available at
www.silabs.com/about-us/legal/master-software-license-agreement. This
software is distributed to you in Source Code format and is governed by the
sections of the MSLA applicable to Source Code.
*******************************************************************************
"""

"""GBLv4 commands: create, createconfig, info, parse, sign."""

from typing import Any

from pycommander_core.commands._base import BaseCommand


class Gbl4Command(BaseCommand):
  """GBLv4 commands."""

  def _get_general_args(self, **kwargs: Any) -> list[str]:
    args = []
    args += self._get_kwargs(**kwargs)
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
             minversion: str | None = None,
             **kwargs: Any) -> dict:
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
    args = self._get_general_args(**kwargs)
    if config:
      args += ["--config", config]
    if data:
      for d in data:
        args += ["--data", d]
    if seupgrade:
      args += ["--seupgrade", seupgrade]
    if encrypt_keyfile:
      args += ["--encrypt", encrypt_keyfile]
    if compress:
      args += ["--compress", compress]
    if certificate:
      args += ["--certificate", certificate]
    if sign_keyfile:
      args += ["--sign", sign_keyfile]
    if extsign:
      args += ["--extsign"]
    if productid:
      args += ["--productid", productid]
    if bundleversion:
      args += ["--bundleversion", bundleversion]
    if minversion:
      args += ["--minversion", minversion]
    return self._run("gbl4", "create", outfile, *args).output

  def createconfig(self, outfile: str, **kwargs: Any) -> dict:
    """Create template config YAML file for GBLv4 input.

    Args:
      outfile (str): Output config file path.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    args += ["--outfile", outfile]
    return self._run("gbl4", "createconfig", *args).output

  def info(self, filename: str, **kwargs: Any) -> dict:
    """Parse and show info about a GBLv4 file.

    Args:
      filename (str): Input GBLv4 file.

    Returns:
      Command output as parsed JSON (dict).
    """
    return self._run("gbl4", "info", filename, *self._get_general_args(**kwargs)).output

  def parse(self,
            infile: str,
            seupgrade: str | None = None,
            outfile: str | None = None,
            **kwargs: Any) -> dict:
    """Parse a GBLv4 file; export updates and/or SE upgrade to files.

    Args:
      infile (str): Input GBLv4 file.
      seupgrade (str): Output filename for SE upgrade image.
      outfile (str): Output for updates (multiple get index suffix, e.g. file_0.s37).

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if seupgrade:
      args += ["--seupgrade", seupgrade]
    if outfile:
      args += ["--outfile", outfile]
    return self._run("gbl4", "parse", infile, *args).output

  def sign(self,
           infile: str,
           signature: str,
           outfile: str,
           verify_keyfile: str | None = None,
           **kwargs: Any) -> dict:
    """Sign a GBLv4 file using external signature (from create --extsign).

    Args:
      infile (str): Input unsigned GBLv4 file (from gbl4 create --extsign).
      signature (str): ECDSA signature of .manifest file in DER format.
      outfile (str): Output signed file path.
      verify_keyfile (str): ECC-P256 PEM public key to verify.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    args += ["--signature", signature]
    args += ["--outfile", outfile]
    if verify_keyfile:
      args += ["--verify", verify_keyfile]
    return self._run("gbl4", "sign", infile, *args).output
