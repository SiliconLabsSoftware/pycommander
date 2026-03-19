#! /usr/bin/env python3

import unittest
import sys

def load_tests():
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()
  suite.addTests(loader.discover("packages/pycommander-core/tests", pattern="test_*.py", top_level_dir="."))
  suite.addTests(loader.discover("packages/pycommander-cli/tests",  pattern="test_*.py", top_level_dir="."))
  suite.addTests(loader.discover("packages/pycommander-gui/tests",  pattern="test_*.py", top_level_dir="."))
  suite.addTests(loader.discover("packages/pycommander/tests",      pattern="test_*.py", top_level_dir="."))
  return suite

if __name__ == "__main__":
  runner = unittest.TextTestRunner(verbosity=2)
  result = runner.run(load_tests())
  sys.exit(not result.wasSuccessful())
