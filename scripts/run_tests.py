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

Run the unit tests for the pycommander packages.
"""

import unittest
import sys

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent


def load_tests():
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()
  suite.addTests(loader.discover(ROOT_DIR / "packages" / "pycommander-core" / "tests", pattern="test_*.py", top_level_dir="."))
  suite.addTests(loader.discover(ROOT_DIR / "packages" / "pycommander-cli"  / "tests", pattern="test_*.py", top_level_dir="."))
  suite.addTests(loader.discover(ROOT_DIR / "packages" / "pycommander-gui"  / "tests", pattern="test_*.py", top_level_dir="."))
  suite.addTests(loader.discover(ROOT_DIR / "packages" / "pycommander"      / "tests", pattern="test_*.py", top_level_dir="."))
  return suite

if __name__ == "__main__":
  runner = unittest.TextTestRunner(verbosity=2)
  result = runner.run(load_tests())
  sys.exit(not result.wasSuccessful())
