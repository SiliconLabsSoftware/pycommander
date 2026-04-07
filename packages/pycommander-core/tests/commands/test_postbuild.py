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

import unittest

from ..mock_commander import MockCommander


class TestPostbuild(unittest.TestCase):
  def test_postbuild_command(self):
    commander = MockCommander()
    commander.postbuild.postbuild("tasks.slpb")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "postbuild", "tasks.slpb", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_postbuild_command_with_device(self):
    commander = MockCommander()
    commander.postbuild.postbuild("tasks.slpb", device="EFR32MG24")
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = ["mock", "postbuild", "tasks.slpb", "--device", "EFR32MG24", "--json"]
    self.assertEqual(commander._runner.logged_commands[0], expected)

  def test_postbuild_command_with_parameters_and_dryrun(self):
    commander = MockCommander()
    commander.postbuild.postbuild(
      "tasks.slpb",
      parameters=[("VAR1", "val1"), ("VAR2", "val2")],
      dryrun=True,
    )
    self.assertEqual(len(commander._runner.logged_commands), 1)
    expected = [
      "mock", "postbuild", "tasks.slpb",
      "--parameter", "VAR1:val1", "--parameter", "VAR2:val2", "--dryrun",
      "--json",
    ]
    self.assertEqual(commander._runner.logged_commands[0], expected)
