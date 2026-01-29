# Ensure that the Commander executable is present
# This entails checking if the executable is present where it should be, and if not, extracting it from the
# archive embedded in the package.

import hashlib
import subprocess
import shutil

import importlib.resources as ir

from pathlib import Path

from .paths import *

def ensure_commander() -> bool:
  if not PYCOMMANDER_DIR.exists():
    PYCOMMANDER_DIR.mkdir(parents=True, exist_ok=True)

  # Look for the executable zip in the packages
  if EXECUTABLE_PATH.exists() and STAMP_FILE_PATH.exists():
    # Check if the executable is up to date. We do this by computing the hash of the archive directory and comparing it to the hash stored in the stamp file.
    expected_hash = _compute_hash_of_resource("pycommander._archive", _find_executable_archive_resource())
    stored_hash   = _read_hash_from_file(STAMP_FILE_PATH)
    if expected_hash == stored_hash:
      # All good, nothing to be done.
      return True
    else:
      # The executable is not up to date, so we need to extract it from the archive
      _extract_commander()
  else:
    # The executable is not present, or the stamp file is missing. Extract Commander.
    _extract_commander()

  return True

def _extract_commander() -> None:
  # Nuke the existing executable and stamp files, if need be.
  if EXECUTABLE_ROOT_DIR.exists():
    shutil.rmtree(EXECUTABLE_ROOT_DIR, ignore_errors=True)
  if STAMP_FILE_PATH.exists():
    STAMP_FILE_PATH.unlink()

  resource = _find_executable_archive_resource()

  # Find the filename of the executable in the archive
  with ir.as_file(ir.files("pycommander._archive") / resource) as zip_file:
    if sys.platform == "darwin":
      _extract_commander_macos(zip_file, EXECUTABLE_ROOT_DIR)
    elif sys.platform == "linux":
      _extract_commander_linux(zip_file, EXECUTABLE_ROOT_DIR)
    elif sys.platform == "win32":
      _extract_commander_windows(zip_file, EXECUTABLE_ROOT_DIR)
    else:
      raise ValueError(f"Unsupported platform: {sys.platform}")

    _write_hash_to_file(STAMP_FILE_PATH, _compute_hash_of_resource("pycommander._archive", resource))

def _extract_commander_macos(zip_file: Path, destination: Path) -> None:
  destination.mkdir(parents=True, exist_ok=True)
  subprocess.run(
    ["ditto", "-xk", str(zip_file), str(destination)],
    check=True
  )

def _extract_commander_linux(zip_file: Path, destination: Path) -> None:
  destination.mkdir(parents=True, exist_ok=True)
  subprocess.run(
    ["tar", "-xjf", str(zip_file), "-C", str(destination)],
    check=True
  )

def _extract_commander_windows(zip_file: Path, destination: Path) -> None:
  destination.mkdir(parents=True, exist_ok=True)
  subprocess.run(
    ["powershell", "-Command", "Expand-Archive", f"-Path {str(zip_file)}", f"-DestinationPath {str(destination)}"],
    check=True
  )

def _compute_hash_of_resource(package: str, resource: str) -> str:
  hash = hashlib.sha256()

  with ir.open_binary(package, resource) as f:
    for chunk in iter(lambda: f.read(4096), b""):
      hash.update(chunk)

  return "sha256:" + hash.hexdigest()

def _find_executable_archive_resource() -> str:
  root = ir.files("pycommander._archive")
  candidates : list[str] = []
  for entry in root.iterdir():
    if not entry.is_file():
      continue
    name = entry.name
    if name.endswith(".zip") or name.endswith(".tar.bz"):
      candidates.append(name)

  if len(candidates) == 0:
    raise FileNotFoundError(f"No executable archive found in {root}")

  return candidates[0]

def _read_hash_from_file(stamp_file: Path) -> str:
  if not stamp_file.exists():
    return ""
  return stamp_file.read_text().strip()

def _write_hash_to_file(stamp_file: Path, hash: str) -> None:
  stamp_file.write_text(hash)
