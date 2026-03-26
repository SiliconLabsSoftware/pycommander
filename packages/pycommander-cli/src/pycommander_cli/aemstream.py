from pycommander_core.aemstream_base import AemStreamBase

from pycommander_cli.commander import Commander

class AemStream(AemStreamBase):
  """
  High-level interface for continuous AEM data captures.
  This class can be used in a context manager to simplify the handling
  of opening and closing the AemStream.

  Args:
    serial_number: Serial number of the adapter
    ip_address: IP address of the adapter
    datarate_hz: Output data rate in Hz.
    duration_s: Capture duration in seconds.
    triggerabove_ma: Trigger above this current in mA.
    triggerbelow_ma: Trigger below this current in mA.
    triggertimeout_s: Trigger timeout in seconds.
    pretrigger_ms: Pre-trigger capture duration in milliseconds.
    calibrate: Whether to run calibration before capturing data. Defaults to False.

  Examples:
    with AemStream(serial_number="123456789", datarate_hz=100, duration_s=10) as stream:
      for measurement in stream:
        print(measurement)
  """
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
