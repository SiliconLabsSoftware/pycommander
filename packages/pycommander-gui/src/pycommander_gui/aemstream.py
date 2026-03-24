from pycommander_core.aemstream_base import AemStreamBase

from pycommander_gui.commander import Commander

class AemStream(AemStreamBase):
  def __init__(self,
               serial_number: str | None = None,
               ip_address: str | None = None,
               datarate_hz: int | None = None,
               duration_s: float | None = None,
               triggerabove_ma: float | None = None,
               triggerbelow_ma: float | None = None,
               triggertimeout_s: float | None = None,
               pretrigger_ms: int | None = None,
               calibrate: bool = False):

    commander = Commander(serial_number=serial_number, ip_address=ip_address)

    super().__init__(commander=commander,
                     datarate_hz=datarate_hz,
                     duration_s=duration_s,
                     triggerabove_ma=triggerabove_ma,
                     triggerbelow_ma=triggerbelow_ma,
                     triggertimeout_s=triggertimeout_s,
                     pretrigger_ms=pretrigger_ms,
                     calibrate=calibrate)
