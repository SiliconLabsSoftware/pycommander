from pathlib import Path

from .commander_base import CommanderBase
from .types import CtuneValue, DeviceInfo

class Device:
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

  def reset(self) -> bool:
    """Reset the device.

    Returns:
      True if the reset was successful, False otherwise.
    """

    result = self._commander.device.reset(device=self.part_number)
    return result["success"]

  def masserase(self) -> bool:
    """Mass erase the device.

    Returns:
      True if the mass erase was successful, False otherwise.
    """

    result = self._commander.device.masserase(device=self.part_number)
    return result["success"]

  def writeManufacturingTokens(self,
                  tokenfiles: list[Path] = [],
                  tokens: list[tuple[str, str]] = [],
                  tokengroup: str | None = None,
                  tokendefs: Path | None = None,
                  securerange: tuple[int | str, int | str] | None = None) -> bool:
    """Write manufacturing tokens to the device. This command is only applicable to Series 1 and 2 devices.
    Args:
      tokenfiles (list[Path]): The paths to the token files to write.
      tokens (list[tuple[str, str]]): The tokens to write (TOKEN_NAME, value).
      tokengroup (str | None): The token group to write.
      tokendefs (Path | None): The path to the token definitions file.
      securerange (tuple[int | str, int | str] | None): The secure range to write the tokens to.

    Returns:
      True if the manufacturing tokens were written successfully, False otherwise.
    """
    for tokenfile in tokenfiles:
      if not tokenfile.exists():
        raise FileNotFoundError(f"Token file {tokenfile} does not exist")

    result = self._commander.tokens.write(
      tokenfiles=[str(tokenfile) for tokenfile in tokenfiles],
      tokens=tokens,
      tokengroup=tokengroup,
      tokendefs=str(tokendefs) if tokendefs is not None else None,
      securerange=securerange,
      device=self.part_number,
    )
    return result["success"]

  def writeStaticTokens(self,
                        tokenfiles: list[Path] = [],
                        tokens: list[tuple[str, str]] = [],
                        tokengroup: str | None = None,
                        tokendefs: Path | None = None,
                        securerange: tuple[int | str, int | str] | None = None) -> bool:
    """Write static tokens to the device. This command is only applicable to Series 3 devices.
    Args:
      tokenfiles (list[Path]): The paths to the token files to write.
      tokens (list[tuple[str, str]]): The tokens to write (TOKEN_NAME, value).
      tokengroup (str | None): The token group to write.
      tokendefs (Path | None): The path to the token definitions file.
      securerange (tuple[int | str, int | str] | None): The secure range to write the tokens to.

    Returns:
      True if the static tokens were written successfully, False otherwise.
    """
    return self.writeManufacturingTokens(tokenfiles, tokens, tokengroup, tokendefs, securerange)


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

  def lockDebugAccess(self) -> bool:
    """Lock the device for debug access.

    Returns:
      True if the debug lock was successful, False otherwise.
    """

    result = self._commander.device.lock(device=self.part_number)
    return result["success"]

  def unlockDebugAccess(self) -> bool:
    """Unlock the device for debug access.

    Returns:
      True if the debug unlock was successful, False otherwise.
    """

    result = self._commander.device.unlock(device=self.part_number)
    return result["success"]

  def enableWriteProtection(self, ranges: list[tuple[int | str, int | str]] = [], regions: list[str] = []) -> bool:
    """Enable write protection for the specified ranges and/or regions.

    Args:
      ranges (list[tuple[int | str, int | str]]): The ranges to write protect (start, end).
      regions (list[str]): The regions to write protect (@region).

    Returns:
      True if the write protection was successful, False otherwise.
    """

    if len(ranges) == 0 and len(regions) == 0:
      raise ValueError("At least one range or region must be specified")

    result = self._commander.device.protect(write=True, ranges=ranges, regions=regions, device=self.part_number)
    return result["success"]

  def enableReadProtection(self, ranges: list[tuple[int | str, int | str]] = [], regions: list[str] = []) -> bool:
    """Read protect the specified ranges and/or regions.

    Args:
      ranges (list[tuple[int | str, int | str]]): The ranges to read protect (start, end).
      regions (list[str]): The regions to read protect (@region).

    Returns:
      True if the read protection was successful, False otherwise.
    """

    if len(ranges) == 0 and len(regions) == 0:
      raise ValueError("At least one range or region must be specified")

    result = self._commander.device.protect(read=True, ranges=ranges, regions=regions, device=self.part_number)
    return result["success"]

  def disableWriteProtection(self) -> bool:
    """Disable write protection for the entire flash.

    Returns:
      True if the write protection was disabled successfully, False otherwise.
    """

    result = self._commander.device.protect(write=True, disable=True, device=self.part_number)
    return result["success"]

  def disableReadProtection(self) -> bool:
    """Disable read protection for the entire flash.

    Returns:
      True if the read protection was disabled successfully, False otherwise.
    """

    result = self._commander.device.protect(read=True, disable=True, device=self.part_number)
    return result["success"]
