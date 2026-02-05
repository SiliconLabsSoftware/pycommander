from pycommander.commands._base import BaseCommand

class Mfg917Command(BaseCommand):

  def _get_general_args(self) -> list[str]:
    args = []
    args += self._get_adapter_connection_args()
    args += self._get_device_args()
    args += self._get_debug_args()
    args += self._get_flags()
    return args

  def _get_mfg917_serial_args(self,
                              serialport: str | None = None,
                              baudrate: int | None = None,
                              serialinterface: bool = False,
                              closeinterface: bool = False,
                              host: str | None = None,
                              skipinit: bool = False,
                              pinset: int | None = None) -> list[str]:
    args = []
    if serialport is not None:
      args += ["--serialport", serialport]
    if baudrate is not None:
      args += ["--baudrate", str(baudrate)]
    if serialinterface:
      args += ["--serialinterface"]
    if closeinterface:
      args += ["--closeinterface"]
    if host is not None:
      args += ["--host", host]
    if skipinit:
      args += ["--skipinit"]
    if pinset is not None:
      args += ["--pinset", str(pinset)]
    return args

  def dpdtraining(self,
                  serialport: str | None = None,
                  baudrate: int | None = None,
                  serialinterface: bool = False,
                  closeinterface: bool = False,
                  host: str | None = None,
                  skipinit: bool = False,
                  pinset: int | None = None,
                  storeinflash: bool = False,
                  storeinefuse: bool = False,
                  prompt: bool = True,
                  vmcu18: bool = False) -> dict:
    args = self._get_general_args()
    args += self._get_mfg917_serial_args(serialport, baudrate, serialinterface, closeinterface, host, skipinit, pinset)
    if storeinflash:
      args += ["--storeinflash"]
    if storeinefuse:
      args += ["--storeinefuse"]
    if not prompt:
      args += ["--noprompt"]
    if vmcu18:
      args += ["--vmcu18"]
    return self._run("mfg917", "dpdtraining", *args).output

  def dump(self,
           filename: str,
           serialport: str | None = None,
           baudrate: int | None = None,
           serialinterface: bool = False,
           closeinterface: bool = False,
           host: str | None = None,
           skipinit: bool = False,
           pinset: int | None = None) -> dict:
    args = self._get_general_args()
    args += self._get_mfg917_serial_args(serialport, baudrate, serialinterface, closeinterface, host, skipinit, pinset)
    return self._run("mfg917", "dump", filename, *args).output

  def erase(self,
            region: str,
            serialport: str | None = None,
            baudrate: int | None = None,
            serialinterface: bool = False,
            closeinterface: bool = False,
            host: str | None = None,
            skipinit: bool = False,
            pinset: int | None = None,
            list_regions: bool = False,
            range: tuple[int, int] | None = None,
            position: int | None = None) -> dict:
    args = self._get_general_args()
    args += self._get_mfg917_serial_args(serialport, baudrate, serialinterface, closeinterface, host, skipinit, pinset)
    if list_regions:
      args += ["--list"]
    if range is not None:
      args += self._get_ranges([range])
    if position is not None:
      args += ["--position", str(position)]
    return self._run("mfg917", "erase", region, *args).output

  def evmoffset(self,
                serialport: str | None = None,
                baudrate: int | None = None,
                serialinterface: bool = False,
                closeinterface: bool = False,
                host: str | None = None,
                skipinit: bool = False,
                pinset: int | None = None,
                storeinflash: bool = False,
                storeinefuse: bool = False,
                prompt: bool = True,
                internalant: bool = False,
                off0: int | None = None,
                off1: int | None = None,
                off2: int | None = None,
                off3: int | None = None,
                off4: int | None = None) -> dict:
    args = self._get_general_args()
    args += self._get_mfg917_serial_args(serialport, baudrate, serialinterface, closeinterface, host, skipinit, pinset)
    if storeinflash:
      args += ["--storeinflash"]
    if storeinefuse:
      args += ["--storeinefuse"]
    if not prompt:
      args += ["--noprompt"]
    if internalant:
      args += ["--internalant"]
    if off0 is not None:
      args += ["--off0", str(off0)]
    if off1 is not None:
      args += ["--off1", str(off1)]
    if off2 is not None:
      args += ["--off2", str(off2)]
    if off3 is not None:
      args += ["--off3", str(off3)]
    if off4 is not None:
      args += ["--off4", str(off4)]
    return self._run("mfg917", "evmoffset", *args).output

  def fwupgrade(self,
                filename: str,
                serialport: str | None = None,
                baudrate: int | None = None,
                serialinterface: bool = False,
                closeinterface: bool = False,
                host: str | None = None,
                skipinit: bool = False,
                pinset: int | None = None) -> dict:
    args = self._get_general_args()
    args += self._get_mfg917_serial_args(serialport, baudrate, serialinterface, closeinterface, host, skipinit, pinset)
    return self._run("mfg917", "fwupgrade", filename, *args).output

  def gain(self,
           serialport: str | None = None,
           baudrate: int | None = None,
           serialinterface: bool = False,
           closeinterface: bool = False,
           host: str | None = None,
           skipinit: bool = False,
           pinset: int | None = None,
           storeinflash: bool = False,
           storeinefuse: bool = False,
           prompt: bool = True,
           ch1: int | None = None,
           ch6: int | None = None,
           ch11: int | None = None,
           ch14: int | None = None,
           vmcu18: bool = False) -> dict:
    args = self._get_general_args()
    args += self._get_mfg917_serial_args(serialport, baudrate, serialinterface, closeinterface, host, skipinit, pinset)
    if storeinflash:
      args += ["--storeinflash"]
    if storeinefuse:
      args += ["--storeinefuse"]
    if not prompt:
      args += ["--noprompt"]
    if ch1 is not None:
      args += ["--ch1", str(ch1)]
    if ch6 is not None:
      args += ["--ch6", str(ch6)]
    if ch11 is not None:
      args += ["--ch11", str(ch11)]
    if ch14 is not None:
      args += ["--ch14", str(ch14)]
    if vmcu18:
      args += ["--vmcu18"]
    return self._run("mfg917", "gain", *args).output

  def info(self,
           serialport: str | None = None,
           baudrate: int | None = None,
           serialinterface: bool = False,
           closeinterface: bool = False,
           host: str | None = None,
           skipinit: bool = False,
           pinset: int | None = None) -> dict:
    args = self._get_general_args()
    args += self._get_mfg917_serial_args(serialport, baudrate, serialinterface, closeinterface, host, skipinit, pinset)
    return self._run("mfg917", "info", *args).output

  def init(self,
           serialport: str | None = None,
           baudrate: int | None = None,
           serialinterface: bool = False,
           closeinterface: bool = False,
           host: str | None = None,
           skipinit: bool = False,
           pinset: int | None = None,
           mbr: str | None = None,
           data: str | None = None) -> dict:
    args = self._get_general_args()
    args += self._get_mfg917_serial_args(serialport, baudrate, serialinterface, closeinterface, host, skipinit, pinset)
    if mbr is not None:
      args += ["--mbr", mbr]
    if data is not None:
      args += ["--data", data]
    return self._run("mfg917", "init", *args).output

  def protectconfig(self,
                    protection: str,
                    serialport: str | None = None,
                    baudrate: int | None = None,
                    serialinterface: bool = False,
                    closeinterface: bool = False,
                    host: str | None = None,
                    skipinit: bool = False,
                    pinset: int | None = None,
                    symmetrickey: str | None = None,
                    privatekey: str | None = None,
                    protectlength: int | None = None,
                    sha: str | None = None,
                    prompt: bool = True) -> dict:
    args = self._get_general_args()
    args += self._get_mfg917_serial_args(serialport, baudrate, serialinterface, closeinterface, host, skipinit, pinset)
    if symmetrickey is not None:
      args += ["--symmetrickey", symmetrickey]
    if privatekey is not None:
      args += ["--privatekey", privatekey]
    if protectlength is not None:
      args += ["--protectlength", str(protectlength)]
    if sha is not None:
      args += ["--sha", sha]
    if not prompt:
      args += ["--noprompt"]
    return self._run("mfg917", "protectconfig", protection, *args).output

  def provision(self,
                serialport: str | None = None,
                baudrate: int | None = None,
                serialinterface: bool = False,
                closeinterface: bool = False,
                host: str | None = None,
                skipinit: bool = False,
                pinset: int | None = None,
                mbr: str | None = None,
                keys: str | None = None,
                data: str | None = None,
                profile: str | None = None,
                listprofiles: bool = False) -> dict:
    args = self._get_general_args()
    args += self._get_mfg917_serial_args(serialport, baudrate, serialinterface, closeinterface, host, skipinit, pinset)
    if mbr is not None:
      args += ["--mbr", mbr]
    if keys is not None:
      args += ["--keys", keys]
    if data is not None:
      args += ["--data", data]
    if profile is not None:
      args += ["--profile", profile]
    if listprofiles:
      args += ["--listprofiles"]
    return self._run("mfg917", "provision", *args).output

  def provisionotpkeys(self,
                      serialport: str | None = None,
                      baudrate: int | None = None,
                      serialinterface: bool = False,
                      closeinterface: bool = False,
                      host: str | None = None,
                      skipinit: bool = False,
                      pinset: int | None = None,
                      symmetrickey: str | None = None,
                      publickey: str | None = None,
                      prompt: bool = True) -> dict:
    args = self._get_general_args()
    args += self._get_mfg917_serial_args(serialport, baudrate, serialinterface, closeinterface, host, skipinit, pinset)
    if symmetrickey is not None:
      args += ["--symmetrickey", symmetrickey]
    if publickey is not None:
      args += ["--publickey", publickey]
    if not prompt:
      args += ["--noprompt"]
    return self._run("mfg917", "provisionotpkeys", *args).output

  def radio(self,
            serialport: str | None = None,
            baudrate: int | None = None,
            serialinterface: bool = False,
            closeinterface: bool = False,
            host: str | None = None,
            skipinit: bool = False,
            pinset: int | None = None,
            channel: int | None = None,
            power: int | None = None,
            phy: str | None = None,
            burst: bool = True,
            start: bool = False,
            stop: bool = False,
            internalant: bool = False,
            vmcu18: bool = False) -> dict:
    args = self._get_general_args()
    args += self._get_mfg917_serial_args(serialport, baudrate, serialinterface, closeinterface, host, skipinit, pinset)
    if channel is not None:
      args += ["--channel", str(channel)]
    if power is not None:
      args += ["--power", str(power)]
    if phy is not None:
      args += ["--phy", phy]
    if not burst:
      args += ["--noburst"]
    if start:
      args += ["--start"]
    if stop:
      args += ["--stop"]
    if internalant:
      args += ["--internalant"]
    if vmcu18:
      args += ["--vmcu18"]
    return self._run("mfg917", "radio", *args).output

  def read(self,
           region: str,
           serialport: str | None = None,
           baudrate: int | None = None,
           serialinterface: bool = False,
           closeinterface: bool = False,
           host: str | None = None,
           skipinit: bool = False,
           pinset: int | None = None,
           list_regions: bool = False,
           range: tuple[int, int] | None = None,
           position: int | None = None,
           outfile: str | None = None,
           property_field: str | None = None) -> dict:
    args = self._get_general_args()
    args += self._get_mfg917_serial_args(serialport, baudrate, serialinterface, closeinterface, host, skipinit, pinset)
    if list_regions:
      args += ["--list"]
    if range is not None:
      args += self._get_ranges([range])
    if position is not None:
      args += ["--position", str(position)]
    if outfile is not None:
      args += ["--outfile", outfile]
    if property_field is not None:
      args += ["--property", property_field]
    return self._run("mfg917", "read", region, *args).output

  def setupinterface(self,
                     serialport: str | None = None,
                     baudrate: int | None = None,
                     serialinterface: bool = False,
                     closeinterface: bool = False,
                     host: str | None = None,
                     skipinit: bool = False,
                     pinset: int | None = None) -> dict:
    args = self._get_general_args()
    args += self._get_mfg917_serial_args(serialport, baudrate, serialinterface, closeinterface, host, skipinit, pinset)
    return self._run("mfg917", "setupinterface", *args).output

  def write(self,
            region: str,
            serialport: str | None = None,
            baudrate: int | None = None,
            serialinterface: bool = False,
            closeinterface: bool = False,
            host: str | None = None,
            skipinit: bool = False,
            pinset: int | None = None,
            list_regions: bool = False,
            address: int | None = None,
            position: int | None = None,
            data: str | None = None,
            crc: bool = True,
            prompt: bool = True) -> dict:
    args = self._get_general_args()
    args += self._get_mfg917_serial_args(serialport, baudrate, serialinterface, closeinterface, host, skipinit, pinset)
    if list_regions:
      args += ["--list"]
    if address is not None:
      args += ["--address", self._get_address_string(address)]
    if position is not None:
      args += ["--position", str(position)]
    if data is not None:
      args += ["--data", data]
    if not crc:
      args += ["--nocrc"]
    if not prompt:
      args += ["--noprompt"]
    return self._run("mfg917", "write", region, *args).output

  def xocal(self,
            serialport: str | None = None,
            baudrate: int | None = None,
            serialinterface: bool = False,
            closeinterface: bool = False,
            host: str | None = None,
            skipinit: bool = False,
            pinset: int | None = None,
            storeinflash: bool = False,
            storeinefuse: bool = False,
            offset_khz: int | None = None,
            ctuneoverride: str | None = None,
            prompt: bool = True,
            internalant: bool = False) -> dict:
    args = self._get_general_args()
    args += self._get_mfg917_serial_args(serialport, baudrate, serialinterface, closeinterface, host, skipinit, pinset)
    if storeinflash:
      args += ["--storeinflash"]
    if storeinefuse:
      args += ["--storeinefuse"]
    if offset_khz is not None:
      args += ["--offset", str(offset_khz)]
    if ctuneoverride is not None:
      args += ["--ctuneoverride", ctuneoverride]
    if not prompt:
      args += ["--noprompt"]
    if internalant:
      args += ["--internalant"]
    return self._run("mfg917", "xocal", *args).output
