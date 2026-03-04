# Ensure that the Commander executable is present
# This entails checking if the executable is present where it should be, and if not, extracting it from the
# archive embedded in the package.
import sys
import hashlib
import subprocess
import shutil

import importlib.resources as ir

from pathlib import Path
from platformdirs import user_cache_dir

from .paths import EXECUTABLE_PATH_CLI, EXECUTABLE_PATH_GUI

def ensure_commander(cli: bool = True) -> Path:
  if cli:
    package_name        = "pycommander_cli._archive"
    executable_path     = EXECUTABLE_PATH_CLI
  else:
    package_name        = "pycommander_gui._archive"
    executable_path     = EXECUTABLE_PATH_GUI
  
  cache_dir = Path(user_cache_dir(f"pycommander", "silabs"))
  archive_path = Path(_find_executable_archive_resource(package_name))
  archive_hash = _compute_hash_of_file(archive_path)

  target_dir = cache_dir / archive_hash

  if not target_dir.exists():
    target_dir.mkdir(parents=True, exist_ok=True)

    _extract_commander(archive_path, target_dir)

  return Path(target_dir / executable_path)

def _extract_commander(zip_file_path: Path, destination: Path) -> None:
  # Remove the existing executable and stamp files, if they exist.
  if destination.exists():
    shutil.rmtree(destination, ignore_errors=True)

  # Find the filename of the executable in the archive
  with ir.as_file(zip_file_path) as zip_file:
    if sys.platform == "darwin":
      _extract_commander_macos(zip_file, destination)
    elif sys.platform == "linux":
      _extract_commander_linux(zip_file, destination)
    elif sys.platform == "win32":
      _extract_commander_windows(zip_file, destination)
    else:
      raise ValueError(f"Unsupported platform: {sys.platform}")

def _extract_commander_macos(zip_file: Path, destination: Path) -> None:
  if not zip_file.exists():
    raise FileNotFoundError(f"Executable archive not found: {zip_file}")

  destination.mkdir(parents=True, exist_ok=True)
  subprocess.run(
    ["ditto", "-xk", str(zip_file), str(destination)],
    check=True
  )

def _extract_commander_linux(zip_file: Path, destination: Path) -> None:
  if not zip_file.exists():
    raise FileNotFoundError(f"Executable archive not found: {zip_file}")

  destination.mkdir(parents=True, exist_ok=True)
  subprocess.run(
    ["tar", "-xjf", str(zip_file), "-C", str(destination)],
    check=True
  )

def _extract_commander_windows(zip_file: Path, destination: Path) -> None:
  if not zip_file.exists():
    raise FileNotFoundError(f"Executable archive not found: {zip_file}")

  destination.mkdir(parents=True, exist_ok=True)
  subprocess.run(
    ["powershell", "-Command", "Expand-Archive", f"-Path {str(zip_file)}", f"-DestinationPath {str(destination)}"],
    check=True
  )

def _compute_hash_of_file(path: Path) -> str:
  hash = hashlib.sha256()
  hash.update(path.read_bytes())
  return hash.hexdigest()[:16]

def _find_executable_archive_resource(package: str) -> Path:
  root = ir.files(package)
  candidates : list[Path] = []
  for entry in root.iterdir():
    if not entry.is_file():
      continue
    name = entry.name
    if name.endswith(".zip") or name.endswith(".tar.bz"):
      candidates.append(root / name)

  if len(candidates) == 0:
    raise FileNotFoundError(f"No executable archive found in {root}")

  return candidates[0]
