from pycommander.commands._base import BaseCommand

class PostbuildCommand(BaseCommand):

  def _get_general_args(self) -> list[str]:
    args = []
    args += self._get_device_args()
    args += self._get_flags()
    return args

  def postbuild(self,
                filename: str,
                parameters: list[tuple[str, str]] = [],
                dryrun: bool = False) -> dict:
    args = self._get_general_args()
    if parameters:
      for name, value in parameters:
        args += ["--parameter", f"{name}:{value}"]
    if dryrun:
      args += ["--dryrun"]
    return self._run("postbuild", filename, *args).output
