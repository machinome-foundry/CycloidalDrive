"""Source-product groupings and authored V4 rest placements."""

# SPDX-FileCopyrightText: 2026 Luis Henrique Cassis Fagundes
# SPDX-License-Identifier: AGPL-3.0-or-later

from solid_node.node import AssemblyNode
from solid_node.motion.joints import Orbit, Revolute

from .layout import (
    DISC_PHASE,
    FRONT_DISC_CENTRE,
    FRONT_DISC_TRANSLATION,
    INPUT_AXIS,
    PULLEY_ROTATION,
    PULLEY_TRANSLATION,
    REAR_DISC_TRANSLATION,
    REAR_DISC_CENTRE,
)
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


class DriveShaft(AssemblyNode):
    bodies = [DriveShaftBody(index) for index in range(2)]


class Cam(AssemblyNode):
    bodies = [CamBody(index) for index in range(8)]


class InputStack(AssemblyNode):
    spin = Revolute(axis=INPUT_AXIS, range=(0.0, 7200.0), unit="deg")

    drive_shaft = DriveShaft()
    cam = Cam()
    pulley = ReducerPulleyBody(0)

    def render(self):
        angle, axis = PULLEY_ROTATION
        self.pulley.rotate(angle, axis)
        self.pulley.translate(PULLEY_TRANSLATION)


class FrontCycloidalDiscs(AssemblyNode):
    spin = Revolute(
        axis=INPUT_AXIS, at=FRONT_DISC_CENTRE, range=(-360.0, 0.0), unit="deg"
    )
    orbit = Orbit(
        axis=INPUT_AXIS,
        at=(0.0, 0.0, 0.0),
        carries=FRONT_DISC_CENTRE,
        range=(0.0, 7200.0),
        unit="deg",
    )

    bodies = [FrontCycloidalDiscBody(index) for index in range(2)]

    def render(self):
        for body in self.bodies:
            body.rotate(DISC_PHASE, (0.0, 1.0, 0.0))
            body.translate(FRONT_DISC_TRANSLATION)


class RearCycloidalDiscs(AssemblyNode):
    spin = Revolute(
        axis=INPUT_AXIS, at=REAR_DISC_CENTRE, range=(-360.0, 0.0), unit="deg"
    )
    orbit = Orbit(
        axis=INPUT_AXIS,
        at=(0.0, 0.0, 0.0),
        carries=REAR_DISC_CENTRE,
        range=(0.0, 7200.0),
        unit="deg",
    )

    bodies = [RearCycloidalDiscBody(index) for index in range(2)]

    def render(self):
        for body in self.bodies:
            body.rotate(DISC_PHASE, (0.0, 1.0, 0.0))
            body.translate(REAR_DISC_TRANSLATION)


class OutputStack(AssemblyNode):
    spin = Revolute(axis=INPUT_AXIS, range=(-360.0, 0.0), unit="deg")

    pins = [OutputPinBody(index) for index in range(6)]
    bearings = [OutputBearingBody(index) for index in range(12)]
    plate = OutputPlateBody()


class FixedRing(AssemblyNode):
    stations = [OuterStationBody(index) for index in range(14)]
    housing = RingHousingBody()
