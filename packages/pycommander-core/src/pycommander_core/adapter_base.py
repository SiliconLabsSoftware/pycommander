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

from . import types

from .commander_base import CommanderBase
from .target import Target

class AdapterBase:
  def __init__(self,
              serial_number: str       | None = None,
              ip_address: str          | None = None,
              serial_port: str         | None = None,
              target_device: str       | None = None,
              debug_speed: int         | None = None,
              debug_tif: str           | None = None,
              debug_irpre: int         | None = None,
              debug_drpre: int         | None = None,
              target: Target           | None = None,
              commander: CommanderBase | None = None):

    if commander is None:
      raise ValueError("commander must be provided")

    self._commander : CommanderBase = commander
    self.target : Target | None = target

  def info(self) -> types.AdapterInfo | None:
    """Get information about the adapter.

    Returns:
      An AdapterInfo object containing the information about the adapter, or None if the information could not be retrieved.
    """

    result : dict = self._commander.adapter.probe()

    if not result["success"]:
      return None

    if "board_lists" not in result["result"]:
      return None

    board_list : list[types.AdapterBoardInfo] = []
    for board in result["result"]["board_lists"]:
      board_list.append(types.AdapterBoardInfo(
        name=board.get("name", None),
        part_number=board.get("part_number", None),
        serial_number=board.get("serial_number", None),
        target_device=board.get("target_device", None),
      ))

    if "firmware_info" not in result["result"]:
      return None

    fw_info = types.AdapterFwInfo(
      current_version=result["result"]["firmware_info"].get("fw_version", None),
      latest_version=result["result"]["firmware_info"].get("new_fw_version", None),
      upgrade_available=result["result"]["firmware_info"].get("upgrade_available", None),
    )

    if "kit_info" not in result["result"]:
      return None

    adapter_info = types.AdapterInfo(
      board_list=board_list,
      fw_info=fw_info,
      jlink_serial_number=result["result"]["kit_info"].get("j_link_serial", None),
      vcom_port=result["result"]["kit_info"].get("vcom_port", None),
      vcom_supported=result["result"]["kit_info"].get("vcom_supported", None),
      ip_supported=result["result"]["kit_info"].get("ip_supported", None),
      ip_address=result["result"]["kit_info"].get("ip_address", None),
      mac_address=result["result"]["kit_info"].get("mac_address", None),
      kit_name=result["result"]["kit_info"].get("kit_name", None),
      kit_part_number=result["result"]["kit_info"].get("kit_part_number", None),
      aem_supported=result["result"]["kit_info"].get("aem_supported", None),
      debug_mode=result["result"]["kit_info"].get("debug_mode", None),
      debug_part=result["result"]["kit_info"].get("debug_part", None),
    )

    return adapter_info

  def reset(self) -> bool:
    """Reset the adapter.

    Returns:
      True if the adapter was reset successfully, False otherwise.
    """
    result : dict = self._commander.adapter.reset()
    return result["success"]

  def getVoltage(self) -> types.AdapterVoltageInfo | None:
    """Get the voltage for the target device.

    Returns:
      A dictionary of rail indices and AdapterVoltageInfo objects containing the voltage 
      information for each rail, or None if the voltage information could not be retrieved. 
      If no voltage information is available for a rail, the rail index will not be present in the dictionary.
    """
    result : dict = self._commander.adapter.voltage()

    if not result["success"]:
      return None

    voltage_info : types.AdapterVoltageInfo = types.AdapterVoltageInfo(rails=[])
    for rail_info in result["result"]["voltages"]:
      voltage_info.rails.append(types.AdapterRailInfo(
        rail_index=rail_info.get("rail_index", None),
        configured_voltage_v=rail_info.get("configured_voltage_v", None),
        measured_voltage_v=rail_info.get("measured_voltage_v", None),
        rail_powered=rail_info.get("rail_powered", None),
      ))

    return voltage_info

  def setVoltage(self, voltage: float, calibrate: bool = True) -> bool:
    """Set the voltage for the target device.

    Args:
      voltage (float): Voltage to set.
      calibrate (bool): If True, automatically calibrate if voltage has changed.

    Returns:
      True if the voltage was set successfully, False otherwise.
    """
    result : dict = self._commander.adapter.voltage(voltage=voltage, calibrate=calibrate)
    return result["success"]

  def setVcomConfig(self, baudrate: int, handshake: types.VcomHandshake, store: bool = False) -> bool:
    """Set the VCOM configuration for the adapter.

    Args:
      baudrate (int): VCOM baudrate.
      handshake (VcomHandshake): VCOM handshake.
      store (bool): Store the VCOM configuration.

    Returns:
      True if the VCOM configuration was set successfully, False otherwise.
    """
    if handshake not in types.VcomHandshake.__members__.values():
      raise ValueError(f"Invalid handshake: {handshake}")

    result : dict = self._commander.vcom.config(baudrate=baudrate, handshake=handshake.value, store=store)
    return result["success"]

  def analyzeEnergyUsage(self, duration_s: float, get_distribution: bool = False, cluster_states: bool = False, detect_period: bool = False) -> types.AemAnalysisResult | None:
    """Analyze the energy usage of the target device.

    Args:
      duration_s: Duration of the measurement in seconds.
      get_distribution: If True, get the distribution of measurements.
      cluster_states: If True, cluster the states of the measurements.
      detect_period: If True, detect the period of the measurements.

    Returns:
      An AemAnalysisResult object containing the analysis results, or None if the analysis could not be performed.
    """

    if not get_distribution and not cluster_states and not detect_period:
      raise ValueError("Distribution, cluster states, and period detection cannot all be False.")

    result : dict = self._commander.aem.analyze(windowlength_ms=duration_s * 1000, get_distribution=get_distribution, cluster=cluster_states, find_period=detect_period)
    if not result["success"]:
      return None

    aem_analysis_result : types.AemAnalysisResult | None = AdapterBase.__parse_aem_analyze_output(result)
    return aem_analysis_result

