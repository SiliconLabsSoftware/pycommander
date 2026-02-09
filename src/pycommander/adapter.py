from .commander import Commander
from .device import Device

from .types import AdapterBoardInfo, AdapterFwInfo, AdapterInfo

class Adapter:
  def __init__(self,
               serial_number: str | None = None,
               ip_address:    str | None = None,
               serial_port:   str | None = None,
               target_device: str | None = None,
               debug_speed:   int | None = None,
               debug_tif:     str | None = None,
               debug_irpre:   int | None = None,
               debug_drpre:   int | None = None):
    """Initialize the Adapter class. Either serial_number, ip_address, or serial_port must be provided.

    Args:
      serial_number (str): The serial number of the adapter.
      ip_address (str): The IP address of the adapter.
      serial_port (str): The serial port/device file of the adapter.
      target_device (str): The target device of the adapter. Required.
      debug_speed (int): The debug speed of the adapter. Optional.
      debug_tif (str): The debug TIF of the adapter. Optional.
      debug_irpre (int): The debug IRPRE of the adapter. Optional.
      debug_drpre (int): The debug DRPRE of the adapter. Optional.
    """


    if (serial_number and ip_address) or (serial_number and serial_port) or (ip_address and serial_port):
      raise ValueError("Only one of serial_number, ip_address, or serial_port can be provided")

    if not (serial_number or ip_address or serial_port):
      raise ValueError("Either serial_number, ip_address, or serial_port must be provided")

    if not target_device:
      raise ValueError("target_device must be provided")

    self._commander : Commander = Commander(serial_number,
                                            ip_address=ip_address,
                                            serial_port=serial_port,
                                            debug_speed=debug_speed,
                                            debug_tif=debug_tif,
                                            debug_irpre=debug_irpre,
                                            debug_drpre=debug_drpre)

    self.target : Device = Device(part_number=target_device, commander=self._commander)


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
