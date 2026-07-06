#! /usr/bin/env python3

"""
License
Copyright 2026 Silicon Laboratories Inc. www.silabs.com
*******************************************************************************
The licensor of this software is Silicon Laboratories Inc. Your use of this
software is governed by the terms of Silicon Labs Master Software License
Agreement (MSLA) available at
www.silabs.com/about-us/legal/master-software-license-agreement. This
software is distributed to you in Source Code format and is governed by the
sections of the MSLA applicable to Source Code.
*******************************************************************************

Developer helper: download the Simplicity Commander release archives for a given
tag and drop them into the `_archive` directories of the CLI and GUI packages.

This mirrors what the CI workflow (`.github/workflows/build-wheels-and-publish.yml`)
does, but for a local development checkout. The raw archive files are placed as-is;
runtime extraction is handled by `pycommander_core._ensure_commander`.

Options:
  -t, --tag TAG        Release tag to download (default: extracted from .github/commander-version file).
  -p, --platform PLAT  Platform archives to fetch, or 'auto' to detect the host
                       (default: auto). Choices: linux-x86_64, linux-aarch64,
                       linux-aarch32, macos, windows, auto.
  --repo OWNER/NAME    GitHub repository (default: SiliconLabsSoftware/pycommander).
  --token TOKEN        GitHub token for private forks (default: GITHUB_TOKEN / GH_TOKEN environment variables).
  -h, --help           Show the full help and exit.

Examples:
  # Use the tag pinned in .github/commander-version, auto-detect this machine:
  python scripts/download_commander_archives.py

  # Pick a specific tag:
  python scripts/download_commander_archives.py --tag commander-1v24p3

  # Download a platform other than the host (e.g. from a mac, grab the linux build):
  python scripts/download_commander_archives.py --platform linux-x86_64

For private forks, set GITHUB_TOKEN (or GH_TOKEN) environment variables to allow the assets to be fetched.
"""

import argparse
import json
import os
import platform
import re
import shutil
import sys
import urllib.error
import urllib.parse
import urllib.request

from pathlib import Path

DEFAULT_REPO = "SiliconLabsSoftware/pycommander"

REPO_ROOT = Path(__file__).resolve().parents[1]
COMMANDER_VERSION_FILE = REPO_ROOT / ".github" / "commander-version"

CLI_ARCHIVE_DIR = REPO_ROOT / "packages" / "pycommander-cli" / "src" / "pycommander_cli" / "_archive"
GUI_ARCHIVE_DIR = REPO_ROOT / "packages" / "pycommander-gui" / "src" / "pycommander_gui" / "_archive"

# Release-asset naming, keyed by platform. `token` is the platform slug that appears
# in the asset filename and `ext` is the archive extension used for that platform.
# Mirrors the matrix in build-wheels-and-publish.yml.
PLATFORMS: dict[str, dict[str, str]] = {
  "linux-x86_64":  {"token": "linux_x86_64",  "ext": "tar.bz"},
  "linux-aarch64": {"token": "linux_aarch64", "ext": "tar.bz"},
  "linux-aarch32": {"token": "linux_aarch32", "ext": "tar.bz"},
  "macos":         {"token": "osx",           "ext": "zip"},
  "windows":       {"token": "win32_x64",     "ext": "zip"},
}

# The two flavors and the filename prefix each release asset uses.
#   CLI assets look like:  Commander-cli_<token>_<version>.<ext>
#   GUI assets look like:  Commander_<token>_<version>.<ext>
FLAVORS: dict[str, dict[str, object]] = {
  "cli": {"prefix": "Commander-cli", "dir": CLI_ARCHIVE_DIR},
  "gui": {"prefix": "Commander",     "dir": GUI_ARCHIVE_DIR},
}


