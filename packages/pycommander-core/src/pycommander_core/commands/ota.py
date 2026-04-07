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

"""OTA commands: create, parse, sign, verify."""

from typing import Any

from pycommander_core.commands._base import BaseCommand


class OtaCommand(BaseCommand):
  """OTA commands."""

  def _get_general_args(self, **kwargs: Any) -> list[str]:
    args = []
    args += self._get_kwargs(**kwargs)
    return args

  def create(self,
             outfile: str,
             type: str | None = None,
             input_files: list[str] = [],
             vendorid: int | None = None,
             productid: int | None = None,
             swversion: int | None = None,
             swstring: str | None = None,
             min_sw: int | None = None,
             max_sw: int | None = None,
             releasenote: str | None = None,
             digest: str | None = None,
             upgrade_images: list[str] = [],
             firmware_version: int | None = None,
             manufacturer_id: int | None = None,
             image_type: int | None = None,
             string: str | None = None,
             stack_version: int | None = None,
             credentials: int | None = None,
             destination: str | None = None,
             min_hw: int | None = None,
             max_hw: int | None = None,
             null_tag: str | None = None,
             manufacturer_tags: list[str] = [],
             certificate: str | None = None,
             sign: bool = False,
             extsign: bool = False,
             **kwargs: Any) -> dict:
    """Create OTA file (Matter or Zigbee).

    Args:
      outfile (str): Output file path.
      type (str): matter or zigbee (default zigbee).
      input_files (list[str]): Matter: upgrade file(s).
      vendorid (int): Matter vendor ID.
      productid (int): Matter product ID.
      swversion (int): Matter software version.
      swstring (str): Matter human-readable version.
      min_sw (int): Matter minimum software version.
      max_sw (int): Matter maximum software version.
      releasenote (str): Matter release notes URL.
      digest (str): Matter digest algorithm (sha256, sha384, etc.).
      upgrade_images (list[str]): Zigbee: GBL file(s).
      firmware_version (int): Zigbee firmware version.
      manufacturer_id (int): Zigbee manufacturer ID.
      image_type (int): Zigbee image type ID.
      string (str): Zigbee header string.
      stack_version (int): Zigbee stack version.
      credentials (int): Zigbee security credentials.
      destination (str): Zigbee destination.
      min_hw (int): Zigbee minimum hardware version.
      max_hw (int): Zigbee maximum hardware version.
      null_tag (str): Zigbee null tag.
      manufacturer_tags (list[str]): Zigbee manufacturer tag(s).
      certificate (str): Certificate file.
      sign (bool): Sign the OTA file.
      extsign (bool): Output for external signing.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    args += ["--outfile", outfile]
    if type:
      args += ["--type", type]
    if input_files:
      for file in input_files:
        args += ["--input", file]
    if vendorid is not None:
      args += ["--vendorid", str(vendorid)]
    if productid is not None:
      args += ["--productid", str(productid)]
    if swversion is not None:
      args += ["--swversion", str(swversion)]
    if swstring:
      args += ["--swstring", swstring]
    if min_sw is not None:
      args += ["--min-sw", str(min_sw)]
    if max_sw is not None:
      args += ["--max-sw", str(max_sw)]
    if releasenote:
      args += ["--releasenote", releasenote]
    if digest:
      args += ["--digest", digest]
    if upgrade_images:
      for image in upgrade_images:
        args += ["--upgrade-image", image]
    if firmware_version is not None:
      args += ["--firmware-version", str(firmware_version)]
    if manufacturer_id is not None:
      args += ["--manufacturer-id", str(manufacturer_id)]
    if image_type is not None:
      args += ["--image-type", str(image_type)]
    if string:
      args += ["--string", string]
    if stack_version is not None:
      args += ["--stack-version", str(stack_version)]
    if credentials is not None:
      args += ["--credentials", str(credentials)]
    if destination:
      args += ["--destination", destination]
    if min_hw is not None:
      args += ["--min-hw", str(min_hw)]
    if max_hw is not None:
      args += ["--max-hw", str(max_hw)]
    if null_tag:
      args += ["--null", null_tag]
    if manufacturer_tags is not None:
      for tag in manufacturer_tags:
        args += ["--manufacturer-tag", tag]
    if certificate:
      args += ["--certificate", certificate]
    if sign:
      args += ["--sign"]
    if extsign:
      args += ["--extsign"]
    return self._run("ota", "create", *args).output

  def parse(self,
            filename: str,
            type: str | None = None,
            outfile: str | None = None,
            **kwargs: Any) -> dict:
    """Parse an OTA file.

    Args:
      filename (str): Input OTA file.
      type (str): matter or zigbee.
      outfile (str): Output file path.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if type:
      args += ["--type", type]
    if outfile:
      args += ["--outfile", outfile]
    return self._run("ota", "parse", filename, *args).output

  def sign(self,
           filename: str,
           signature: str,
           outfile: str,
           curve: str,
           **kwargs: Any) -> dict:
    """Sign an OTA file.

    Args:
      filename (str): Input OTA file.
      signature (str): Signature file.
      outfile (str): Output signed file path.
      curve (str): Curve name for signing.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    args += ["--signature", signature]
    args += ["--outfile", outfile]
    args += ["--curve", curve]
    return self._run("ota", "sign", filename, *args).output

  def verify(self, filename: str, certificate: str, **kwargs: Any) -> dict:
    """Verify an OTA file with a certificate.

    Args:
      filename (str): OTA file to verify.
      certificate (str): Certificate file path.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    args += ["--certificate", certificate]
    return self._run("ota", "verify", filename, *args).output
