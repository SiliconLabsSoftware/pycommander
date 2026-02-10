"""mfg917 commands: provision SiWx91x manufacturing data (dpdtraining, dump, erase, etc.)."""

from typing import Any

from pycommander_core.commands._base import BaseCommand


class Mfg917Command(BaseCommand):
  """Provision manufacturing data to the device (SiWx91x)."""

  def _get_general_args(self, **kwargs: Any) -> list[str]:
    args = []
    args += self._get_adapter_connection_args()
    args += self._get_debug_args()
    args += self._get_kwargs(**kwargs)
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
                  vmcu18: bool = False,
                  **kwargs: Any) -> dict:
    """Run DPD (Digital Pre-Distortion) training.

    Args:
      serialport (str): Serial port.
      baudrate (int): Baud rate.
      serialinterface (bool): Use serial interface.
      closeinterface (bool): Close interface after.
      host (str): Host address.
      skipinit (bool): Skip initialization.
      pinset (int): Pin set.
      storeinflash (bool): Store result in flash.
      storeinefuse (bool): Store result in eFuse.
      prompt (bool): Show confirmation prompt.
      vmcu18 (bool): VMCU 1.8V option.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
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
           pinset: int | None = None,
           **kwargs: Any) -> dict:
    """Dump device data to file.

    Args:
      filename (str): Output file path.
      serialport (str): Serial port.
      baudrate (int): Baud rate.
      serialinterface (bool): Use serial interface.
      closeinterface (bool): Close interface after.
      host (str): Host address.
      skipinit (bool): Skip initialization.
      pinset (int): Pin set.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
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
            position: int | None = None,
            **kwargs: Any) -> dict:
    """Erase a region (or list regions with list_regions=True).

    Args:
      region (str): Region name to erase.
      serialport (str): Serial port.
      baudrate (int): Baud rate.
      serialinterface (bool): Use serial interface.
      closeinterface (bool): Close interface after.
      host (str): Host address.
      skipinit (bool): Skip initialization.
      pinset (int): Pin set.
      list_regions (bool): List available regions instead of erasing.
      range (tuple[int,int]): Memory range.
      position (int): Position for erase.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
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
                off4: int | None = None,
                **kwargs: Any) -> dict:
    """EVM offset calibration (off0-off4 for antenna offsets).

    Args:
      serialport (str): Serial port.
      baudrate (int): Baud rate.
      serialinterface (bool): Use serial interface.
      closeinterface (bool): Close interface after.
      host (str): Host address.
      skipinit (bool): Skip initialization.
      pinset (int): Pin set.
      storeinflash (bool): Store in flash.
      storeinefuse (bool): Store in eFuse.
      prompt (bool): Show confirmation prompt.
      internalant (bool): Internal antenna.
      off0 (int): Offset 0.
      off1 (int): Offset 1.
      off2 (int): Offset 2.
      off3 (int): Offset 3.
      off4 (int): Offset 4.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
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
                pinset: int | None = None,
                **kwargs: Any) -> dict:
    """Upgrade device firmware.

    Args:
      filename (str): Firmware file path.
      serialport (str): Serial port.
      baudrate (int): Baud rate.
      serialinterface (bool): Use serial interface.
      closeinterface (bool): Close interface after.
      host (str): Host address.
      skipinit (bool): Skip initialization.
      pinset (int): Pin set.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
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
           vmcu18: bool = False,
           **kwargs: Any) -> dict:
    """Gain calibration (per-channel: ch1, ch6, ch11, ch14).

    Args:
      serialport (str): Serial port.
      baudrate (int): Baud rate.
      serialinterface (bool): Use serial interface.
      closeinterface (bool): Close interface after.
      host (str): Host address.
      skipinit (bool): Skip initialization.
      pinset (int): Pin set.
      storeinflash (bool): Store in flash.
      storeinefuse (bool): Store in eFuse.
      prompt (bool): Show confirmation prompt.
      ch1 (int): Channel 1 gain.
      ch6 (int): Channel 6 gain.
      ch11 (int): Channel 11 gain.
      ch14 (int): Channel 14 gain.
      vmcu18 (bool): VMCU 1.8V option.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
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
           pinset: int | None = None,
           **kwargs: Any) -> dict:
    """Show device info.

    Args:
      serialport (str): Serial port.
      baudrate (int): Baud rate.
      serialinterface (bool): Use serial interface.
      closeinterface (bool): Close interface after.
      host (str): Host address.
      skipinit (bool): Skip initialization.
      pinset (int): Pin set.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
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
           data: str | None = None,
           **kwargs: Any) -> dict:
    """Initialize device (MBR/data files).

    Args:
      serialport (str): Serial port.
      baudrate (int): Baud rate.
      serialinterface (bool): Use serial interface.
      closeinterface (bool): Close interface after.
      host (str): Host address.
      skipinit (bool): Skip initialization.
      pinset (int): Pin set.
      mbr (str): MBR file path.
      data (str): Data file path.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
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
                    prompt: bool = True,
                    **kwargs: Any) -> dict:
    """Protect config (symmetric/private key, SHA).

    Args:
      protection (str): Protection type/level.
      serialport (str): Serial port.
      baudrate (int): Baud rate.
      serialinterface (bool): Use serial interface.
      closeinterface (bool): Close interface after.
      host (str): Host address.
      skipinit (bool): Skip initialization.
      pinset (int): Pin set.
      symmetrickey (str): Symmetric key file.
      privatekey (str): Private key file.
      protectlength (int): Protection length.
      sha (str): SHA algorithm.
      prompt (bool): Show confirmation prompt.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
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
                listprofiles: bool = False,
                **kwargs: Any) -> dict:
    """Provision device (MBR, keys, data, profile).

    Args:
      serialport (str): Serial port.
      baudrate (int): Baud rate.
      serialinterface (bool): Use serial interface.
      closeinterface (bool): Close interface after.
      host (str): Host address.
      skipinit (bool): Skip initialization.
      pinset (int): Pin set.
      mbr (str): MBR file path.
      keys (str): Keys file path.
      data (str): Data file path.
      profile (str): Profile name.
      listprofiles (bool): List available profiles.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
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
                      prompt: bool = True,
                      **kwargs: Any) -> dict:
    """Provision OTP keys (symmetric/public key).

    Args:
      serialport (str): Serial port.
      baudrate (int): Baud rate.
      serialinterface (bool): Use serial interface.
      closeinterface (bool): Close interface after.
      host (str): Host address.
      skipinit (bool): Skip initialization.
      pinset (int): Pin set.
      symmetrickey (str): Symmetric key file.
      publickey (str): Public key file.
      prompt (bool): Show confirmation prompt.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
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
            vmcu18: bool = False,
            **kwargs: Any) -> dict:
    """Radio test/calibration (channel, power, phy; start/stop/burst).

    Args:
      serialport (str): Serial port.
      baudrate (int): Baud rate.
      serialinterface (bool): Use serial interface.
      closeinterface (bool): Close interface after.
      host (str): Host address.
      skipinit (bool): Skip initialization.
      pinset (int): Pin set.
      channel (int): Radio channel.
      power (int): Power level.
      phy (str): PHY type.
      burst (bool): Burst mode.
      start (bool): Start radio.
      stop (bool): Stop radio.
      internalant (bool): Internal antenna.
      vmcu18 (bool): VMCU 1.8V option.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
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
           property_field: str | None = None,
           **kwargs: Any) -> dict:
    """Read region (or list regions; optional range/position/outfile/property).

    Args:
      region (str): Region name to read.
      serialport (str): Serial port.
      baudrate (int): Baud rate.
      serialinterface (bool): Use serial interface.
      closeinterface (bool): Close interface after.
      host (str): Host address.
      skipinit (bool): Skip initialization.
      pinset (int): Pin set.
      list_regions (bool): List available regions.
      range (tuple[int,int]): Memory range.
      position (int): Position.
      outfile (str): Output file path.
      property_field (str): Property name.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
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
                     pinset: int | None = None,
                     **kwargs: Any) -> dict:
    """Setup serial/network interface for mfg917.

    Args:
      serialport (str): Serial port.
      baudrate (int): Baud rate.
      serialinterface (bool): Use serial interface.
      closeinterface (bool): Close interface after.
      host (str): Host address.
      skipinit (bool): Skip initialization.
      pinset (int): Pin set.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
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
            prompt: bool = True,
            **kwargs: Any) -> dict:
    """Write to region (address, position, data; optional crc/prompt).

    Args:
      region (str): Region name to write.
      serialport (str): Serial port.
      baudrate (int): Baud rate.
      serialinterface (bool): Use serial interface.
      closeinterface (bool): Close interface after.
      host (str): Host address.
      skipinit (bool): Skip initialization.
      pinset (int): Pin set.
      list_regions (bool): List available regions.
      address (int): Address.
      position (int): Position.
      data (str): Data file path.
      crc (bool): Verify CRC.
      prompt (bool): Show confirmation prompt.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
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
            internalant: bool = False,
            **kwargs: Any) -> dict:
    """XO (crystal) calibration (offset, ctune; store in flash/eFuse).

    Args:
      serialport (str): Serial port.
      baudrate (int): Baud rate.
      serialinterface (bool): Use serial interface.
      closeinterface (bool): Close interface after.
      host (str): Host address.
      skipinit (bool): Skip initialization.
      pinset (int): Pin set.
      storeinflash (bool): Store in flash.
      storeinefuse (bool): Store in eFuse.
      offset_khz (int): Frequency offset in kHz.
      ctuneoverride (str): CTUNE override value.
      prompt (bool): Show confirmation prompt.
      internalant (bool): Internal antenna.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
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
