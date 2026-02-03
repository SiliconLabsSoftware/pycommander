from pycommander.commands._base import BaseCommand

class AdapterCommand(BaseCommand):

  def _get_general_args(self) -> list[str]:
    args = []
    args += self._get_adapter_connection_args()
    args += self._get_device_args()
    args += self._get_flags()
    return args

  def dbgmode(self, mode: str | None = None) -> dict:
    args = self._get_general_args()
    mode_string = mode if mode is not None else ""
    return self._run("adapter", "dbgmode", mode_string, *args).output

  def drivermode(self, mode: str | None = None) -> dict:
    args = self._get_general_args()
    mode_string = mode if mode is not None else ""
    return self._run("adapter", "drivermode", mode_string, *args).output

  def fwupgrade(self, filename: str | None = None, nocheck: bool = False) -> dict:
    args = self._get_general_args()
    filename_string = filename if filename is not None else ""
    if nocheck:
      args += ["--nocheck"]
    return self._run("adapter", "fwupgrade", filename_string, *args).output

  def fwupgradecheck(self) -> dict:
    return self._run("adapter", "fwupgradecheck", *self._get_general_args()).output

  def ip(self,
         dhcp: bool = False,
         addr: str | None = None,
         dns: str | None = None,
         gw: str | None = None) -> dict:
    args = self._get_general_args()
    if dhcp:
      args += ["--dhcp"]
    if addr is not None:
      args += ["--addr", addr]
    if dns is not None:
      args += ["--dns", dns]
    if gw is not None:
      args += ["--gw", gw]
    return self._run("adapter", "ip", *args).output

  def list(self,
           net: bool = False,
           filter_regex: str | None = None,
           noconnect: bool = False) -> dict:
    args = self._get_general_args()
    if net:
      args += ["--net"]
    if filter_regex is not None:
      args += ["--filter", filter_regex]
    if noconnect:
      args += ["--noconnect"]    
    return self._run("adapter", "list", *args).output

  def nick(self, nickname: str | None = None, clear: bool = False) -> dict:
    args = self._get_general_args()
    nickname_string = nickname if nickname is not None else ""
    if clear:
      args += ["--clear"]
    return self._run("adapter", "nick", nickname_string, *args).output

  def power(self, state: str | None = None) -> dict:
    args = self._get_general_args()
    state_string = state if state is not None else ""
    return self._run("adapter", "power", state_string, *args).output

  def probe(self,
            fw: bool = False,
            kit: bool = False,
            boards: bool = False) -> dict:
    args = self._get_general_args()
    if fw:
      args += ["--fw"]
    if kit:
      args += ["--kit"]
    if boards:
      args += ["--boards"]
    return self._run("adapter", "probe", *args).output

  def reset(self) -> dict:
    return self._run("adapter", "reset", *self._get_general_args()).output

  def voltage(self, voltage: str | None = None, nocalibrate: bool = False) -> dict:
    args = self._get_general_args()
    voltage_string = voltage if voltage is not None else ""
    if nocalibrate:
      args += ["--nocalibrate"]
    return self._run("adapter", "voltage", voltage_string, *args).output
