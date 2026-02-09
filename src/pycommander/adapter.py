from .commander import Commander
from .device import Device

  def __init__(self,
               serial_number: str | None = None,
               ip_address:    str | None = None,
               serial_port:   str | None = None,
               target_device: str | None = None,
               debug_speed:   int | None = None,
               debug_tif:     str | None = None,
               debug_irpre:   int | None = None,
               debug_drpre:   int | None = None):

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

