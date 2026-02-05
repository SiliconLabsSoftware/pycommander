"""Postbuild command: run post-build tasks from YAML."""

from pycommander.commands._base import BaseCommand


class PostbuildCommand(BaseCommand):
  """Perform post-build tasks as defined in a post-build YAML (.slpb) file."""

  def _get_general_args(self) -> list[str]:
    args = []
    args += self._get_device_args()
    args += self._get_flags()
    return args

  def postbuild(self,
                filename: str,
                parameters: list[tuple[str, str]] = [],
                dryrun: bool = False) -> dict:
    """Run post-build tasks from a .slpb file.

    Args:
      filename (str): Input post-build YAML file (.slpb).
      parameters (list[tuple[str,str]]): Parameter overrides as (name, value).
      dryrun (bool): Resolve input filenames without running tasks.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args()
    if parameters:
      for name, value in parameters:
        args += ["--parameter", f"{name}:{value}"]
    if dryrun:
      args += ["--dryrun"]
    return self._run("postbuild", filename, *args).output
