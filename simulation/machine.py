"""V4 cycloidal-drive assembly, built from the source document upward."""

# SPDX-FileCopyrightText: 2026 Luis Henrique Cassis Fagundes
# SPDX-License-Identifier: AGPL-3.0-or-later

from machinome.node.assembly import AssemblyNode
from machinome.simulation import Driver, Instruction

from .layout import (
    DEMO_INPUT_SPEED,
    ONE_INPUT_REVOLUTION,
    ONE_OUTPUT_REVOLUTION,
    OUTPUT_INPUT_RATIO,
)

from .subassemblies import (
    FixedRing,
    FrontCycloidalDiscs,
    InputStack,
    OutputStack,
    RearCycloidalDiscs,
)


class CycloidalDrive(AssemblyNode):
    """The currently assembled V4 mechanism."""

    input_angle = Driver(
        default=0.0, range=(0.0, ONE_OUTPUT_REVOLUTION), unit="deg"
    )

    input_stack = InputStack()
    front_discs = FrontCycloidalDiscs()
    rear_discs = RearCycloidalDiscs()
    output_stack = OutputStack()
    fixed_ring = FixedRing()

    input_angle.drives(input_stack.spin)
    input_angle.drives(front_discs.orbit)
    input_angle.drives(rear_discs.orbit)
    input_angle.drives(front_discs.spin, ratio=OUTPUT_INPUT_RATIO)
    input_angle.drives(rear_discs.spin, ratio=OUTPUT_INPUT_RATIO)
    input_angle.drives(output_stack.spin, ratio=OUTPUT_INPUT_RATIO)

    instructions = {
        "Home": Instruction(
            {"input_angle": 0.0}, duration=ONE_OUTPUT_REVOLUTION / DEMO_INPUT_SPEED
        ),
        "One Input Revolution": Instruction(
            {"input_angle": ONE_INPUT_REVOLUTION},
            duration=ONE_INPUT_REVOLUTION / DEMO_INPUT_SPEED,
        ),
        "One Output Revolution": Instruction(
            {"input_angle": ONE_OUTPUT_REVOLUTION},
            duration=ONE_OUTPUT_REVOLUTION / DEMO_INPUT_SPEED,
        ),
    }


class ActuatedCycloidalDrive(AssemblyNode):
    """Fixed 1890-degree driver default used only for visual evidence."""

    input_angle = Driver(
        default=1890.0, range=(0.0, ONE_OUTPUT_REVOLUTION), unit="deg"
    )

    input_stack = InputStack()
    front_discs = FrontCycloidalDiscs()
    rear_discs = RearCycloidalDiscs()
    output_stack = OutputStack()
    fixed_ring = FixedRing()

    input_angle.drives(input_stack.spin)
    input_angle.drives(front_discs.orbit)
    input_angle.drives(rear_discs.orbit)
    input_angle.drives(front_discs.spin, ratio=OUTPUT_INPUT_RATIO)
    input_angle.drives(rear_discs.spin, ratio=OUTPUT_INPUT_RATIO)
    input_angle.drives(output_stack.spin, ratio=OUTPUT_INPUT_RATIO)
