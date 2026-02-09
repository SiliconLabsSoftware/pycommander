from dataclasses import dataclass

@dataclass
class CtuneValue:
  di:    int | None = None # Value from the Device Info page
  board: int | None = None # Value from the EEPROM on the board
  token: int | None = None # Value from the MFG token
