"""
License
Copyright 2026 Silicon Laboratories Inc. www.silabs.com
*******************************************************************************
The licensor of this software is Silicon Laboratories Inc. Your use of this
software is governed by the terms of Silicon Labs Master Software License
Agreement (MSLA) available at
www.silabs.com/about-us/legal/master-software-license-agreement. This
software is distributed to you in Source Code format and is governed by the
sections of the MSLA applicable to Source Code.
*******************************************************************************
"""

import unittest

from ..mock_commander import MockCommander


def _serial_all(serialno: str = "123456789"):
  return [
    "--serialno", serialno,
    "--serialport", "COM1", "--baudrate", "115200",
    "--serialinterface", "--closeinterface", "--host", "192.168.1.1", "--skipinit", "--pinset", "1",
  ]


class TestMfg917(unittest.TestCase):
  def test_mfg917_dpdtraining_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.mfg917.dpdtraining(
      serialport="COM1",
      baudrate=115200,
      serialinterface=True,
      closeinterface=True,
      host="192.168.1.1",
      skipinit=True,
      pinset=1,
      storeinflash=True,
      storeinefuse=True,
      prompt=False,
      vmcu18=True,
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "mfg917", "dpdtraining",
    ] + _serial_all() + [
      "--storeinflash", "--storeinefuse", "--noprompt", "--vmcu18",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_mfg917_dump_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.mfg917.dump(
      "out.bin",
      serialport="COM1",
      baudrate=115200,
      serialinterface=True,
      closeinterface=True,
      host="192.168.1.1",
      skipinit=True,
      pinset=1,
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "mfg917", "dump", "out.bin"] + _serial_all() + ["--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_mfg917_erase_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.mfg917.erase(
      "region1",
      serialport="COM1",
      baudrate=115200,
      serialinterface=True,
      closeinterface=True,
      host="192.168.1.1",
      skipinit=True,
      pinset=1,
      list_regions=True,
      range=(0x0, 0x1000),
      position=0,
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "mfg917", "erase", "region1",
    ] + _serial_all() + [
      "--list", "--range", "0x00000000:0x00001000", "--position", "0",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_mfg917_evmoffset_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.mfg917.evmoffset(
      serialport="COM1",
      baudrate=115200,
      serialinterface=True,
      closeinterface=True,
      host="192.168.1.1",
      skipinit=True,
      pinset=1,
      storeinflash=True,
      storeinefuse=True,
      prompt=False,
      internalant=True,
      off0=1,
      off1=2,
      off2=3,
      off3=4,
      off4=5,
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "mfg917", "evmoffset",
    ] + _serial_all() + [
      "--storeinflash", "--storeinefuse", "--noprompt", "--internalant",
      "--off0", "1", "--off1", "2", "--off2", "3", "--off3", "4", "--off4", "5",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_mfg917_fwupgrade_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.mfg917.fwupgrade(
      "fw.bin",
      serialport="COM1",
      baudrate=115200,
      serialinterface=True,
      closeinterface=True,
      host="192.168.1.1",
      skipinit=True,
      pinset=1,
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "mfg917", "fwupgrade", "fw.bin"] + _serial_all() + ["--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_mfg917_gain_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.mfg917.gain(
      serialport="COM1",
      baudrate=115200,
      serialinterface=True,
      closeinterface=True,
      host="192.168.1.1",
      skipinit=True,
      pinset=1,
      storeinflash=True,
      storeinefuse=True,
      prompt=False,
      ch1=10,
      ch6=20,
      ch11=30,
      ch14=40,
      vmcu18=True,
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "mfg917", "gain",
    ] + _serial_all() + [
      "--storeinflash", "--storeinefuse", "--noprompt",
      "--ch1", "10", "--ch6", "20", "--ch11", "30", "--ch14", "40", "--vmcu18",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_mfg917_info_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.mfg917.info(
      serialport="COM1",
      baudrate=115200,
      serialinterface=True,
      closeinterface=True,
      host="192.168.1.1",
      skipinit=True,
      pinset=1,
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "mfg917", "info"] + _serial_all() + ["--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_mfg917_info_command_with_device(self):
    commander = MockCommander(serial_number="123456789")
    commander.mfg917.info(device="SiWx917")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "mfg917", "info", "--serialno", "123456789", "--device", "SiWx917", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_mfg917_init_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.mfg917.init(
      serialport="COM1",
      baudrate=115200,
      serialinterface=True,
      closeinterface=True,
      host="192.168.1.1",
      skipinit=True,
      pinset=1,
      mbr="mbr.bin",
      data="data.bin",
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "mfg917", "init",
    ] + _serial_all() + [
      "--mbr", "mbr.bin", "--data", "data.bin",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_mfg917_protectconfig_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.mfg917.protectconfig(
      "full",
      serialport="COM1",
      baudrate=115200,
      serialinterface=True,
      closeinterface=True,
      host="192.168.1.1",
      skipinit=True,
      pinset=1,
      symmetrickey="sym.key",
      privatekey="priv.pem",
      protectlength=256,
      sha="sha256",
      prompt=False,
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "mfg917", "protectconfig", "full",
    ] + _serial_all() + [
      "--symmetrickey", "sym.key", "--privatekey", "priv.pem",
      "--protectlength", "256", "--sha", "sha256", "--noprompt",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_mfg917_provision_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.mfg917.provision(
      serialport="COM1",
      baudrate=115200,
      serialinterface=True,
      closeinterface=True,
      host="192.168.1.1",
      skipinit=True,
      pinset=1,
      mbr="m.br",
      keys="k.dat",
      data="d.bin",
      profile="p1",
      listprofiles=True,
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "mfg917", "provision",
    ] + _serial_all() + [
      "--mbr", "m.br", "--keys", "k.dat", "--data", "d.bin", "--profile", "p1", "--listprofiles",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_mfg917_provisionotpkeys_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.mfg917.provisionotpkeys(
      serialport="COM1",
      baudrate=115200,
      serialinterface=True,
      closeinterface=True,
      host="192.168.1.1",
      skipinit=True,
      pinset=1,
      symmetrickey="sym.key",
      publickey="pub.pem",
      prompt=False,
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "mfg917", "provisionotpkeys",
    ] + _serial_all() + [
      "--symmetrickey", "sym.key", "--publickey", "pub.pem", "--noprompt",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_mfg917_radio_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.mfg917.radio(
      serialport="COM1",
      baudrate=115200,
      serialinterface=True,
      closeinterface=True,
      host="192.168.1.1",
      skipinit=True,
      pinset=1,
      channel=11,
      power=10,
      phy="1m",
      burst=False,
      start=True,
      stop=True,
      internalant=True,
      vmcu18=True,
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "mfg917", "radio",
    ] + _serial_all() + [
      "--channel", "11", "--power", "10", "--phy", "1m", "--noburst",
      "--start", "--stop", "--internalant", "--vmcu18",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_mfg917_read_command_all_options(self):
    commander = MockCommander(serial_number="123456789")
    commander.mfg917.read(
      "region1",
      serialport="COM1",
      baudrate=115200,
      serialinterface=True,
      closeinterface=True,
      host="192.168.1.1",
      skipinit=True,
      pinset=1,
      list_regions=True,
      range=(0x0, 0x1000),
      position=0,
      outfile="out.bin",
      property_field="prop1",
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "mfg917", "read", "region1",
    ] + _serial_all() + [
      "--list", "--range", "0x00000000:0x00001000", "--position", "0",
      "--outfile", "out.bin", "--property", "prop1",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_mfg917_setupinterface_command_all_options(self):
    commander = MockCommander(serial_number="123456789")
    commander.mfg917.setupinterface(
      serialport="COM1",
      baudrate=115200,
      serialinterface=True,
      closeinterface=True,
      host="192.168.1.1",
      skipinit=True,
      pinset=1,
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "mfg917", "setupinterface"] + _serial_all() + ["--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_mfg917_write_command_all_options(self):
    commander = MockCommander(serial_number="123456789")
    commander.mfg917.write(
      "region1",
      serialport="COM1",
      baudrate=115200,
      serialinterface=True,
      closeinterface=True,
      host="192.168.1.1",
      skipinit=True,
      pinset=1,
      list_regions=True,
      address=0x1000,
      position=1,
      data="d.bin",
      crc=False,
      prompt=False,
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "mfg917", "write", "region1",
    ] + _serial_all() + [
      "--list", "--address", "0x00001000", "--position", "1", "--data", "d.bin",
      "--nocrc", "--noprompt",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_mfg917_xocal_command_all_options(self):
    commander = MockCommander(serial_number="123456789")
    commander.mfg917.xocal(
      serialport="COM1",
      baudrate=115200,
      serialinterface=True,
      closeinterface=True,
      host="192.168.1.1",
      skipinit=True,
      pinset=1,
      storeinflash=True,
      storeinefuse=True,
      offset_khz=100,
      ctuneoverride="0x1234",
      prompt=False,
      internalant=True,
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "mfg917", "xocal",
    ] + _serial_all() + [
      "--storeinflash", "--storeinefuse", "--offset", "100", "--ctuneoverride", "0x1234",
      "--noprompt", "--internalant",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)
