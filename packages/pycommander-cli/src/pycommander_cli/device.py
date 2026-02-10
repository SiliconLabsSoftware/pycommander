from pycommander_core.device_base import DeviceBase

from .commander import Commander

class Device(DeviceBase):
  def __init__(self, part_number: str, commander: Commander):
    super().__init__(part_number=part_number, commander=commander)
