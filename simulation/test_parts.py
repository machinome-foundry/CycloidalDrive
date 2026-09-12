"""Build and connectivity smoke contracts for every concrete part node."""

# SPDX-FileCopyrightText: 2026 Luis Henrique Cassis Fagundes
# SPDX-License-Identifier: AGPL-3.0-or-later

from solid_node.test import TestCase

from .parts import (
    CamBody,
    DriveShaftBody,
    FrontCycloidalDiscBody,
    OuterStationBody,
    OutputBearingBody,
    OutputPinBody,
    OutputPlateBody,
    RearCycloidalDiscBody,
    ReducerPulleyBody,
    RingHousingBody,
)


class _ConnectedPartTest(TestCase):
    node = DriveShaftBody

    def test_body_is_connected(self):
        self.assertNoDisconnectedSolids(self.node)


class DriveShaftBodyTest(_ConnectedPartTest):
    node = DriveShaftBody


class CamBodyTest(_ConnectedPartTest):
    node = CamBody


class OutputPinBodyTest(_ConnectedPartTest):
    node = OutputPinBody


class OutputBearingBodyTest(_ConnectedPartTest):
    node = OutputBearingBody


class FrontCycloidalDiscBodyTest(_ConnectedPartTest):
    node = FrontCycloidalDiscBody


class RearCycloidalDiscBodyTest(_ConnectedPartTest):
    node = RearCycloidalDiscBody


class OuterStationBodyTest(_ConnectedPartTest):
    node = OuterStationBody


class ReducerPulleyBodyTest(_ConnectedPartTest):
    node = ReducerPulleyBody


class OutputPlateBodyTest(_ConnectedPartTest):
    node = OutputPlateBody


class RingHousingBodyTest(_ConnectedPartTest):
    node = RingHousingBody
