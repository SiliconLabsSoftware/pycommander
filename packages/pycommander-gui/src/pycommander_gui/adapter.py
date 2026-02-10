from pycommander_core.adapter_base import AdapterBase

from .commander import Commander
from .device import Device

class Adapter(AdapterBase):
  def __init__(self,
              serial_number: str       | None = None,
              ip_address:    str       | None = None,
              serial_port:   str       | None = None,
              target_device: str       | None = None,
              debug_speed:   int       | None = None,
              debug_tif:     str       | None = None,
              debug_irpre:   int       | None = None,
              debug_drpre:   int       | None = None,
              commander:     Commander | None = None):
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

    if commander is None:
      commander = Commander(
        serial_number=serial_number,
        ip_address=ip_address,
        serial_port=serial_port,
        debug_speed=debug_speed,
        debug_tif=debug_tif,
        debug_irpre=debug_irpre,
        debug_drpre=debug_drpre,
      )

    super().__init__(commander=commander, target=Device(part_number=target_device, commander=commander))
