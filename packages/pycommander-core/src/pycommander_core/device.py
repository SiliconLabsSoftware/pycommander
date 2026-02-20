import tempfile
import yaml

from pathlib import Path

from .commander_base import CommanderBase
from .types import *

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

  def pageerase(self, ranges: list[tuple[int | str, int | str]] = [], regions: list[str] = []) -> bool:
    """Erase selected flash pages.
    Args:
      ranges (list[tuple[int | str, int | str]]): Memory ranges to erase (start, end); extended to page boundaries.
      regions (list[str]): Named memory regions (@region).
    Returns:
      True if the page erase was successful, False otherwise.
    """
    result = self._commander.device.pageerase(ranges=ranges, regions=regions, device=self.part_number)
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

  def flashApplication(self,
                       filenames: list[Path],
                       address: int | None = None,
                       include_sections: list[str] = [],
                       exclude_sections: list[str] = [],
                       treat_as_binary: bool = False,
                       masserase: bool = False,
                       force: bool = False,
                       reset: bool = True,
                       halt: bool = False,
                       close: bool = True,
                       verify: bool = True) -> bool:
    """Flash a binary file (.bin, .s37, .hex, .gbl, or .rps) to the device.

    Args:
      filenames (list[Path]): The paths to the binary files to flash.
      address (int): The address to flash the binary file to. If the file is a .hex or .s37 file, the address will be ignored.
      include_sections (list[str]): The ELF sections to include in the flashing.
      exclude_sections (list[str]): The ELF sections to exclude in the flashing.
      treat_as_binary (bool): Treat the file as a flat binary file, regardless of the file extension.
      masserase (bool): Mass erase the device before flashing.
      force (bool): Whether to force the flash.
      reset (bool): Reset the device after flashing.
      halt (bool): Halt the device after flashing.
      close (bool): Close the code regions after flashing (Series 3 only).
      verify (bool): Verify the contents of the flash after flashing.

    Returns:
      True if the flashing was successful, False otherwise.
    """

    for filename in filenames:
      if not filename.exists():
        raise FileNotFoundError(f"File {filename} does not exist")

    result = self._commander.flash.flash(
      filenames=[str(filename) for filename in filenames],
      address=address,
      include_sections=include_sections,
      exclude_sections=exclude_sections,
      binary=treat_as_binary,
      force=force,
      masserase=masserase,
      reset=reset,
      halt=halt,
      close=close,
      verify=verify,
      device=self.part_number,
    )
    return result["success"]

  def flashRamCode(self,
                   filenames: list[Path],
                   address: int | None = None,
                   include_sections: list[str] = [],
                   exclude_sections: list[str] = [],
                   vtor: int | None = None,
                   force: bool = False,
                   halt: bool = False) -> bool:
    """Flash RAM code to the device.
    Args:
      filenames (list[Path]): The paths to the binary files to flash.
      address (int): The address to flash the binary file to. If the file is a .hex or .s37 file, the address will be ignored.
      include_sections (list[str]): The ELF sections to include in the flashing.
      exclude_sections (list[str]): The ELF sections to exclude in the flashing.
      vtor (int): The vector table address to flash the binary file to. If the file is a .hex or .s37 file, the vtor will be ignored.
      force (bool): Whether to force the flash.
      halt (bool): Halt the device after flashing.
    Returns:
      True if the RAM code was flashed successfully, False otherwise.
    """
    for filename in filenames:
      if not filename.exists():
        raise FileNotFoundError(f"File {filename} does not exist")

    result = self._commander.flash.flash(
      filenames=[str(filename) for filename in filenames],
      address=address,
      include_sections=include_sections,
      exclude_sections=exclude_sections,
      vtor=vtor,
      force=force,
      reset=False,
      halt=halt,
      device=self.part_number,
    )
    return result["success"]

  def flashPatches(self,
                   patches: list[tuple[int | str, int | str, int | str | None]],
                   force: bool = False,
                   reset: bool = True,
                   halt: bool = False) -> bool:
    """Flash patches to the device.
    Args:
      patches (list[tuple[int | str, int | str, int | str | None]]): The patches to flash.
      force (bool): Whether to force the flash.
      reset (bool): Whether to reset the device after flashing.
      halt (bool): Halt the device after flashing.
    Returns:
      True if the patches were flashed successfully, False otherwise.
    """
    result = self._commander.flash.flash(
      patches=patches,
      force=force,
      reset=reset,
      halt=halt,
      device=self.part_number,
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

  def readRegionConfig(self, allow_reset: bool = True) -> RegionConfig | None:
    """Read the region configuration from the device. Series 3 only.
    Args:
      allow_reset (bool): Allow the device to be reset during the operation.
    Returns:
      A RegionConfig object containing the region configuration, or None if the region configuration could not be retrieved.
    """
    result = self._commander.security.readregionconfig(reset=allow_reset, device=self.part_number)

    if not result["success"]:
      return None

    if "regions" not in result["result"]:
      return None

    if "data_region" not in result["result"]:
      return None

    code_regions : list[CodeRegionConfig] = []
    for code_region in result["result"]["regions"]:

      raw_protection_mode = code_region["protection_mode"]

      if raw_protection_mode == "Encrypted and authenticated":
        protection_mode = CodeRegionProtectionMode.ENCRYPTED_AND_AUTHENTICATED
      elif raw_protection_mode == "Encrypted":
        protection_mode = CodeRegionProtectionMode.ENCRYPTED
      elif raw_protection_mode == "None":
        protection_mode = CodeRegionProtectionMode.NONE

      code_regions.append(CodeRegionConfig(
        index=code_region["index"],
        size_kb=code_region["size_kb"],
        protection_mode=protection_mode,
        closed=code_region["closed"],
      ))

    data_region : DataRegionConfig = DataRegionConfig(
      location=result["result"]["data_region"]["location"],
      size=result["result"]["data_region"]["size"],
    )

    region_config = RegionConfig(
      code_regions=code_regions,
      data_region=data_region,
    )

    return region_config

  def readRegionConfigToFile(self, outfile: Path, allow_reset: bool = True) -> bool:
    """Read the region configuration from the device and write it to a file. Series 3 only.
    Args:
      outfile (Path): The path to the output file.
      allow_reset (bool): Allow the device to be reset during the operation.
    Returns:
      True if the region configuration was read successfully and written to the file, False otherwise.
    """
    result = self._commander.security.readregionconfig(outfile=str(outfile), reset=allow_reset, device=self.part_number)

    return result["success"]

  def writeRegionConfig(self, config: RegionConfig, allow_reset: bool = True, force: bool = False) -> bool:
    """Write the region configuration to the device. Series 3 only.
    Args:
      config (RegionConfig): The region configuration to write.
      allow_reset (bool): Allow the device to be reset during the operation.
      force (bool): Force the region configuration to be written, even if the desired configuration is already set.
    Returns:
      True if the region configuration was written successfully, False otherwise.
    """

    config_dict = {}
    config_dict["regions"] = []
    for code_region in config.code_regions:

      # Validate the protection mode
      if code_region.protection_mode not in CodeRegionProtectionMode.__members__.values():
        raise ValueError(f"Invalid protection mode: {code_region.protection_mode}")

      code_region_dict = {
        "size_kb": code_region.size_kb,
        "protection_mode": code_region.protection_mode.value,
      }
      config_dict["regions"].append(code_region_dict)

    if not force:
      configs_are_equal = True
      # Check if the desired configuration is already set
      existing_config = self.readRegionConfig(allow_reset=allow_reset)
      if not existing_config:
        return False

      # Check if the data region is the same
      if existing_config.data_region.location != config.data_region.location:
        configs_are_equal = False

      # Check if the code regions are the same
      for existing_code_region, new_code_region in zip(existing_config.code_regions, config.code_regions):
        if existing_code_region.index != new_code_region.index:
          configs_are_equal = False
        if existing_code_region.size_kb != new_code_region.size_kb:
          configs_are_equal = False
        if existing_code_region.protection_mode != new_code_region.protection_mode:
          configs_are_equal = False
        if existing_code_region.closed != new_code_region.closed:
          configs_are_equal = False

      if configs_are_equal:
        # Don't write anything to the device, we're already set up as desired
        return True

    # Write the region configuration to a temporary YAML file, then write it to the device
    with tempfile.NamedTemporaryFile(dir=".", suffix=".yaml") as tf:
      tf.write(yaml.dump(config_dict, indent=2).encode())
      tf.flush()
      result = self._commander.security.writeregionconfig(file=str(Path(tf.name)), reset=allow_reset, device=self.part_number)
      return result["success"]

  def writeRegionConfigFromFile(self, config_file: Path, allow_reset: bool = True, force: bool = False) -> bool:
    """Write the region configuration to the device. Series 3 only.
    Args:
      config_file (Path): The path to the configuration file.
      allow_reset (bool): Allow the device to be reset during the operation.
      force (bool): Force the region configuration to be written, even if the desired configuration is already set.
    Returns:
      True if the region configuration was written successfully, False otherwise.
    """
    if not config_file.exists():
      raise FileNotFoundError(f"Configuration file {config_file} does not exist")

    # Validate the required fields are present in the provided configuration file
    with config_file.open("r") as f:
      config_dict = yaml.safe_load(f)

    if "regions" not in config_dict:
      raise ValueError("Regions are required in the configuration file")
    for region in config_dict["regions"]:
      if "size_kb" not in region:
        raise ValueError("Size KB is required in the region configuration")
      if "protection_mode" not in region:
        raise ValueError("Protection mode is required in the region configuration")
      if region["protection_mode"] not in (
        CodeRegionProtectionMode.ENCRYPTED_AND_AUTHENTICATED.value,
        CodeRegionProtectionMode.ENCRYPTED.value,
        CodeRegionProtectionMode.NONE.value):
        raise ValueError(f"Invalid protection mode: {region['protection_mode']}")
    
    if not force:
      configs_are_equal = True
      existing_config = self.readRegionConfig(allow_reset=allow_reset)
      if not existing_config:
        return False

      for existing_region, new_region in zip(existing_config.code_regions, config_dict["regions"]):
        if existing_region.size_kb != new_region["size_kb"]:
          configs_are_equal = False
        if existing_region.protection_mode.value != new_region["protection_mode"]:
          configs_are_equal = False

      if configs_are_equal:
        # Don't write anything to the device, we're already set up as desired
        return True

    # Write the region configuration to the device
    result = self._commander.security.writeregionconfig(file=str(config_file), reset=allow_reset, device=self.part_number)
    return result["success"]

  def closeCodeRegion(self, index: int, code_version: int | None = None, allow_reset: bool = True, force: bool = False) -> bool:
    """Close a code region by index. Series 3 only.
    Args:
      index (int): The index of the code region to close.
      code_version (int | None): The code version to set (32 bits unsigned integer).
      allow_reset (bool): Allow the device to be reset during the operation.
      force (bool): Force the code region to be closed, even if it is already closed.
    Returns:
      True if the code region was closed successfully, False otherwise.
    """
    if code_version is not None:
      if code_version < 0 or code_version > 0xFFFFFFFF:
        raise ValueError("Code version must be a 32 bits unsigned integer")

    # Get the current region configuration
    existing_config = self.readRegionConfig(allow_reset=allow_reset)
    if not existing_config:
      return False

    # Check if the index is valid
    if index < 0 or index >= len(existing_config.code_regions):
      raise ValueError(f"Invalid index: {index}. Valid indices are 0 to {len(existing_config.code_regions) - 1}.")

    # Check if the desired configuration is already set
    if not force:
      if existing_config.code_regions[index].closed:
        return True

    result = self._commander.security.closeregion(index=index, codeversion=code_version, reset=allow_reset, device=self.part_number)
    return result["success"]
