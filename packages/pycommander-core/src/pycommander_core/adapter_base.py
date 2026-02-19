from .commander_base import CommanderBase
from .device import Device

from .types import AdapterBoardInfo, AdapterFwInfo, AdapterInfo, AdapterVoltageInfo

class AdapterBase:
  def __init__(self,
              serial_number: str       | None = None,
              ip_address: str          | None = None,
              serial_port: str         | None = None,
              target_device: str       | None = None,
              debug_speed: int         | None = None,
              debug_tif: str           | None = None,
              debug_irpre: int         | None = None,
              debug_drpre: int         | None = None,
              target: Device           | None = None,
              commander: CommanderBase | None = None):

    if commander is None:
      raise ValueError("commander must be provided")

    if target is None:
      raise ValueError("target must be provided")

    self._commander : CommanderBase = commander
    self.target : Device = target

  def info(self) -> AdapterInfo | None:
    """Get information about the adapter.

    Returns:
      An AdapterInfo object containing the information about the adapter, or None if the information could not be retrieved.
    """

    result : dict = self._commander.adapter.probe()

    if not result["success"]:
      return None

    if "board_lists" not in result["result"]:
      return None

    board_list : list[AdapterBoardInfo] = []
    for board in result["result"]["board_lists"]:
      board_list.append(AdapterBoardInfo(
        name=board.get("name", None),
        part_number=board.get("part_number", None),
        serial_number=board.get("serial_number", None),
        target_device=board.get("target_device", None),
      ))

    if "firmware_info" not in result["result"]:
      return None

    fw_info = AdapterFwInfo(
      current_version=result["result"]["firmware_info"].get("fw_version", None),
      latest_version=result["result"]["firmware_info"].get("new_fw_version", None),
      upgrade_available=result["result"]["firmware_info"].get("upgrade_available", None),
    )

    if "kit_info" not in result["result"]:
      return None

    adapter_info = AdapterInfo(
      board_list=board_list,
      fw_info=fw_info,
      jlink_serial_number=result["result"]["kit_info"].get("j_link_serial", None),
      vcom_port=result["result"]["kit_info"].get("vcom_port", None),
      vcom_supported=result["result"]["kit_info"].get("vcom_supported", None),
      ip_supported=result["result"]["kit_info"].get("ip_supported", None),
      ip_address=result["result"]["kit_info"].get("ip_address", None),
      mac_address=result["result"]["kit_info"].get("mac_address", None),
      kit_name=result["result"]["kit_info"].get("kit_name", None),
      kit_part_number=result["result"]["kit_info"].get("kit_part_number", None),
      aem_supported=result["result"]["kit_info"].get("aem_supported", None),
      debug_mode=result["result"]["kit_info"].get("debug_mode", None),
      debug_part=result["result"]["kit_info"].get("debug_part", None),
    )

    return adapter_info

  def reset(self) -> bool:
    """Reset the adapter.
    Returns:
      True if the adapter was reset successfully, False otherwise.
    """
    result : dict = self._commander.adapter.reset()
    return result["success"]

  def getVoltage(self) -> dict[int, AdapterVoltageInfo] | None:
    """Get the voltage for the target device.
    Returns:
      A dictionary of rail indices and AdapterVoltageInfo objects containing the voltage 
      information for each rail, or None if the voltage information could not be retrieved. 
      If no voltage information is available for a rail, the rail index will not be present in the dictionary.
    """
    result : dict = self._commander.adapter.voltage()

    if not result["success"]:
      return None

    voltage_info_dict : dict[int, AdapterVoltageInfo] = {}
    for voltage_info in result["result"]["voltages"]:
      rail_index = voltage_info.get("rail_index", None)
      if rail_index is None:
        continue
      voltage_info_dict[rail_index] = AdapterVoltageInfo(
        configured_voltage_v=voltage_info.get("configured_voltage_v", None),
        measured_voltage_v=voltage_info.get("measured_voltage_v", None),
        rail_powered=voltage_info.get("rail_powered", None),
      )

    return voltage_info_dict

  def setVoltage(self, voltage: float, calibrate: bool = True) -> bool:
    """Set the voltage for the target device.
    Args:
      voltage (float): Voltage to set.
      calibrate (bool): If True, automatically calibrate if voltage has changed.
    Returns:
      True if the voltage was set successfully, False otherwise.
    """
    result : dict = self._commander.adapter.voltage(voltage=voltage, calibrate=calibrate)
    return result["success"]
