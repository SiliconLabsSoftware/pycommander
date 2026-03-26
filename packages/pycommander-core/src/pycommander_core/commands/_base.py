import json

from collections import namedtuple
from typing import Any

from pycommander_core.commander_base import CommanderBase
from pycommander_core.runner import Runner, RunnerResult
from pycommander_core._utils import sanitize_args

CommandResult = namedtuple("CommandResult", ["returncode", "output"])

class BaseCommand:
  def __init__(self, commander: CommanderBase):
    self._commander : CommanderBase = commander
    self._runner : Runner = self._commander._runner


  def _run(self, *args: str) -> CommandResult:
    result : RunnerResult = self._runner.run(*sanitize_args(args), json_format=True)
    command_result : CommandResult | None = None
    try:
      json_output = json.loads(result.output) 
      command_result = CommandResult(result.returncode, json_output)
    except json.JSONDecodeError:
      # If the output wasn't pure JSON, we shoehorn it regardless.
      if result.returncode == 0:
        command_result = CommandResult(result.returncode, {"success": True, "output": result.output})
      else:
        command_result = CommandResult(result.returncode, {"success": False, "error": result.output})

    return command_result

  # Adapter connection arguments are kept by the commander class
  def _get_adapter_connection_args(self) -> list[str]:
    args = []
    args += self._commander._get_serial_number_option()
    args += self._commander._get_ip_address_option()
    args += self._commander._get_serial_port_option()
    return args

  # Debug arguments are kept by the commander class
  def _get_debug_args(self) -> list[str]:
    args = []
    args += self._commander._get_debug_speed_option()
    args += self._commander._get_debug_tif_option()
    args += self._commander._get_debug_irpre_option()
    args += self._commander._get_debug_drpre_option()
    return args

  # Keyword arguments
  def _get_kwargs(self, **kwargs: Any) -> list[str]:
    args = []
    if kwargs.get("device"):
      args += ["--device", kwargs["device"]]
    if kwargs.get("force", False):
      args += ["--force"]
    return args

  # Helper methods for common arguments
  def _get_address_string(self, address: int) -> str:
    return f"0x{address:08X}"

  def _get_ranges(self, ranges: list[tuple[int | str, int | str]]) -> list[str]:
    args = []
    for range in ranges:
      if not isinstance(range, tuple) or len(range) != 2:
        raise ValueError(f"Range must be a tuple with 2 elements: {range}")

      start = range[0]
      end   = range[1]

      if isinstance(start, int):
        start = self._get_address_string(start)
      if isinstance(end, int):
        end = self._get_address_string(end)

      args += ["--range", f"{start}:{end}"]
    return args

  def _get_secureranges(self, secureranges: list[tuple[int | str, int | str]]) -> list[str]:
    args = []
    for securerange in secureranges:
      if not isinstance(securerange, tuple) or len(securerange) != 2:
        raise ValueError(f"Secure range must be a tuple with 2 elements: {securerange}")

      start = securerange[0]
      end   = securerange[1]

      if isinstance(start, int):
        start = self._get_address_string(start)
      if isinstance(end, int):
        end = self._get_address_string(end)

      args += ["--securerange", f"{start}:{end}"]
    return args

  def _get_regions(self, regions: list[str]) -> list[str]:
    args = []
    for region in regions:
      args += ["--region", region]
    return args

  def _get_patches(self, patches: list[tuple[int | str, int | str, int | str | None]]) -> list[str]:
    args = []
    for patch in patches:
      if not isinstance(patch, tuple) or len(patch) not in [2, 3]:
        raise ValueError(f"Patch must be a tuple with 2 or 3 elements: {patch}")

      start = patch[0]
      end   = patch[1]

      if len(patch) > 2:
        length = patch[2]
      else:
        length = None

      if isinstance(start, int):
        start = self._get_address_string(start)
      if isinstance(end, int):
        end = self._get_address_string(end)
      if length is not None and isinstance(length, int):
        length = str(length)

      args += ["--patch", f"{start}:{end}{f':{length}' if length is not None else ''}"]
    return args

  def _get_tokens(self, tokens: list[tuple[str, str]]) -> list[str]:
    args = []
    for token in tokens:
      token_name = token[0]
      token_value = token[1]
      args += ["--token", f"{token_name}:{token_value}"]
    return args

  def _get_token_names(self, tokens: list[str]) -> list[str]:
    args = []
    for token_name in tokens:
      args += ["--token", token_name]
    return args

  def _get_tokenfiles(self, tokenfiles: list[str]) -> list[str]:
    args = []
    for tokenfile in tokenfiles:
      args += ["--tokenfile", tokenfile]
    return args

  def _get_include_sections(self, include_sections: list[str]) -> list[str]:
    args = []
    for section in include_sections:
      args += ["--include-section", section]
    return args

  def _get_exclude_sections(self, exclude_sections: list[str]) -> list[str]:
    args = []
    for section in exclude_sections:
      args += ["--exclude-section", section]
    return args
