import json
import importlib

from pathlib import Path
from collections import namedtuple

from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from .commands import *

from .paths import EXECUTABLE_PATH
from .runner import Runner, RunnerResult

CommanderResult = namedtuple("CommanderResult", ["returncode", "output"])
LogConfig       = namedtuple("LogConfig", ["file", "kit_name"])

class PyCommander:
  # Command overview. These are for type hinting only.
  # The commands are initialized in the __init__ method.
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

  def __init__(self, 
              serial_number: str | None = None,
              ip_address: str | None = None,
              serial_port: str | None = None,
              target_device: str | None = None,
              debug_speed: int | None = None,
              debug_tif: str | None = None,
              debug_irpre: int | None = None,
              debug_drpre: int | None = None,
              force: bool = False,
              show_timestamps: bool = False,
              log_config: LogConfig | None = None,
              executable_path: Path = EXECUTABLE_PATH):

    self._runner : Runner = Runner(executable_path)
    
    # Adapter-specific parameters
    self._serial_number : str | None = serial_number
    self._ip_address    : str | None = ip_address
    self._serial_port   : str | None = serial_port

    # Device-specific parameters
    self._target_device : str | None = target_device

    # Debug parameters
    self._debug_speed : int | None = debug_speed
    self._debug_tif   : str | None = debug_tif
    self._debug_irpre : int | None = debug_irpre
    self._debug_drpre : int | None = debug_drpre

    # Flags
    self._force           : bool = force
    self._show_timestamps : bool = show_timestamps

    # Logging
    self._log_config  : LogConfig | None = log_config # TODO: To do

    # Initialize available commands
    from . import commands
    for name in commands.__all__:
      command_class = getattr(commands, name)
      attribute_name = name.removesuffix("Command").lower() # e.g. "AdapterCommand" -> "adapter"
      setattr(self, attribute_name, command_class(self))

  def getVersionString(self) -> str:
    result : RunnerResult = self._runner.run("--version", "--json")

    json_output = json.loads(result.output)
    version_string = json_output["result"]["version"]["simplicity_commander_version"]

    return version_string


  def runCommand(self, *args : str) -> CommanderResult:
    result : RunnerResult = self._runner.run(*args)
    return CommanderResult(result.returncode, result.output)
