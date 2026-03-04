from pathlib import Path

from pycommander_core.commander_base import CommanderBase

class Commander(CommanderBase):
  def __init__(self,
              serial_number:    str  | None = None,
              ip_address:       str  | None = None,
              serial_port:      str  | None = None,
              debug_speed:      int  | None = None,
              debug_tif:        str  | None = None,
              debug_irpre:      int  | None = None,
              debug_drpre:      int  | None = None,
              log_file_path:    Path | None = None,
              executable_path:  Path | None = None):

    super().__init__(serial_number=serial_number,
                     ip_address=ip_address,
                     serial_port=serial_port,
                     debug_speed=debug_speed,
                     debug_tif=debug_tif,
                     debug_irpre=debug_irpre,
                     debug_drpre=debug_drpre,
                     log_file_path=log_file_path,
                     executable_path=executable_path,
                     cli=False)
