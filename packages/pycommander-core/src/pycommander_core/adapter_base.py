from abc import ABC

from .commander_base import CommanderBase
from .device_base import DeviceBase

from .types import AdapterBoardInfo, AdapterFwInfo, AdapterInfo

class AdapterBase(ABC):
  def __init__(self, commander: CommanderBase, target: DeviceBase):
    self._commander : CommanderBase = commander
    self.target : DeviceBase = target


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