class _StripAuthOnRedirect(urllib.request.HTTPRedirectHandler):
  """Drop the Authorization header when a redirect crosses to a different host.

  GitHub asset downloads redirect from api.github.com to a signed storage URL
  (e.g. S3). Forwarding our `Authorization: Bearer ...` header to that host makes
  the storage backend reject the request, so we strip it on cross-host redirects.
  """

  def redirect_request(self, req, fp, code, msg, headers, newurl):
    new_req = super().redirect_request(req, fp, code, msg, headers, newurl)
    if new_req is None:
      return None
    old_host = urllib.parse.urlparse(req.full_url).netloc
    new_host = urllib.parse.urlparse(newurl).netloc
    if old_host != new_host:
      new_req.headers = {
        key: value for key, value in new_req.headers.items()
        if key.lower() != "authorization"
      }
    return new_req


_OPENER = urllib.request.build_opener(_StripAuthOnRedirect())


def detect_platform() -> str:
  """Return the PLATFORMS key matching the host machine."""
  if sys.platform == "darwin":
    return "macos"
  if sys.platform == "win32":
    return "windows"
  if sys.platform.startswith("linux"):
    machine = platform.machine().lower()
    if machine in ("x86_64", "amd64"):
      return "linux-x86_64"
    if machine in ("aarch64", "arm64"):
      return "linux-aarch64"
    if machine in ("armv7l", "armv6l", "armv8l"):
      return "linux-aarch32"
    raise SystemExit(
      f"Unsupported Linux architecture '{machine}'. "
      f"Pass --platform explicitly (choices: {', '.join(PLATFORMS)})."
    )
  raise SystemExit(
    f"Unsupported platform '{sys.platform}'. "
    f"Pass --platform explicitly (choices: {', '.join(PLATFORMS)})."
  )


def read_default_tag() -> str:
  if not COMMANDER_VERSION_FILE.exists():
    raise SystemExit(
      f"No --tag given and default file not found: {COMMANDER_VERSION_FILE}"
    )
  tag = COMMANDER_VERSION_FILE.read_text(encoding="utf-8").strip()
  if not tag:
    raise SystemExit(f"Default tag file is empty: {COMMANDER_VERSION_FILE}")
  return tag


def get_release(repo: str, tag: str, token: str | None) -> dict:
  url = f"https://api.github.com/repos/{repo}/releases/tags/{urllib.parse.quote(tag)}"
  request = urllib.request.Request(
    url,
    headers={
      "Accept": "application/vnd.github+json",
      "X-GitHub-Api-Version": "2022-11-28",
    },
  )
  if token:
    request.add_header("Authorization", f"Bearer {token}")

  try:
    with _OPENER.open(request) as response:
      return json.load(response)
  except urllib.error.HTTPError as error:
    if error.code == 404:
      raise SystemExit(
        f"Release for tag '{tag}' not found in '{repo}'. "
        f"(If the repo is private, set GITHUB_TOKEN / GH_TOKEN.)"
      ) from error
    if error.code in (401, 403):
      raise SystemExit(
        f"Access denied ({error.code}) fetching release '{tag}' from '{repo}'. "
        f"Set GITHUB_TOKEN / GH_TOKEN with access to the repo."
      ) from error
    raise SystemExit(f"Failed to fetch release '{tag}': HTTP {error.code}") from error
  except urllib.error.URLError as error:
    raise SystemExit(f"Network error fetching release '{tag}': {error.reason}") from error


def select_assets(assets: list[dict], platform_key: str) -> dict[str, list[dict]]:
  """Return, per flavor, the release assets matching the requested platform."""
  spec = PLATFORMS[platform_key]
  token = spec["token"]
  ext = spec["ext"]

  selected: dict[str, list[dict]] = {}
  for flavor, info in FLAVORS.items():
    prefix = str(info["prefix"])
    pattern = re.compile(
      rf"^{re.escape(prefix)}_{re.escape(token)}_.*\.{re.escape(ext)}$"
    )
    matches = [asset for asset in assets if pattern.match(asset.get("name", ""))]
    selected[flavor] = matches
  return selected


