import json

from pathlib import Path
from collections import namedtuple

from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from .commands import *

from .paths import EXECUTABLE_PATH
from .runner import Runner, RunnerResult
from ._ensure_commander import ensure_commander

CommanderResult = namedtuple("CommanderResult", ["returncode", "output"])

class Commander:
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
              executable_path:  Path        = EXECUTABLE_PATH):

    if executable_path == EXECUTABLE_PATH:
      # If we're using the default executable, ensure we are unzipped and ready to go.
      ensure_commander()

    self._runner : Runner = Runner(executable_path, log_file_path=log_file_path, timeout_s=Commander.default_timeout_s)
    
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


  def getVersion(self) -> str:
    """Get the version of the Commander executable.

    Returns:
      The version of the Commander executable, e.g. "1v22p0b1234"
    """
    result : RunnerResult = self._runner.run("--version", "--json")

    json_output = json.loads(result.output)
    version_string = json_output["result"]["version"]["simplicity_commander_version"]

    return version_string

  def runCommand(self, *args : str, json_formatted_output: bool = True) -> CommanderResult | dict:
    """Run a command and return the result.

    Args:
      args (str): The arguments to pass to the command.
      json_formatted_output (bool): Whether to return the output as JSON.

    Returns:
      The result of the command.
    """
    result : RunnerResult = self._runner.run(*args, json=json_formatted_output)
    if json_formatted_output:
      return json.loads(result.output)
    else:
      return CommanderResult(result.returncode, result.output)
