"""AEM (Advanced Energy Monitor) commands: calibrate, dump, measure."""

from pycommander.commands._base import BaseCommand


class AemCommand(BaseCommand):
  """Advanced Energy Monitor (AEM) commands."""

  def _get_general_args(self) -> list[str]:
    args = []
    args += self._get_adapter_connection_args()
    args += self._get_device_args()
    args += self._get_flags()
    return args

  def calibrate(self) -> dict:
    """Calibrate AEM.

    Returns:
      Command output as parsed JSON (dict).
    """
    return self._run("aem", "calibrate", *self._get_general_args()).output

  def dump(self,
           outfile: str,
           duration_s: float,
           datarate_hz: int | None = None,
           triggerabove_ma: float | None = None,
           triggerbelow_ma: float | None = None,
           triggertimeout_s: float | None = None,
           pretrigger_ms: int | None = None,
           header: bool = True,
           calibrate: bool = False) -> dict:
    """Log AEM measurements as time series data to a file.

    Args:
      outfile (str): File (.csv or .txt) to store the AEM data in.
      duration_s (float): AEM data logging duration in seconds.
      datarate_hz (int): Desired AEM data logging rate in Hz.
      triggerabove_ma (float): Start logging if measured current rises above (mA).
      triggerbelow_ma (float): Start logging if measured current drops below (mA).
      triggertimeout_s (float): Timeout in seconds if not triggered.
      pretrigger_ms (int): Start logging this many ms before the trigger event.
      header (bool): If True, include column header in the output file.
      calibrate (bool): Run AEM calibration before measuring.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args()

    # Require outfile and duration, since we are not in interactive CLI mode here
    args += ["--outfile", outfile]
    args += ["--duration", str(duration_s)]

    if datarate_hz is not None:
      args += ["--datarate", str(datarate_hz)]
    if triggerabove_ma is not None:
      args += ["--triggerabove", str(triggerabove_ma)]
    if triggerbelow_ma is not None:
      args += ["--triggerbelow", str(triggerbelow_ma)]
    if triggertimeout_s is not None:
      args += ["--triggertimeout", str(triggertimeout_s)]
    if pretrigger_ms is not None:
      args += ["--pretrigger", str(pretrigger_ms)]
    if not header:
      args += ["--noheader"]
    if calibrate:
      args += ["--calibrate"]
    return self._run("aem", "dump", *args).output

  def measure(self,
              windowlength_ms: int | None = None,
              calibrate: bool = False) -> dict:
    """Measure the average current in a time window.

    Args:
      windowlength_ms (int): Duration in ms to measure and average (default 100).
      calibrate (bool): Run AEM calibration before measuring.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args()
    if windowlength_ms is not None:
      args += ["--windowlength", str(windowlength_ms)]
    if calibrate:
      args += ["--calibrate"]
    return self._run("aem", "measure", *args).output
