from hatchling.builders.hooks.plugin.interface import BuildHookInterface

# We are including platform-specific files in the wheel, even though the package is pure Python.
# Add a custom build hook to ensure that the built wheel does not claim to suitable for *any* platform
class PyCommanderBuildHook(BuildHookInterface):
  def initialize(self, version: str, build_system: str) -> None:
    build_system["infer_tag"] = True
    build_system["pure_python"] = False
