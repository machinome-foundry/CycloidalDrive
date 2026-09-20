"""Lightweight parity proof for the cycloidal-drive relation migration.

Run from the repository root with this project and the selected
machinome-mechanics source worktree on ``PYTHONPATH``.
"""

# SPDX-FileCopyrightText: 2026 Luis Henrique Cassis Fagundes
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# This verification records the upstream V4 design relation. Its source-derived
# measurements and geometry remain MIT-licensed upstream material; see ../../NOTICE.

from math import isclose

from machinome.core.expressions import parse, render
from machinome.scad_expression import get_animation_time

from simulation.layout import (
    DISC_LOBES,
    ONE_OUTPUT_REVOLUTION,
    OUTPUT_INPUT_RATIO,
    REDUCTION_RATIO,
    RING_PINS,
)
from simulation.machine import ActuatedCycloidalDrive, CycloidalDrive


STATE_SAMPLES = (0.0, 1.0, 360.0, 1890.0, 7199.0, 7200.0)
LAW_SAMPLES = (-7200.0, -360.0, 0.0, 360.0, 1890.0, 7200.0)


def legacy_output(input_angle):
    """Independent pre-migration oracle; intentionally does not use the helper."""
    return -input_angle / REDUCTION_RATIO


def evaluate(expression, animation_time):
    source = render(parse(str(expression))).replace("$t", repr(animation_time))
    return eval(source, {"__builtins__": {}}, {})


def equal(actual, expected):
    return isclose(actual, expected, rel_tol=1e-12, abs_tol=1e-12)


def check_node(node_class):
    node = node_class()
    relations = tuple(node._relations)
    assert len(relations) == 6
    assert tuple(relation.law.ratio for relation in relations[:3]) == (1, 1, 1)
    assert tuple(relation.law.ratio for relation in relations[3:]) == (
        OUTPUT_INPUT_RATIO,
        OUTPUT_INPUT_RATIO,
        OUTPUT_INPUT_RATIO,
    )

    # Actual machine state keeps the project's declared 0..7200-degree guard.
    for input_angle in STATE_SAMPLES:
        node.set_state(input_angle=input_angle)
        expected_output = legacy_output(input_angle)
        assert equal(node.input_stack.spin.value, input_angle)
        assert equal(node.front_discs.orbit.value, input_angle)
        assert equal(node.rear_discs.orbit.value, input_angle)
        assert equal(node.front_discs.spin.value, expected_output)
        assert equal(node.rear_discs.spin.value, expected_output)
        assert equal(node.output_stack.spin.value, expected_output)

    time = get_animation_time()
    for relation in relations[3:]:
        deferred = relation.law.forward(time)
        # The underlying law stays signed and unwrapped independently of that guard.
        for sample in LAW_SAMPLES:
            assert equal(evaluate(deferred, sample), legacy_output(sample))


assert (DISC_LOBES, RING_PINS) == (20, 21)
assert REDUCTION_RATIO == 20
assert OUTPUT_INPUT_RATIO == -0.05
assert ONE_OUTPUT_REVOLUTION == 7200.0
check_node(CycloidalDrive)
check_node(ActuatedCycloidalDrive)
print("PASS: 12 actual production states and 36 deferred relation evaluations")
