from .commander import Commander
from .types import CtuneValue

class Device:
  def __init__(self, part_number: str, commander: Commander):
    self._commander : Commander = commander
    self.part_number : str = part_number


  def getCTUNE(self) -> CtuneValue | None:
    """Get the CTUNE values from the DI, board and token on the device.

    Returns:
      A CtuneValue object containing the CTUNE values from the DI, board and token, or None if the CTUNE values could not be retrieved.
    """

    result : dict = self._commander.ctune.get(device=self.part_number)
    if not result["success"]:
      return None

    val = CtuneValue()
    board_setting : dict = result["result"]["ctune"]["board"]
    if board_setting["status_str"] == "OK" and board_setting["valid"]:
      val.board = int(board_setting["value"])
    else:
      val.board = None

    di_setting : dict = result["result"]["ctune"]["di"]
    if di_setting["status_str"] == "OK" and di_setting["valid"]:
      val.di = int(di_setting["value"])
    else:
      val.di = None

    token_setting : dict = result["result"]["ctune"]["token"]
    if token_setting["status_str"] == "OK" and token_setting["valid"]:
      val.token = int(token_setting["value"])
    else:
      val.token = None

    return val


  def setCTUNE(self, value: int | None = None, force: bool = False) -> bool:
    """Set the value to the CTUNE token on the device.

    Args:
      value (int): The value to assign to the CTUNE token. If None, the CTUNE value will be set from the value stored in the board EEPROM.
      force (bool): Force the CTUNE value to be set, even if the desired value is already configured.

    Returns:
      True if the CTUNE value was set successfully, False otherwise.
    """

    existing_ctune : CtuneValue | None = self.getCTUNE()
    if not force and existing_ctune is None:
      return False

    if value is None:
      # Autoset the CTUNE token value from the board value
      if not force and existing_ctune.token == existing_ctune.board:
        # Desired value is already set, so get out early
        return True

      result = self._commander.ctune.autoset(device=self.part_number)
    else:
      # Set the CTUNE token value
      if not force and existing_ctune.token == value:
        # Desired value is already set, so get out early
        return True

      result = self._commander.ctune.set(f"0x{value:08X}", device=self.part_number)

    return result["success"]
