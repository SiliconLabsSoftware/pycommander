from pycommander.commands._base import BaseCommand

class VerifyCommand(BaseCommand):

  def _get_general_args(self) -> list[str]:
    args = []
    args += self._get_adapter_connection_args()
    args += self._get_device_args()
    args += self._get_debug_args()
    args += self._get_flags()
    return args

  def verify(self,
             filenames: list[str] | None = None,
             address: int | None = None,
             patches: list[str] = [],
             tokens: list[str] = [],
             tokenfiles: list[str] = [],
             tokengroup: str | None = None,
             tokendefs: str | None = None,
             blank: bool = False,
             reset: bool = True,
             regions: list[str] = [],
             binary: bool = False) -> dict:
    args = self._get_general_args()
    if filenames:
      args = list(filenames) + args
    if address is not None:
      args += ["--address", self._get_address_string(address)]
    if patches:
      args += self._get_patches(patches)
    if tokens:
      args += self._get_tokens(tokens)
    if tokenfiles:
      args += self._get_tokenfiles(tokenfiles)
    if tokengroup is not None:
      args += ["--tokengroup", tokengroup]
    if tokendefs is not None:
      args += ["--tokendefs", tokendefs]
    if blank:
      args += ["--blank"]
    if not reset:
      args += ["--noreset"]
    if regions:
      args += self._get_regions(regions)
    if binary:
      args += ["--binary"]
    return self._run("verify", *args).output
