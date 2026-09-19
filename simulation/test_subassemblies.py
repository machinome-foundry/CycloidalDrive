"""Connectivity smoke contracts for every subassembly node."""

# SPDX-FileCopyrightText: 2026 Luis Henrique Cassis Fagundes
# SPDX-License-Identifier: AGPL-3.0-or-later

from machinome.test import TestCase

from .subassemblies import (
    Cam,
    DriveShaft,
    FixedRing,
    FrontCycloidalDiscs,
    InputStack,
    OutputStack,
    RearCycloidalDiscs,
)


class _ConnectedAssemblyTest(TestCase):
    node = DriveShaft

    def test_bodies_are_connected(self):
        self.assertNoDisconnectedSolids(self.node)


class DriveShaftTest(_ConnectedAssemblyTest):
    node = DriveShaft


class CamTest(_ConnectedAssemblyTest):
    node = Cam


class InputStackTest(_ConnectedAssemblyTest):
    node = InputStack


class FrontCycloidalDiscsTest(_ConnectedAssemblyTest):
    node = FrontCycloidalDiscs


class RearCycloidalDiscsTest(_ConnectedAssemblyTest):
    node = RearCycloidalDiscs


class OutputStackTest(_ConnectedAssemblyTest):
    node = OutputStack


class FixedRingTest(_ConnectedAssemblyTest):
    node = FixedRing
