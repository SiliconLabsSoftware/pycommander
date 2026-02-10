"""Postbuild command: run post-build tasks from YAML."""

from typing import Any

from pycommander_core.commands._base import BaseCommand


class PostbuildCommand(BaseCommand):
  """Perform post-build tasks as defined in a post-build YAML (.slpb) file."""

  def _get_general_args(self, **kwargs: Any) -> list[str]:
    args = []
    args += self._get_kwargs(**kwargs)
    return args

  def postbuild(self,
                filename: str,
                parameters: list[tuple[str, str]] = [],
                dryrun: bool = False,
                **kwargs: Any) -> dict:
    """Run post-build tasks from a .slpb file.

    Args:
      filename (str): Input post-build YAML file (.slpb).
      parameters (list[tuple[str,str]]): Parameter overrides as (name, value).
      dryrun (bool): Resolve input filenames without running tasks.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if parameters:
      for name, value in parameters:
        args += ["--parameter", f"{name}:{value}"]
    if dryrun:
      args += ["--dryrun"]
    return self._run("postbuild", filename, *args).output
