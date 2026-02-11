from pathlib import Path

from pycommander_core.commander_base import CommanderBase
from pycommander_core.commands._base import BaseCommand

from .mock_runner import MockRunner


class MockCommander(CommanderBase):
  """Commander that uses MockRunner instead of Runner.

  In tests, use commander._runner.logged_commands to inspect the full
  command lines that were "run" (without actually executing them).
  """

  def __init__(
    self,
    serial_number: str | None = None,
    ip_address: str | None = None,
    serial_port: str | None = None,
    debug_speed: int | None = None,
    debug_tif: str | None = None,
    debug_irpre: int | None = None,
    debug_drpre: int | None = None,
    log_file_path: Path | None = None,
    executable_path: Path | None = None,
  ):
    executable_path = executable_path or Path("mock")
    super().__init__(
      serial_number=serial_number,
      ip_address=ip_address,
      serial_port=serial_port,
      debug_speed=debug_speed,
      debug_tif=debug_tif,
      debug_irpre=debug_irpre,
      debug_drpre=debug_drpre,
      log_file_path=log_file_path,
      executable_path=executable_path,
    )

    # Replace the runner with a mock runner
    self._runner = MockRunner(
      executable_path,
      log_file_path=log_file_path,
      timeout_s=CommanderBase.default_timeout_s,
    )

    # Update all commands to use the mock runner
    for command in self.__dict__.values():
      if isinstance(command, BaseCommand):
        command._commander = self
        command._runner    = self._runner
