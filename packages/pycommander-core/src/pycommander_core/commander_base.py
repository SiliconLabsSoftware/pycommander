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

import json

from pathlib import Path
from collections import namedtuple

from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
  from .commands import *

from .types import CommanderVersionInfo, BasicAdapterInfo
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
              target_device:    str  | None = None,
              debug_speed:      int  | None = None,
              debug_tif:        str  | None = None,
              debug_irpre:      int  | None = None,
              debug_drpre:      int  | None = None,
              log_file_path:    Path | None = None,
              executable_path:  Path | None = None,
              cli:              bool | None = None,
              **kwargs):

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

    # Additional parameters
    self._target_device : str | None = target_device

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

  def listAvailableAdapters(self, list_usb_adapters: bool = False, list_network_adapters: bool = False) -> list[BasicAdapterInfo] | None:
    """Do an unintrusive scan for available adapters across the USB interface or the network.

    Args:
      list_usb_adapters (bool): Whether to list USB adapters.
      list_network_adapters (bool): Whether to list network adapters.

    Returns:
      A list of BasicAdapterInfo objects, or None if the list could not be retrieved.
    """
    if list_usb_adapters and list_network_adapters:
      raise ValueError("Only one of list_usb_adapters or list_network_adapters can be True")

    args = ["--noconnect"]
    if list_network_adapters:
      args += ["--net"]
    result : RunnerResult = self._runner.run("adapter", "list", *args)

    if result.returncode != 0:
      return None

    json_output = json.loads(result.output)
    if "result" not in json_output or "devices" not in json_output["result"]:
      return None
    
    adapter_list : list[BasicAdapterInfo] = []
    for device in json_output["result"]["devices"]:
       ip_address    : str | None = device.get("adapter_ip", None)
       nickname      : str | None = device.get("adapter_nickname", None)
       serial_number : str | None = device.get("serial_number", None)
       adapter_list.append(BasicAdapterInfo(jlink_serial_number=serial_number, ip_address=ip_address, nickname=nickname))

    return adapter_list

  def runCommand(self, *args : str, json_formatted_output: bool = True, **kwargs: Any) -> CommanderResult | dict:
    """Run a command and return the result.

    Args:
      args (str): The arguments to pass to the command.
      json_formatted_output (bool): Whether to return the output as JSON.

    Returns:
      The result of the command.
    """

    args = list(args) + self._get_kwargs(**kwargs)

    result : RunnerResult = self._runner.run(*sanitize_args(args), json_format=json_formatted_output)
    if json_formatted_output:
      return json.loads(result.output)
    else:
      return CommanderResult(result.returncode, result.output)


  def _get_kwargs(self, **kwargs: Any) -> list[str]:
    args = []

    # Temporary connection options
    if kwargs.get("serial_number"):
      args += ["--serialno", kwargs["serial_number"]]
    if kwargs.get("ip_address"):
      args += ["--ip", kwargs["ip_address"]]
    if kwargs.get("serial_port"):
      args += ["--identifybyserialport", kwargs["serial_port"]]

    # Temporary debug options
    if kwargs.get("debug_speed"):
      args += ["--speed", str(kwargs["debug_speed"])]
    if kwargs.get("debug_tif"):
      args += ["--tif", kwargs["debug_tif"]]
    if kwargs.get("debug_irpre"):
      args += ["--irpre", str(kwargs["debug_irpre"])]
    if kwargs.get("debug_drpre"):
      args += ["--drpre", str(kwargs["debug_drpre"])]

    # Other temporary options
    if kwargs.get("target_device"):
      args += ["--device", kwargs["target_device"]]

    if kwargs.get("force", False):
      args += ["--force"]

    if kwargs.get("devicexml"):
      args += ["--devicexml", kwargs["devicexml"]]

    return args

  def _get_serial_number_option(self) -> list[str]:
    if self._serial_number:
      return ["--serialno", self._serial_number]
    return []

  def _get_ip_address_option(self) -> list[str]:
    if self._ip_address:
      return ["--ip", self._ip_address]
    return []

  def _get_serial_port_option(self) -> list[str]:
    if self._serial_port:
      return ["--identifybyserialport", self._serial_port]
    return []

  def _get_device_option(self) -> list[str]:
    if self._target_device:
      return ["--device", self._target_device]
    return []

  def _get_debug_speed_option(self) -> list[str]:
    if self._debug_speed:
      return ["--speed", str(self._debug_speed)]
    return []

  def _get_debug_tif_option(self) -> list[str]:
    if self._debug_tif:
      return ["--tif", self._debug_tif]
    return []

  def _get_debug_irpre_option(self) -> list[str]:
    if self._debug_irpre:
      return ["--irpre", str(self._debug_irpre)]
    return []

  def _get_debug_drpre_option(self) -> list[str]:
    if self._debug_drpre:
      return ["--drpre", str(self._debug_drpre)]
    return []
