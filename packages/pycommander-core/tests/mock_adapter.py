from pycommander_core.adapter_base import AdapterBase
from pycommander_core.device import Device

from .mock_commander import MockCommander

class MockAdapter(AdapterBase):
  def __init__(self,
               serial_number: str           | None = None,
               ip_address:    str           | None = None,
               serial_port:   str           | None = None,
               target_device: str           | None = None,
               debug_speed:   int           | None = None,
               debug_tif:     str           | None = None,
               debug_irpre:   int           | None = None,
               debug_drpre:   int           | None = None,
               commander:     MockCommander | None = None):

    if commander is None:
      if not (serial_number or ip_address or serial_port):
        raise ValueError("Either serial_number, ip_address, or serial_port must be provided")

      commander = MockCommander(
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

    target = Device(part_number=target_device, commander=commander)

    super().__init__(commander=commander, target=target)
