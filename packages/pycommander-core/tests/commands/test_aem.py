import unittest

from ..mock_commander import MockCommander


class TestAem(unittest.TestCase):
  def test_aem_calibrate_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.aem.calibrate()
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "aem", "calibrate", "--serialno", "123456789", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_aem_dump_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.aem.dump("out.csv", 10.0)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "aem", "dump", "--serialno", "123456789", "--outfile", "out.csv", "--duration", "10.0", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_aem_dump_command_with_options(self):
    commander = MockCommander(serial_number="123456789")
    commander.aem.dump(
      "out.csv", 5.0,
      datarate_hz=100,
      triggerabove_ma=50.0,
      triggerbelow_ma=10.0,
      triggertimeout_s=2.0,
      pretrigger_ms=100,
      header=False,
      calibrate=True,
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "aem", "dump",
      "--serialno", "123456789",
      "--outfile", "out.csv", "--duration", "5.0",
      "--datarate", "100", "--triggerabove", "50.0", "--triggerbelow", "10.0",
      "--triggertimeout", "2.0", "--pretrigger", "100",
      "--noheader", "--calibrate",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_aem_measure_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.aem.measure()
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "aem", "measure", "--serialno", "123456789", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_aem_measure_command_with_options(self):
    commander = MockCommander(serial_number="123456789")
    commander.aem.measure(windowlength_ms=200, calibrate=True)
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "aem", "measure", "--serialno", "123456789", "--windowlength", "200", "--calibrate", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_aem_analyze_command(self):
    commander = MockCommander(serial_number="123456789")
    commander.aem.analyze()
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "aem", "analyze", "--serialno", "123456789", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_aem_analyze_command_with_options(self):
    commander = MockCommander(serial_number="123456789")
    commander.aem.analyze(file="data.csv", windowlength_ms=200, get_distribution=True, cluster=True, cluster_filename="clusters.csv", find_period=True, device="EFR32MG24")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "aem", "analyze", "--serialno", "123456789", "--device", "EFR32MG24", "--file", "data.csv", "--windowlength", "200", "--showdistribution", "--cluster", "--clusterfile", "clusters.csv", "--findperiod", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)