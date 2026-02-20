import enum

from dataclasses import dataclass

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
class AdapterVoltageInfo:
  configured_voltage_v: float | None = None
  measured_voltage_v: float | None = None
  rail_powered: bool | None = None

@dataclass
class CtuneValue:
  di:    int | None = None # Value from the Device Info page
  board: int | None = None # Value from the EEPROM on the board
  token: int | None = None # Value from the MFG token

@dataclass
class DeviceInfo:
  part_number:        str | None = None
  die_revision:       str | None = None
  production_version: str | None = None
  flash_size_kb:      int | None = None
  sram_size_kb:       int | None = None
  unique_id:          str | None = None

class CodeRegionProtectionMode(enum.Enum):
  ENCRYPTED_AND_AUTHENTICATED = "encrypted_authenticated"
  ENCRYPTED = "encrypted"
  NONE = "none"

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
  NONE = "none"
  RTSCTS = "rtscts"
  AUX = "aux"