def clean_archive_dir(directory: Path) -> None:
  """Remove existing Commander archives, leaving package/docs files intact."""
  if not directory.exists():
    return
  for entry in directory.iterdir():
    if entry.is_file() and entry.name.startswith("Commander"):
      print(f"  removing existing {entry.name}")
      entry.unlink()


def download_asset(asset: dict, destination_dir: Path, token: str | None) -> Path:
  destination = destination_dir / asset["name"]

  if token:
    # The asset API URL returns the binary when asked for octet-stream, and works
    # for private repos. Cross-host redirect auth is stripped by the opener.
    url = asset["url"]
    headers = {
      "Accept": "application/octet-stream",
      "Authorization": f"Bearer {token}",
    }
  else:
    url = asset["browser_download_url"]
    headers = {}

  request = urllib.request.Request(url, headers=headers)
  try:
    with _OPENER.open(request) as response, open(destination, "wb") as handle:
      shutil.copyfileobj(response, handle)
  except urllib.error.HTTPError as error:
    raise SystemExit(
      f"Failed to download '{asset['name']}': HTTP {error.code}"
    ) from error
  except urllib.error.URLError as error:
    raise SystemExit(
      f"Network error downloading '{asset['name']}': {error.reason}"
    ) from error
  return destination


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
  parser = argparse.ArgumentParser(
    description=(
      "Download Simplicity Commander release archives for a tag into the CLI and "
      "GUI package _archive directories."
    ),
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
  )
  parser.add_argument(
    "-t", "--tag",
    default=None,
    help="Release tag to download (e.g. commander-1v24p3). "
         "Defaults to the value in .github/commander-version.",
  )
  parser.add_argument(
    "-p", "--platform",
    choices=[*PLATFORMS.keys(), "auto"],
    default="auto",
    help="Platform archives to fetch. 'auto' detects the host machine.",
  )
  parser.add_argument(
    "--repo",
    default=DEFAULT_REPO,
    help="GitHub repository in owner/name form.",
  )
  parser.add_argument(
    "--token",
    default=os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN"),
    help="GitHub token for private repos. Falls back to GITHUB_TOKEN / GH_TOKEN.",
  )
  return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
  args = parse_args(argv)

  tag = args.tag or read_default_tag()
  platform_key = detect_platform() if args.platform == "auto" else args.platform

  print(f"Repository : {args.repo}")
  print(f"Tag        : {tag}")
  print(f"Platform   : {platform_key}")
  if not args.token:
    print("Token      : (none) - fine for public repos; needed for private ones")
  print()

  release = get_release(args.repo, tag, args.token)
  assets = release.get("assets", [])
  if not assets:
    raise SystemExit(f"Release '{tag}' has no downloadable assets.")

  selected = select_assets(assets, platform_key)

  # Fail early if either flavor is missing so we don't leave a half-populated checkout.
  missing = [flavor for flavor, matches in selected.items() if not matches]
  if missing:
    spec = PLATFORMS[platform_key]
    available = ", ".join(sorted(asset.get("name", "") for asset in assets))
    raise SystemExit(
      f"No {', '.join(missing)} archive found for platform '{platform_key}' "
      f"(token '{spec['token']}', .{spec['ext']}) in release '{tag}'.\n"
      f"Available assets: {available}"
    )

  downloaded: list[Path] = []
  for flavor, matches in selected.items():
    target_dir = Path(str(FLAVORS[flavor]["dir"]))
    target_dir.mkdir(parents=True, exist_ok=True)

    print(f"[{flavor}] -> {target_dir.relative_to(REPO_ROOT)}")
    clean_archive_dir(target_dir)

    for asset in matches:
      print(f"  downloading {asset['name']} ...")
      path = download_asset(asset, target_dir, args.token)
      downloaded.append(path)
      print(f"  saved {path.relative_to(REPO_ROOT)}")
    print()

  print(f"Done. Downloaded {len(downloaded)} archive(s) for '{tag}' ({platform_key}).")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
