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
    self._executable = str(executable)
    self._log_file_path = log_file_path
    self._timeout_s = timeout_s
    self._subprocess_flags = 0
    self.logged_commands: list[list[str]] = []
    self.queued_results: list[RunnerResult] = []

  def run(self, *args: str, json_format: bool = True) -> RunnerResult:
    if json_format:
      args = (*args, "--json")

    self.logged_commands.append([str(self._executable), *args])

    if "--version" in args:
      output = json.dumps({
        "result": {
            "version": {"simplicity_commander_version": "0.0.0"},
        },
      })
    elif self.queued_results:
      result = self.queued_results.pop(0)
      return result
    elif json_format:
      output = json.dumps({"result": {}})
    else:
      output = ""

    return RunnerResult(0, output)

  def queue_result(self, result: RunnerResult):
    self.queued_results.append(result)
