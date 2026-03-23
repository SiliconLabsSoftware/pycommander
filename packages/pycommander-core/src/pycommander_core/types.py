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
class AdapterRailInfo:
  rail_index: int | None = None
  configured_voltage_v: float | None = None
  measured_voltage_v: float | None = None
  rail_powered: bool | None = None

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
  trustzone_state: TrustzoneState | None = None

@dataclass
class SeFirmwareInfo:
  current_version:   str  | None = None
  latest_version:    str  | None = None
  upgrade_available: bool | None = None