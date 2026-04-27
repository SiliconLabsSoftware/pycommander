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
"""

"""LittleFS commands: add, dump, extract, info, init, list, remove."""

from typing import Any

from pycommander_core.commands._base import BaseCommand


class LittlefsCommand(BaseCommand):
  """Commands for interacting with the LittleFS filesystem."""

  def _get_general_args(self, **kwargs: Any) -> list[str]:
    args = self._get_adapter_connection_args()
    args += self._get_debug_args()
    args += super()._get_general_args(**kwargs)
    return args

  def _add_location_args(self,
                         address: int | None = None,
                         range: tuple[int | str, int | str] | None = None,
                         infile: str | None = None) -> list[str]:
    args = []
    if address is not None:
      args += ["--address", self._get_address_string(address)]
    if range is not None:
      args += self._get_ranges([range])
    if infile:
      args += ["--infile", infile]
    return args

  def _get_file_paths(self, file_paths: list[str]) -> list[str]:
    args = []
    for file_path in file_paths:
      args += ["--file", file_path]
    return args

  def _get_dir_paths(self, dir_paths: list[str]) -> list[str]:
    args = []
    for dir_path in dir_paths:
      args += ["--dir", dir_path]
    return args

  def add(self,
          outfile: str,
          file_paths: list[str] = [],
          dir_paths: list[str] = [],
          address: int | None = None,
          range: tuple[int | str, int | str] | None = None,
          infile: str | None = None,
          **kwargs: Any) -> dict:
    """Add file(s) or dir(s) to a LittleFS filesystem.

    Args:
      outfile (str): Output filesystem file path.
      file_paths (list[str]): Files to add (paths relative to cwd).
      dir_paths (list[str]): Directories to add (paths relative to cwd).
      address (int): Memory address of filesystem.
      range (tuple[int | str, int | str]): Memory range (start, end).
      infile (str): Binary file containing the filesystem (or app image).

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    args += self._add_location_args(address, range, infile)
    if file_paths:
      args += self._get_file_paths(file_paths)
    if dir_paths:
      args += self._get_dir_paths(dir_paths)
    args += ["--outfile", outfile]
    return self._run("littlefs", "add", *args).output

  def dump(self,
           outfile: str,
           address: int | None = None,
           range: tuple[int | str, int | str] | None = None,
           infile: str | None = None,
           **kwargs: Any) -> dict:
    """Dump LittleFS filesystem to output file.

    Args:
      outfile (str): Output file path.
      address (int): Memory address.
      range (tuple[int | str, int | str]): Memory range.
      infile (str): Input binary containing filesystem.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    args += self._add_location_args(address, range, infile)
    args += ["--outfile", outfile]
    return self._run("littlefs", "dump", *args).output

  def extract(self,
              dest_dir: str | None = None,
              zip_dir: str | None = None,
              file_paths: list[str] = [],
              dir_paths: list[str] = [],
              address: int | None = None,
              range: tuple[int | str, int | str] | None = None,
              infile: str | None = None,
              **kwargs: Any) -> dict:
    """Extract file(s) or dir(s) from LittleFS to destination or zip.

    Args:
      dest_dir (str): Destination directory for extracted content.
      zip_dir (str): Create zip at this path instead of extracting to dir.
      file_paths (list[str]): Files to extract.
      dir_paths (list[str]): Directories to extract.
      address (int): Memory address.
      range (tuple[int | str, int | str]): Memory range.
      infile (str): Input binary containing filesystem.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    args += self._add_location_args(address, range, infile)
    if file_paths:
      args += self._get_file_paths(file_paths)
    if dir_paths:
      args += self._get_dir_paths(dir_paths)
    if dest_dir:
      args += ["--dest", dest_dir]
    if zip_dir:
      args += ["--zip", zip_dir]
    return self._run("littlefs", "extract", *args).output

  def info(self,
           address: int | None = None,
           range: tuple[int | str, int | str] | None = None,
           infile: str | None = None,
           **kwargs: Any) -> dict:
    """Show LittleFS filesystem info.

    Args:
      address (int): Memory address.
      range (tuple[int | str, int | str]): Memory range.
      infile (str): Input binary containing filesystem.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    args += self._add_location_args(address, range, infile)
    return self._run("littlefs", "info", *args).output

  def init(self,
           outfile: str,
           device: str,
           size: int | None = None,
           address: int | None = None,
           range: tuple[int | str, int | str] | None = None,
           **kwargs: Any) -> dict:
    """Initialize a new LittleFS filesystem.

    Args:
      outfile (str): Output filesystem file path.
      device (str): Device/device family for layout.
      size (int): Filesystem size in bytes.
      address (int): Memory address.
      range (tuple[int | str, int | str]): Memory range.

    Returns:
      Command output as parsed JSON (dict).
    """
    # Don't include the device argument from the PyCommander instance here
    args  = self._get_adapter_connection_args()
    args += self._get_debug_args()
    args += self._get_kwargs(**kwargs)

    if address is not None:
      args += ["--address", self._get_address_string(address)]
    if range is not None:
      args += self._get_ranges([range])
    if size is not None:
      args += ["--size", str(size)]

    args += ["--device", device]
    args += ["--outfile", outfile]
    return self._run("littlefs", "init", *args).output

  def list_files(self,
           address: int | None = None,
           range: tuple[int | str, int | str] | None = None,
           infile: str | None = None,
           **kwargs: Any) -> dict:
    """List files in LittleFS filesystem.

    Args:
      address (int): Memory address.
      range (tuple[int,int]): Memory range.
      infile (str): Input binary containing filesystem.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    args += self._add_location_args(address, range, infile)
    return self._run("littlefs", "list", *args).output

  def remove(self,
             file_paths: list[str] = [],
             dir_paths: list[str] = [],
             address: int | None = None,
             range: tuple[int | str, int | str] | None = None,
             infile: str | None = None,
             **kwargs: Any) -> dict:
    """Remove file(s) or dir(s) from LittleFS filesystem.

    Args:
      file_paths (list[str]): Files to remove.
      dir_paths (list[str]): Directories to remove.
      address (int): Memory address.
      range (tuple[int | str, int | str]): Memory range.
      infile (str): Input binary containing filesystem.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    args += self._add_location_args(address, range, infile)
    if file_paths:
      args += self._get_file_paths(file_paths)
    if dir_paths:
      args += self._get_dir_paths(dir_paths)
    return self._run("littlefs", "remove", *args).output
