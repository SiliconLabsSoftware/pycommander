import json
from pathlib import Path

from pycommander_core.runner import Runner, RunnerResult


class MockRunner(Runner):
  """Runner that logs the full command instead of executing it.

  Use the `logged_commands` list in tests to assert on which commands were run.
  Each entry is the full command string as would be executed (executable + args).
  """

  def __init__(
    self,
    executable: Path,
    log_file_path: Path | None = None,
    timeout_s: int = 300,
  ):
    super().__init__(executable, log_file_path=log_file_path, timeout_s=timeout_s)
    self.logged_commands: list[str] = []

  def run(self, *args: str, json_format: bool = True) -> RunnerResult:
    if json_format:
      args = (*args, "--json")
    full_cmd = f"{self._executable} {' '.join(args)}"
    self.logged_commands.append(full_cmd)

    if "--version" in args:
      output = json.dumps({
        "result": {
            "version": {"simplicity_commander_version": "0.0.0"},
        },
      })
    elif json_format:
      output = json.dumps({"result": {}})
    else:
      output = ""

    return RunnerResult(0, output)
