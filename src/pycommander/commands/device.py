from pycommander.commands._base import BaseCommand

class DeviceCommand(BaseCommand):

  def _get_general_args(self) -> list[str]:
    args = []
    args += self._get_adapter_connection_args()
    args += self._get_device_args()
    args += self._get_debug_args()
    args += self._get_flags()
    return args

  def info(self) -> dict:
    return self._run("device", "info", *self._get_general_args()).output

  def lock(self) -> dict:
    return self._run("device", "lock", *self._get_general_args()).output

  def unlock(self) -> dict:
    return self._run("device", "unlock", *self._get_general_args()).output

  def masserase(self) -> dict:
    return self._run("device", "masserase", *self._get_general_args()).output

  def pageerase(self, ranges: list[tuple[int, int]] = [], regions: list[str] = []) -> dict:
    args = []
    args += self._get_ranges(ranges)
    args += self._get_regions(regions)
    args += self._get_general_args()

    return self._run("device", "pageerase", *args).output

  def protect(self,
              read: bool = False,
              write: bool = False,
              disable: bool = False,
              ranges: list[tuple[int, int]] = [],
              regions: list[str] = []) -> dict:
    args = []
    if read:
      args += ["--read"]
    if write:
      args += ["--write"]
    if disable:
      args += ["--disable"]

    args += self._get_ranges(ranges)
    args += self._get_regions(regions)
    args += self._get_general_args()

    return self._run("device", "protect", *args).output

  def recover(self) -> dict:
    args = []
    args += self._get_adapter_connection_args()
    args += self._get_device_args()
    args += self._get_flags()

    args += self.__get_debug_speed_option()

    return self._run("device", "recover", *self._get_general_args()).output

  def reset(self) -> dict:
    args = []
    args += self._get_adapter_connection_args()
    args += self._get_device_args()
    args += self._get_flags()

    return self._run("device", "reset", *args).output

  def zwave_qrcode(self, timeout_ms: int = 0) -> dict:
    args = []
    args += self._get_general_args()
    args += ["--timeout", str(timeout_ms)]

    return self._run("device", "zwave-qrcode", *args).output
