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

"""Postbuild command: run post-build tasks from YAML."""

from typing import Any

from pycommander_core.commands._base import BaseCommand


class PostbuildCommand(BaseCommand):
  """Perform post-build tasks as defined in a post-build YAML (.slpb) file."""

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