#########################################################

  @staticmethod
  def __parse_aem_analyze_output(result: dict) -> types.AemAnalysisResult | None:
    if "result" not in result:
      return None

    aem_distribution           : types.AemDistribution          | None = None
    aem_clustering             : types.AemClustering            | None = None
    aem_period_detection       : types.AemPeriodDetection       | None = None
    aem_signal_characteristics : types.AemSignalCharacteristics | None = None

    dist_dict : dict | None = result["result"].get("distribution", None)
    if dist_dict: 
      aem_distribution = types.AemDistribution()
      aem_distribution.bins = []
      for bin in dist_dict.get("bins", {}):
        aem_distribution.bins.append(types.AemDistributionBin(
          average_current    = bin.get("average_current", None),
          bin_max            = bin.get("bin_max", None),
          bin_min            = bin.get("bin_min", None),
          current_unit       = bin.get("current_unit", None),
          num_samples        = bin.get("num_samples", None),
          percentage         = bin.get("percentage", None),
          standard_deviation = bin.get("standard_deviation", None),
          time               = bin.get("time", None),
          time_unit          = bin.get("time_unit", None),
        ))

      aem_distribution.configuration = types.AemDistributionConfiguration(
        bins        = dist_dict.get("configuration", {}).get("bins", None),
        logarithmic = dist_dict.get("configuration", {}).get("logarithmic", None),
      )

      aem_distribution.summary = types.AemDistributionSummary(
        max_current       = dist_dict.get("summary", {}).get("max_current", None),
        min_current       = dist_dict.get("summary", {}).get("min_current", None),
        total_duration_ms = dist_dict.get("summary", {}).get("total_duration_ms", None),
        total_samples     = dist_dict.get("summary", {}).get("total_samples", None),
        unit              = dist_dict.get("summary", {}).get("unit", None),
      )

      aem_distribution.type = dist_dict.get("type", None)

    cluster_dict : dict | None = result["result"].get("clustering", None)
    if cluster_dict:
      aem_clustering = types.AemClustering()
      aem_clustering.blocks = []
      for block in cluster_dict.get("blocks", {}):
        aem_clustering.blocks.append(types.AemClusterBlock(
          duration_ms = block.get("duration_ms", None),
          end_ms      = block.get("end_ms", None),
          level_mA    = block.get("level_mA", None),
          max_mA      = block.get("max_mA", None),
          min_mA      = block.get("min_mA", None),
          range_mA    = block.get("range_mA", None),
          samples     = block.get("samples", None),
          start_ms    = block.get("start_ms", None),
        ))
      
      aem_clustering.configuration = types.AemClusterConfiguration(
        false_alarm_probability = cluster_dict.get("configuration", {}).get("false_alarm_probability", None),
        max_points              = cluster_dict.get("configuration", {}).get("max_points", None),
        min_segment_ms          = cluster_dict.get("configuration", {}).get("min_segment_ms", None),
      )

      aem_clustering.method        = cluster_dict.get("method", None)
      aem_clustering.total_blocks  = cluster_dict.get("total_blocks", None)
      aem_clustering.type          = cluster_dict.get("type", None)
      aem_clustering.unique_states = cluster_dict.get("unique_states", None)

    period_dict : dict | None = result["result"].get("period_detection", None)
    if period_dict:
      aem_period_detection = types.AemPeriodDetection()
      aem_period_detection.configuration = types.AemPeriodDetectionConfiguration(
        max_period_ms = period_dict.get("configuration", {}).get("max_period_ms", None),
        min_period_ms = period_dict.get("configuration", {}).get("min_period_ms", None),
      )

      aem_period_detection.result = types.AemPeriodDetectionResult()
      aem_period_detection.result.confidence = period_dict.get("result", {}).get("confidence", None)
      aem_period_detection.result.frequency_hz = period_dict.get("result", {}).get("frequency_hz", None)

      aem_period_detection.result.interval_summary = types.AemPeriodDetectionIntervalSummary(
        average_mean_current_ma = period_dict.get("result", {}).get("interval_summary", {}).get("average_mean_current_ma", None),
        average_peak_current_ma = period_dict.get("result", {}).get("interval_summary", {}).get("average_peak_current_ma", None),
        max_period_ms           = period_dict.get("result", {}).get("interval_summary", {}).get("max_period_ms", None),
        min_period_ms           = period_dict.get("result", {}).get("interval_summary", {}).get("min_period_ms", None),
      )

      aem_period_detection.result.intervals = []
      for interval in period_dict.get("result", {}).get("intervals", {}):
        aem_period_detection.result.intervals.append(types.AemPeriodDetectionInterval(
          cycle           = interval.get("cycle", None),
          end_index       = interval.get("end_index", None),
          end_ms          = interval.get("end_ms", None),
          mean_current_ma = interval.get("mean_current_ma", None),
          peak_current_ma = interval.get("peak_current_ma", None),
          period_ms       = interval.get("period_ms", None),
          start_index     = interval.get("start_index", None),
          start_ms        = interval.get("start_ms", None),
        ))

      aem_period_detection.result.is_periodic     = period_dict.get("result", {}).get("is_periodic", None)
      aem_period_detection.result.jitter_relative = period_dict.get("result", {}).get("jitter_relative", None)
      aem_period_detection.result.method          = period_dict.get("result", {}).get("method", None)
      aem_period_detection.result.num_cycles      = period_dict.get("result", {}).get("num_cycles", None)
      aem_period_detection.result.period_ms       = period_dict.get("result", {}).get("period_ms", None)
      aem_period_detection.result.method_results  = []
      for method_result in period_dict.get("result", {}).get("method_results", {}):
        aem_period_detection.result.method_results.append(types.AemPeriodDetectionMethodResult(
          method         = method_result.get("method", None),
          detected       = method_result.get("detected", None),
          confidence     = method_result.get("confidence", None),
          period_ms      = method_result.get("period_ms", None),
          relative_error = method_result.get("relative_error", None),
        ))

      aem_period_detection.type = period_dict.get("type", None)

    signal_char_dict : dict | None = result["result"].get("signal_characteristics", None)
    if signal_char_dict:
      aem_signal_characteristics = types.AemSignalCharacteristics(
        average_voltage_v        = signal_char_dict.get("average_voltage_V", None),
        dynamic_range_ratio      = signal_char_dict.get("dynamic_range_ratio", None),
        estimated_states         = signal_char_dict.get("estimated_states", None),
        max_current_ma           = signal_char_dict.get("max_current_mA", None),
        min_current_ma           = signal_char_dict.get("min_current_mA", None),
        noise_level_mad_sigma_ma = signal_char_dict.get("noise_level_mad_sigma_mA", None),
      )

    return types.AemAnalysisResult(
      distribution           = aem_distribution,
      clustering             = aem_clustering,
      period_detection       = aem_period_detection,
      signal_characteristics = aem_signal_characteristics,
    )
