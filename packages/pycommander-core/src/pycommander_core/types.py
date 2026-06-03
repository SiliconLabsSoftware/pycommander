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

import enum

from dataclasses import dataclass

@dataclass
class CommanderVersionInfo:
  simplicity_commander_version: str
  jlink_dll_version: str
  emdll_version: str
  mbed_tls_version: str
  qt_version: str

@dataclass
class AemMeasurement:
  timestamp_us: int
  current_ma: float
  voltage_v: float
  power_mw: float

@dataclass
class AdapterBoardInfo:
  name:          str | None = None
  part_number:   str | None = None
  serial_number: str | None = None
  target_device: str | None = None

@dataclass
class AdapterFwInfo:
  current_version:   str  | None = None
  latest_version:    str  | None = None
  upgrade_available: bool | None = None

@dataclass
class BasicAdapterInfo:
  jlink_serial_number: str
  ip_address: str
  nickname: str

@dataclass
class AdapterInfo:
  board_list:          list[AdapterBoardInfo] | None = None
  fw_info:             AdapterFwInfo          | None = None
  jlink_serial_number: int                    | None = None
  vcom_port:           str                    | None = None
  vcom_supported:      bool                   | None = None
  ip_supported:        bool                   | None = None
  ip_address:          str                    | None = None
  mac_address:         str                    | None = None
  kit_name:            str                    | None = None
  kit_part_number:     str                    | None = None
  aem_supported:       bool                   | None = None
  debug_mode:          str                    | None = None
  debug_part:          str                    | None = None

@dataclass
class AdapterRailInfo:
  rail_index:           int   | None = None
  configured_voltage_v: float | None = None
  measured_voltage_v:   float | None = None
  rail_powered:         bool  | None = None

@dataclass
class AdapterVoltageInfo:
  rails: list[AdapterRailInfo]

@dataclass
class CtuneValue:
  di:    int | None = None # Value from the Device Info page
  board: int | None = None # Value from the EEPROM on the board
  token: int | None = None # Value from the MFG token

@dataclass
class TargetInfo:
  part_number:        str | None = None
  die_revision:       str | None = None
  production_version: str | None = None
  flash_size_kb:      int | None = None
  sram_size_kb:       int | None = None
  unique_id:          str | None = None

class CodeRegionProtectionMode(enum.Enum):
  ENCRYPTED_AND_AUTHENTICATED = "encrypted_authenticated"
  ENCRYPTED                   = "encrypted"
  NONE                        = "none"

@dataclass
class CodeRegionConfig:
  index: int
  size_kb: int
  protection_mode: CodeRegionProtectionMode
  closed: bool

@dataclass
class DataRegionConfig:
  location: int
  size: int

@dataclass
class RegionConfig:
  code_regions: list[CodeRegionConfig]
  data_region: DataRegionConfig

class VcomHandshake(enum.Enum):
  NONE   = "none"
  RTSCTS = "rtscts"
  AUX    = "aux"

@dataclass
class TrustzoneConfig:
  debug_lock_locked: bool
  debug_port_locked: bool
  nidlock_locked: bool
  spidlock_locked: bool
  spnidlock_locked: bool

@dataclass
class TrustzoneState:
  debug_lock_locked: bool
  nidlock_locked: bool
  spidlock_locked: bool
  spnidlock_locked: bool

@dataclass
class SecurityStatus:
  boot_status: int
  boot_status_str: str
  command_key_installed: bool
  debug_lock_enabled: bool
  device_erase_enabled: bool
  se_firmware_version: str
  secure_boot_enabled: bool
  secure_debug_unlock_enabled: bool
  serial_number: str
  sign_key_installed: bool
  tamper_ok: bool
  trustzone_config: TrustzoneConfig | None = None
  trustzone_state: TrustzoneState   | None = None

@dataclass
class SeFirmwareInfo:
  current_version:   str  | None = None
  latest_version:    str  | None = None
  upgrade_available: bool | None = None

