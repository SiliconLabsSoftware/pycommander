from pycommander_core.adapter_base import AdapterBase
from pycommander_core.target import Target

from .commander import Commander

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

    if commander is None:
      if not (serial_number or ip_address or serial_port):
        raise ValueError("Either serial_number, ip_address, or serial_port must be provided")

      commander = Commander(
        serial_number=serial_number,
        ip_address=ip_address,
        serial_port=serial_port,
        debug_speed=debug_speed,
        debug_tif=debug_tif,
        debug_irpre=debug_irpre,
        debug_drpre=debug_drpre,
      )

    if not target_device:
      raise ValueError("target_device must be provided")

    target = Target(part_number=target_device, commander=commander)

    super().__init__(commander=commander, target=target)
