import json

from abc import ABC
from collections import namedtuple

from pycommander.pycommander import PyCommander
from pycommander.runner import Runner, RunnerResult

CommandResult = namedtuple("CommandResult", ["returncode", "output"])

class BaseCommand(ABC):
  def __init__(self, commander: PyCommander):
    self._commander : PyCommander = commander
    self._runner : Runner = self._commander._runner


  def _run(self, *args: str) -> CommandResult:
    print(args) # TODO: Remove before flight

    # Strip away any empty elements
    args = [arg for arg in args if arg]

    result : RunnerResult = self._runner.run(*args, "--json")
    json_output = json.loads(result.output)

    return CommandResult(result.returncode, json_output)


  # Adapter connection arguments
  def _get_adapter_connection_args(self) -> list[str]:
    args = []
    args += self.__get_serial_number_option()
    args += self.__get_ip_address_option()
    args += self.__get_serial_port_option()
    return args

  def __get_serial_number_option(self) -> list[str]:
    if self._commander._serial_number:
      return ["--serialno", self._commander._serial_number]
    return []

  def __get_ip_address_option(self) -> list[str]:
    if self._commander._ip_address:
      return ["--ip", self._commander._ip_address]
    return []

  def __get_serial_port_option(self) -> list[str]:
    if self._commander._serial_port:
      return ["--identifybyserialport", self._commander._serial_port]
    return []


  # Device arguments
  def _get_device_args(self) -> list[str]:
    args = []
    if self._commander._target_device:
      args += ["--device", self._commander._target_device]
    return args


  # Debug arguments
  def _get_debug_args(self) -> list[str]:
    args = []
    args += self.__get_debug_speed_option()
    args += self.__get_debug_tif_option()
    args += self.__get_debug_irpre_option()
    args += self.__get_debug_drpre_option()
    return args

  def __get_debug_speed_option(self) -> list[str]:
    if self._commander._debug_speed:
      return ["--speed", str(self._commander._debug_speed)]
    return []

  def __get_debug_tif_option(self) -> list[str]:
    if self._commander._debug_tif:
      return ["--tif", self._commander._debug_tif]
    return []

  def __get_debug_irpre_option(self) -> list[str]:
    if self._commander._debug_irpre:
      return ["--irpre", str(self._commander._debug_irpre)]
    return []

  def __get_debug_drpre_option(self) -> list[str]:
    if self._commander._debug_drpre:
      return ["--drpre", str(self._commander._debug_drpre)]
    return []


  # Flag arguments
  def _get_flags(self) -> list[str]:
    args = []
    args += self.__get_force_option()
    args += self.__get_show_timestamps_option()
    return args

  def __get_force_option(self) -> list[str]:
    if self._commander._force:
      return ["--force"]
    return []

  def __get_show_timestamps_option(self) -> list[str]:
    if self._commander._show_timestamps:
      return ["--timestamp"]
    return []


  # Helper methods for common arguments
  def _get_address(self, address: int) -> str:
    return f"0x{address:08X}"

  def _get_ranges(self, ranges: list[tuple[int, int]]) -> list[str]:
    args = []
    for range in ranges:
      start = range[0]
      end   = range[1]

      args += ["--range", f"0x{start:X}:0x{end:X}"]
    return args

  def _get_regions(self, regions: list[str]) -> list[str]:
    args = []
    for region in regions:
      args += ["--region", region]
    return args

  def _get_patches(self, patches: list[str]) -> list[str]:
    args = []
    for patch in patches:
      args += ["--patch", patch]
    return args

  def _get_tokens(self, tokens: list[str]) -> list[str]:
    args = []
    for token in tokens:
      args += ["--token", token]
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
