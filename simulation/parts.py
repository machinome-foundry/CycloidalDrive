"""Connected rigid bodies imported from the V4 STEP document."""

# SPDX-FileCopyrightText: 2026 Luis Henrique Cassis Fagundes
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# This adapter uses the upstream V4 STEP document. That document and its
# exported geometry remain MIT-licensed upstream material; see ../NOTICE.

from pathlib import Path

import cadquery as cq

from machinome.node import CadQueryNode, StepNode

from .layout import OUTPUT_PLATE_SOLID_INDEX, RING_HOUSING_SOLID_INDEX


SOURCE = Path(__file__).resolve().parents[1] / "V4" / "Cycloidal_V4_02.stp"


class _ProductBody(StepNode):
    """One connected body selected from a named multi-body STEP product."""

    angular_deflection = 0.5

    def __init__(self, body_index: int = 0, name: str | None = None):
        self.body_index = body_index
        super().__init__(body_index=body_index, name=name)

    def adjust(self, shape):
        solids = shape.Solids()
        if not 0 <= self.body_index < len(solids):
            raise ValueError(
                f"{type(self).__name__} body {self.body_index} is outside "
                f"the source inventory of {len(solids)} solids"
            )
        return solids[self.body_index]


class DriveShaftBody(_ProductBody):
    step_source = "../V4/Cycloidal_V4_02.stp"
    part = "driveShaftInner"
    color = "#B8BDC4"


class CamBody(_ProductBody):
    step_source = "../V4/Cycloidal_V4_02.stp"
    part = "cam"
    color = "#D5A021"


class OutputPinBody(_ProductBody):
    step_source = "../V4/Cycloidal_V4_02.stp"
    part = "8mm"
    color = "#B8BDC4"


class OutputBearingBody(_ProductBody):
    step_source = "../V4/Cycloidal_V4_02.stp"
    part = "bearing2287 (1)"
    color = "#777D85"


class FrontCycloidalDiscBody(_ProductBody):
    step_source = "../V4/Cycloidal_V4_02.stp"
    part = "cycDisc"
    color = "#E5723A"


class RearCycloidalDiscBody(_ProductBody):
    step_source = "../V4/Cycloidal_V4_02.stp"
    part = "cycDisc (2)"
    color = "#F0A04B"


class OuterStationBody(_ProductBody):
    step_source = "../V4/Cycloidal_V4_02.stp"
    part = "bearring8227"
    color = "#60666E"


class ReducerPulleyBody(_ProductBody):
    step_source = "../V4/Cycloidal_V4_02.stp"
    part = "HTD 5M Pulley"
    color = "#3678B5"


class _GuardedDocumentBody(CadQueryNode):
    """One necessary body from an ambiguously named source product."""

    angular_deflection = 0.5
    solid_index: int
    expected_bounds: tuple[float, float, float]

    def render(self):
        solid = cq.importers.importStep(str(SOURCE)).val().Solids()[self.solid_index]
        bounds = solid.BoundingBox()
        measured = (bounds.xlen, bounds.ylen, bounds.zlen)
        for actual, expected in zip(measured, self.expected_bounds):
            if abs(actual - expected) > 0.01:
                raise ValueError(
                    f"source solid {self.solid_index} bounds changed: "
                    f"expected {self.expected_bounds}, found {measured}"
                )
        return cq.Workplane(obj=solid)


class OutputPlateBody(_GuardedDocumentBody):
    solid_index = OUTPUT_PLATE_SOLID_INDEX
    expected_bounds = (180.0, 17.0, 180.0)
    color = "#497EAA"


class RingHousingBody(_GuardedDocumentBody):
    solid_index = RING_HOUSING_SOLID_INDEX
    expected_bounds = (260.0, 81.0, 247.0)
    color = "#4A5058"
