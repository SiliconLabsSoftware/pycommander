from abc import ABC
from pathlib import Path

from .commander_base import CommanderBase
from .types import CtuneValue, DeviceInfo

class DeviceBase(ABC):
  def __init__(self, part_number: str, commander: CommanderBase):
    self._commander : CommanderBase = commander
    self.part_number : str = part_number


  def info(self) -> DeviceInfo | None:
    """Get information about the device.

    Returns:
      A DeviceInfo object containing the information about the device, or None if the information could not be retrieved.
    """

    result : dict = self._commander.device.info(target_device=self.part_number)
    if not result["success"]:
      return None

    if "device_info" not in result["result"]:
      return None

    device_info = DeviceInfo(
      part_number=result["result"]["device_info"].get("part_number", None),
      die_revision=result["result"]["device_info"].get("die_revision", None),
      production_version=result["result"]["device_info"].get("production_version", None),
      flash_size_kb=result["result"]["device_info"].get("flash_size_kb", None),
      sram_size_kb=result["result"]["device_info"].get("sram_size_kb", None),
      unique_id=result["result"]["device_info"].get("unique_id", None),
    )

    return device_info


  def flash(self, filenames: list[Path], address: int | None = None, treat_as_binary: bool = False, force: bool = False) -> bool:
    """Flash a binary file (.bin, .s37, .hex, .gbl, or .rps) to the device.

    Args:
      filenames (list[Path]): The paths to the binary files to flash.
      address (int): The address to flash the binary file to. If the file is a .hex or .s37 file, the address will be ignored.
      treat_as_binary (bool): Treat the file as a flat binary file, regardless of the file extension.
      force (bool): Whether to force the flash.

    Returns:
      True if the flashing was successful, False otherwise.
    """

    for filename in filenames:
      if not filename.exists():
        raise FileNotFoundError(f"File {filename} does not exist")

    result = self._commander.flash.flash(
      filenames=[str(filename) for filename in filenames],
      target_device=self.part_number,
      force=force
    )

    return result["success"]


  def getCTUNE(self) -> CtuneValue | None:
    """Get the CTUNE values from the DI, board and token on the device.

    Returns:
      A CtuneValue object containing the CTUNE values from the DI, board and token, or None if the CTUNE values could not be retrieved.
    """

    result : dict = self._commander.ctune.get(device=self.part_number)
    if not result["success"]:
      return None

    val = CtuneValue()
    board_setting : dict = result["result"]["ctune"]["board"]
    if board_setting["status_str"] == "OK" and board_setting["valid"]:
      val.board = int(board_setting["value"])
    else:
      val.board = None

    di_setting : dict = result["result"]["ctune"]["di"]
    if di_setting["status_str"] == "OK" and di_setting["valid"]:
      val.di = int(di_setting["value"])
    else:
      val.di = None

    token_setting : dict = result["result"]["ctune"]["token"]
    if token_setting["status_str"] == "OK" and token_setting["valid"]:
      val.token = int(token_setting["value"])
    else:
      val.token = None

    return val


  def setCTUNE(self, value: int | None = None, force: bool = False) -> bool:
    """Set the value to the CTUNE token on the device.

    Args:
      value (int): The value to assign to the CTUNE token. If None, the CTUNE value will be set from the value stored in the board EEPROM.
      force (bool): Force the CTUNE value to be set, even if the desired value is already configured.

    Returns:
      True if the CTUNE value was set successfully, False otherwise.
    """

    existing_ctune : CtuneValue | None = self.getCTUNE()
    if not force and existing_ctune is None:
      return False

    if value is None:
      # Autoset the CTUNE token value from the board value
      if not force and existing_ctune.token == existing_ctune.board:
        # Desired value is already set, so get out early
        return True

      result = self._commander.ctune.autoset(device=self.part_number)
    else:
      # Set the CTUNE token value
      if not force and existing_ctune.token == value:
        # Desired value is already set, so get out early
        return True

      result = self._commander.ctune.set(f"0x{value:08X}", device=self.part_number)

    return result["success"]
