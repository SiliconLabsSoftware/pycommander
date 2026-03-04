import json

from pathlib import Path
from collections import namedtuple

from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from .commands import *

from .types import CommanderVersionInfo
from .runner import Runner, RunnerResult
from ._ensure_commander import ensure_commander
from ._utils import sanitize_args

CommanderResult = namedtuple("CommanderResult", ["returncode", "output"])

class CommanderBase:
  # Command overview. These are for type hinting only.
  # The real commands are initialized in the __init__ method.
  adapter   : "AdapterCommand"
  aem       : "AemCommand"
  convert   : "ConvertCommand"
  ctune     : "CtuneCommand"
  device    : "DeviceCommand"
  ebl       : "EblCommand"
  extflash  : "ExtflashCommand"
  flash     : "FlashCommand"
  gbl3      : "Gbl3Command"
  gbl4      : "Gbl4Command"
  littlefs  : "LittlefsCommand"
  mfg917    : "Mfg917Command"
  nvm3      : "Nvm3Command"
  ota       : "OtaCommand"
  postbuild : "PostbuildCommand"
  readmem   : "ReadmemCommand"
  rps       : "RpsCommand"
  security  : "SecurityCommand"
  serial    : "SerialCommand"
  tokens    : "TokensCommand"
  util      : "UtilCommand"
  vcom      : "VcomCommand"
  verify    : "VerifyCommand"

  default_timeout_s : int = 300

  def __init__(self, 
              serial_number:    str  | None = None,
              ip_address:       str  | None = None,
              serial_port:      str  | None = None,
              debug_speed:      int  | None = None,
              debug_tif:        str  | None = None,
              debug_irpre:      int  | None = None,
              debug_drpre:      int  | None = None,
              log_file_path:    Path | None = None,
              executable_path:  Path | None = None,
              cli:              bool | None = None):

    if (serial_number and ip_address) or (serial_number and serial_port) or (ip_address and serial_port):
      raise ValueError("Only one of serial_number, ip_address, or serial_port can be provided")

    if executable_path:
      if not isinstance(executable_path, Path):
        executable_path = Path(executable_path)

      if not executable_path.exists():
        raise FileNotFoundError(f"Executable not found: {str(executable_path)}")
      self._executable_path = executable_path
    else:
      if cli is None:
        raise ValueError("cli must be provided if executable_path is not provided")
      self._executable_path = ensure_commander(cli=cli)

    self._runner : Runner = Runner(self._executable_path, log_file_path=log_file_path, timeout_s=CommanderBase.default_timeout_s)

    # Adapter-specific parameters
    self._serial_number : str | None = serial_number
    self._ip_address    : str | None = ip_address
    self._serial_port   : str | None = serial_port

    # Debug parameters
    self._debug_speed : int | None = debug_speed
    self._debug_tif   : str | None = debug_tif
    self._debug_irpre : int | None = debug_irpre
    self._debug_drpre : int | None = debug_drpre

    # Initialize all the available commands
    from . import commands
    for name in commands.__all__:
      command_class = getattr(commands, name)
      attribute_name = name.removesuffix("Command").lower() # e.g. "AdapterCommand" -> "adapter"
      setattr(self, attribute_name, command_class(self))


  def getVersion(self) -> CommanderVersionInfo | None:
    """Get the version information for the Commander executable.

    Returns:
      A CommanderVersionInfo object containing the version of the Commander executable.
    """
    result : RunnerResult = self._runner.run("--version", json_format=True)

    if result.returncode != 0:
      return None

    json_output = json.loads(result.output)
    if "result" not in json_output or "version" not in json_output["result"]:
      return None

    version_info = CommanderVersionInfo(
      simplicity_commander_version=json_output["result"]["version"]["simplicity_commander_version"],
      jlink_dll_version=json_output["result"]["version"]["jlink_dll_version"],
      emdll_version=json_output["result"]["version"]["emdll_version"],
      mbed_tls_version=json_output["result"]["version"]["mbed_tls_version"],
      qt_version=json_output["result"]["version"]["qt_version"],
    )

    return version_info

  def runCommand(self, *args : str, json_formatted_output: bool = True) -> CommanderResult | dict:
    """Run a command and return the result.

    Args:
      args (str): The arguments to pass to the command.
      json_formatted_output (bool): Whether to return the output as JSON.

    Returns:
      The result of the command.
    """

    result : RunnerResult = self._runner.run(*sanitize_args(args), json_format=json_formatted_output)
    if json_formatted_output:
      return json.loads(result.output)
    else:
      return CommanderResult(result.returncode, result.output)