@dataclass
class AemClusterBlock:
  duration_ms: float | None = None
  end_ms:      float | None = None
  level_mA:    float | None = None
  max_mA:      float | None = None
  min_mA:      float | None = None
  range_mA:    float | None = None
  samples:     int   | None = None
  start_ms:    float | None = None

@dataclass
class AemClusterConfiguration:
  false_alarm_probability: float | None = None
  max_points:              int   | None = None
  min_segment_ms:          float | None = None

@dataclass
class AemClustering:
  blocks:        list[AemClusterBlock]   | None = None
  configuration: AemClusterConfiguration | None = None
  method:        str                     | None = None
  total_blocks:  int                     | None = None
  type:          str                     | None = None
  unique_states: int                     | None = None

@dataclass
class AemDistributionBin:
  average_current:    float | None = None
  bin_max:            float | None = None
  bin_min:            float | None = None
  current_unit:       str   | None = None
  num_samples:        int   | None = None
  percentage:         float | None = None
  standard_deviation: float | None = None
  time:               float | None = None
  time_unit:          str   | None = None

@dataclass
class AemDistributionConfiguration:
  bins:        int  | None = None
  logarithmic: bool | None = None

@dataclass
class AemDistributionSummary:
  max_current:       float | None = None
  min_current:       float | None = None
  total_duration_ms: float | None = None
  total_samples:     int   | None = None
  unit:              str   | None = None

@dataclass
class AemDistribution:
  bins:          list[AemDistributionBin]     | None = None
  configuration: AemDistributionConfiguration | None = None
  summary:       AemDistributionSummary       | None = None
  type:          str                          | None = None

@dataclass
class AemPeriodDetectionConfiguration:
  max_period_ms: float | None = None
  min_period_ms: float | None = None

@dataclass
class AemPeriodDetectionIntervalSummary:
  average_mean_current_ma: float | None = None
  average_peak_current_ma: float | None = None
  max_period_ms:           float | None = None
  min_period_ms:           float | None = None

@dataclass
class AemPeriodDetectionInterval:
  cycle:           int   | None = None
  end_index:       int   | None = None
  end_ms:          float | None = None
  mean_current_ma: float | None = None
  peak_current_ma: float | None = None
  period_ms:       float | None = None
  start_index:     int   | None = None
  start_ms:        float | None = None

@dataclass
class AemPeriodDetectionMethodResult:
  method:         str   | None = None
  detected:       bool  | None = None
  confidence:     float | None = None
  period_ms:      float | None = None
  relative_error: float | None = None

@dataclass
class AemPeriodDetectionResult:
  confidence:       float                                | None = None
  frequency_hz:     float                                | None = None
  interval_summary: AemPeriodDetectionIntervalSummary    | None = None
  intervals:        list[AemPeriodDetectionInterval]     | None = None
  is_periodic:      bool                                 | None = None
  jitter_relative:  float                                | None = None
  method:           str                                  | None = None
  method_results:   list[AemPeriodDetectionMethodResult] | None = None
  num_cycles:       int                                  | None = None
  period_ms:        float                                | None = None

@dataclass
class AemPeriodDetection:
  configuration: AemPeriodDetectionConfiguration | None = None
  result:        AemPeriodDetectionResult        | None = None
  type:          str                             | None = None

@dataclass
class AemSignalCharacteristics:
  average_voltage_v:        float | None = None
  dynamic_range_ratio:      float | None = None
  estimated_states:         int   | None = None
  max_current_ma:           float | None = None
  min_current_ma:           float | None = None
  noise_level_mad_sigma_ma: float | None = None

@dataclass
class AemAnalysisResult:
  distribution:           AemDistribution          | None = None
  clustering:             AemClustering            | None = None
  period_detection:       AemPeriodDetection       | None = None
  signal_characteristics: AemSignalCharacteristics | None = None
