from pycommander.commands._base import BaseCommand

class OtaCommand(BaseCommand):

  def _get_general_args(self) -> list[str]:
    args = []
    args += self._get_device_args()
    args += self._get_flags()
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
             extsign: bool = False) -> dict:
    args = self._get_general_args()
    args += ["--outfile", outfile]
    if type is not None:
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
    if swstring is not None:
      args += ["--swstring", swstring]
    if min_sw is not None:
      args += ["--min-sw", str(min_sw)]
    if max_sw is not None:
      args += ["--max-sw", str(max_sw)]
    if releasenote is not None:
      args += ["--releasenote", releasenote]
    if digest is not None:
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
    if string is not None:
      args += ["--string", string]
    if stack_version is not None:
      args += ["--stack-version", str(stack_version)]
    if credentials is not None:
      args += ["--credentials", str(credentials)]
    if destination is not None:
      args += ["--destination", destination]
    if min_hw is not None:
      args += ["--min-hw", str(min_hw)]
    if max_hw is not None:
      args += ["--max-hw", str(max_hw)]
    if null_tag is not None:
      args += ["--null", null_tag]
    if manufacturer_tags is not None:
      for tag in manufacturer_tags:
        args += ["--manufacturer-tag", tag]
    if certificate is not None:
      args += ["--certificate", certificate]
    if sign:
      args += ["--sign"]
    if extsign:
      args += ["--extsign"]
    return self._run("ota", "create", *args).output

  def parse(self,
            filename: str,
            type: str | None = None,
            outfile: str | None = None) -> dict:
    args = self._get_general_args()
    if type is not None:
      args += ["--type", type]
    if outfile is not None:
      args += ["--outfile", outfile]
    return self._run("ota", "parse", filename, *args).output

  def sign(self,
           filename: str,
           signature: str,
           outfile: str,
           curve: str) -> dict:
    args = self._get_general_args()
    args += ["--signature", signature]
    args += ["--outfile", outfile]
    args += ["--curve", curve]
    return self._run("ota", "sign", filename, *args).output

  def verify(self, filename: str, certificate: str) -> dict:
    args = self._get_general_args()
    args += ["--certificate", certificate]
    return self._run("ota", "verify", filename, *args).output
