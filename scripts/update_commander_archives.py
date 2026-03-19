#!/usr/bin/env python3

"""
This is a convenience script to update the Commander archives that are embedded in the pycommander packages.
For the specified version of Commander, it pulls all available archives from the Artifactory repository and
places them in the ../archives directory. The release process will then later use these archives to create
the wheels that are uploaded to PyPI.

Usage:
  ./update_commander_archives.py [-v, --version <version>]

Options:
  -v, --version <version>   The version of Commander to update to (e.g. 1.2.3). If not specified, the script 
                            will traverse the Artifactory API and find the latest version (in terms of 
                            the version number, not the time of upload).

Example:
  ./update_commander_archives.py
  ./update_commander_archives.py --version 1.0.0

"""


import argparse
import re
import requests

from pathlib import Path

ARTIFACTORY_URL_BASE = "https://artifactory.silabs.net/ui/native"
ARTIFACTORY_API_BASE = "https://artifactory.silabs.net/artifactory/api/storage"
ARTIFACTORY_REPO_KEY = "hwtools-releases"
COMMANDER_PATH = "Software/Simplicity-Commander"
ARTIFACTORY_URL = f"{ARTIFACTORY_URL_BASE}/{ARTIFACTORY_REPO_KEY}/{COMMANDER_PATH}"
ARTIFACTORY_API = f"{ARTIFACTORY_API_BASE}/{ARTIFACTORY_REPO_KEY}/{COMMANDER_PATH}"

ARCHIVES_DIR = Path(__file__).resolve().parent.parent / "archives"

VERSION_STRING_REGEX = r"^(\d+)v(\d+)p(\d+)$"
VERSION_NUMBER_REGEX = r"^(\d+)\.(\d+)\.(\d+)$"

def get_latest_version_string_from_artifactory() -> str:
  response = requests.get(ARTIFACTORY_API)
  if response.status_code != 200:
    raise Exception(f"Failed to get latest version from Artifactory: {response.status_code}")

  json_response = response.json()

  latest_version_major = 0
  latest_version_minor = 0
  latest_version_patch = 0
  for child in json_response["children"]:
    v = child["uri"].lstrip("/")
    m = re.match(VERSION_STRING_REGEX, v)
    if not m:
      continue

    major = int(m.group(1))
    minor = int(m.group(2))
    patch = int(m.group(3))

    if major > latest_version_major:
      latest_version_major = major
      latest_version_minor = minor
      latest_version_patch = patch
    elif major == latest_version_major:

      if minor > latest_version_minor:
        latest_version_minor = minor
        latest_version_patch = patch
      elif minor == latest_version_minor:
        if patch > latest_version_patch:
          latest_version_patch = patch

  return f"{latest_version_major}v{latest_version_minor}p{latest_version_patch}"


def get_artifact_urls_from_artifactory(version_string: str) -> list[str]:
  version_dir = f"{ARTIFACTORY_API}/{version_string}"
  
  response = requests.get(version_dir)
  if response.status_code != 200:
    raise Exception(f"Failed to get artifact URLs from Artifactory: {response.status_code}")

  json_response = response.json()

  artifact_urls = []
  for child in json_response["children"]:
    child_uri = child["uri"].lstrip("/")
    if not child_uri.startswith("Commander"):
      continue

    child_dir = f"{version_dir}/{child_uri}"
    child_response = requests.get(child_dir)
    if child_response.status_code != 200:
      raise Exception(f"Failed to get artifact URLs from Artifactory for {child_dir}: {child_response.status_code}")

    child_json_response = child_response.json()

    download_uri = child_json_response["downloadUri"]
    artifact_urls.append(download_uri)
  return artifact_urls


def get_longest_string_length(strings: list[str]) -> int:
  return max(len(s) for s in strings)


def main(version: str) -> int:
  version_string : str = ""

  if version:
    m = re.match(VERSION_NUMBER_REGEX, version)
    if not m:
      raise ValueError("Invalid version format. Please use the format X.Y.Z.")
    print(f"Looking for version {version}...")
    version_string = f"{m.group(1)}v{m.group(2)}p{m.group(3)}"
  else:
    print("Looking for latest version...")
    version_string = get_latest_version_string_from_artifactory()
    print(f"Latest version is {version_string}")

  artifact_urls = get_artifact_urls_from_artifactory(version_string)
  print(f"Found {len(artifact_urls)} artifacts at {ARTIFACTORY_URL}/{version_string}")

  print("Nuking existing archives...")
  for file in ARCHIVES_DIR.glob("*"):
    file.unlink()

  print("Downloading fresh ones. This may take a little while...")
  longest_filename_length = get_longest_string_length([url.split("/")[-1] for url in artifact_urls]) + 3
  for artifact_url in artifact_urls:
    filename = artifact_url.split("/")[-1]
    print(f"  {filename:.<{longest_filename_length}}", end="")
    with requests.get(artifact_url, stream=True) as response:
      if response.status_code != 200:
        raise Exception(f"Failed to download {filename}: {response.status_code}")
      with open(ARCHIVES_DIR / filename, "wb") as f:
        total_size = int(response.headers.get("content-length", 0))
        downloaded = 0
        for chunk in response.iter_content(chunk_size=8192):
          if not chunk:
            continue
          f.write(chunk)
          downloaded += len(chunk)
          progress = int(downloaded / total_size * 100)
          print(f"\r  {filename:.<{longest_filename_length}} {progress:>3}%", end="", flush=True)
    print(f"\r  {filename:.<{longest_filename_length}} 100%")

  print(f"Archives updated to version {version_string}")

  return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", type=str, required=False, default="")
    args = parser.parse_args()
    raise SystemExit(main(args.version))
