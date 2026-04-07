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

from pycommander_core.aemstream_base import AemStreamBase

from .mock_commander import MockCommander

class TestAemStreamBase(unittest.TestCase):
  def test_aemstream_base_init_serial_number(self):
    commander = MockCommander(
      serial_number="123456789",
      debug_speed=1000000,
      debug_tif="SWD",
      debug_irpre=1,
      debug_drpre=2,
    )
    aemstream = AemStreamBase(
      commander=commander,
      datarate_hz=100,
      duration_s=10,
      triggerabove_ma=1000,
      triggerbelow_ma=2000,
      triggertimeout_s=10,
      pretrigger_ms=100,
      calibrate=True,
    )
    self.assertEqual(aemstream._commander, commander)
    self.assertEqual(aemstream._runner, commander._runner)
    self.assertEqual(aemstream._process, None)
    self.assertEqual(aemstream._args, [
      "aem", "dump", 
      "--serialno", "123456789",
      "--datarate", "100",
      "--duration", "10",
      "--triggerabove", "1000",
      "--triggerbelow", "2000",
      "--triggertimeout", "10",
      "--pretrigger", "100",
      "--calibrate",
    ])

  def test_aemstream_base_init_ip_address(self):
    commander = MockCommander(
      ip_address="192.168.1.100",
      debug_speed=1000000,
      debug_tif="SWD",
      debug_irpre=1,
      debug_drpre=2,
    )
    aemstream = AemStreamBase(
      commander=commander,
      datarate_hz=100,
      duration_s=10,
      triggerabove_ma=1000,
      triggerbelow_ma=2000,
      triggertimeout_s=10,
      pretrigger_ms=100,
      calibrate=True,
    )
    self.assertEqual(aemstream._commander, commander)
    self.assertEqual(aemstream._runner, commander._runner)
    self.assertEqual(aemstream._process, None)
    self.assertEqual(aemstream._args, [
      "aem", "dump", 
      "--ip", "192.168.1.100",
      "--datarate", "100",
      "--duration", "10",
      "--triggerabove", "1000",
      "--triggerbelow", "2000",
      "--triggertimeout", "10",
      "--pretrigger", "100",
      "--calibrate",
    ])

  def test_aemstream_base_init_serial_port(self):
    commander = MockCommander(
      serial_port="/dev/tty.usbmodem141101",
      debug_speed=1000000,
      debug_tif="SWD",
      debug_irpre=1,
      debug_drpre=2,
    )
    aemstream = AemStreamBase(
      commander=commander,
      datarate_hz=100,
      duration_s=10,
      triggerabove_ma=1000,
      triggerbelow_ma=2000,
      triggertimeout_s=10,
      pretrigger_ms=100,
      calibrate=True,
    )
    self.assertEqual(aemstream._commander, commander)
    self.assertEqual(aemstream._runner, commander._runner)
    self.assertEqual(aemstream._process, None)
    self.assertEqual(aemstream._args, [
      "aem", "dump", 
      "--identifybyserialport", "/dev/tty.usbmodem141101",
      "--datarate", "100",
      "--duration", "10",
      "--triggerabove", "1000",
      "--triggerbelow", "2000",
      "--triggertimeout", "10",
      "--pretrigger", "100",
      "--calibrate",
    ])

  def test_parse_line(self):
    commander = MockCommander()
    aemstream = AemStreamBase(commander=commander)

    line = "123456789,1000,2000"
    measurement = aemstream._AemStreamBase__parse_line(line)
    self.assertEqual(measurement.timestamp_us, 123456789)
    self.assertEqual(measurement.current_ma, 1000)
    self.assertEqual(measurement.voltage_v, 2000)
    self.assertEqual(measurement.power_mw, 1000 * 2000)

  def test_parse_line_invalid(self):
    commander = MockCommander()
    aemstream = AemStreamBase(commander=commander)

    line = "123456789,1000,2000,3000"
    with self.assertRaises(ValueError):
      aemstream._AemStreamBase__parse_line(line)

  def test_open(self):
    commander = MockCommander()
    aemstream = AemStreamBase(commander=commander)

    self.assertEqual(aemstream._process, None)
    aemstream.open()
    self.assertEqual(commander._runner.logged_commands[0], ["mock", "aem", "dump"])

  def test_open_already_open(self):
    commander = MockCommander()
    aemstream = AemStreamBase(commander=commander)

    aemstream._process = 1 # Just not None
    with self.assertRaises(RuntimeError):
      aemstream.open()

  def test_close(self):
    commander = MockCommander()
    aemstream = AemStreamBase(commander=commander)

    aemstream._process = 1 # Just not None
    aemstream.close()
    self.assertEqual(aemstream._process, None)

  def test_close_not_open(self):
    commander = MockCommander()
    aemstream = AemStreamBase(commander=commander)

    # It's okay
    aemstream.close()
