"""Source-derived V4 layout and kinematic constants.

All distances are millimetres and all angles are degrees.  The values are
guarded by ``CycloidalDriveTest.test_v4_source_digest`` and documented in
``docs/measurements.md``.
"""

# SPDX-FileCopyrightText: 2026 Luis Henrique Cassis Fagundes
# SPDX-License-Identifier: AGPL-3.0-or-later

from machinome.mechanics import cycloidal_ratio

SOURCE_SHA256 = "343b23d7e8ff4416e9a51121171a301fd77ce4353b371567bd1c0dfe15a18cc8"

INPUT_AXIS = (0.0, 1.0, 0.0)
DISC_PHASE = -9.0
DISC_ECCENTRICITY = 5.0
FRONT_DISC_CENTRE = (0.0, 0.0, -DISC_ECCENTRICITY)
REAR_DISC_CENTRE = (0.0, 0.0, DISC_ECCENTRICITY)
FRONT_DISC_TRANSLATION = (-0.782172325, 0.0, -0.061558297)
REAR_DISC_TRANSLATION = (0.782172325, 0.0, 0.061558297)

DISC_LOBES = 20
RING_PINS = 21
REDUCTION_RATIO = DISC_LOBES // (RING_PINS - DISC_LOBES)
OUTPUT_INPUT_RATIO = cycloidal_ratio(DISC_LOBES, RING_PINS)

PULLEY_ROTATION = (-90.0, (1.0, 0.0, 0.0))
PULLEY_TRANSLATION = (0.0, 81.0, 0.0)

SOURCE_PRODUCT_BODY_COUNTS = {
    "driveShaftInner": 2,
    "cam": 8,
    "8mm": 6,
    "bearing2287 (1)": 12,
    "cycDisc": 2,
    "cycDisc (2)": 2,
    "bearring8227": 14,
    "HTD 5M Pulley": 2,
}

# The two anonymous products cannot be selected by StepNode.  These guarded
# indices address the mechanically necessary bodies in the immutable root
# document: the output plate and the 21-scallop fixed ring housing.
OUTPUT_PLATE_SOLID_INDEX = 28
RING_HOUSING_SOLID_INDEX = 51

DEMO_INPUT_SPEED = 360.0  # deg/s, presentation timing only
ONE_INPUT_REVOLUTION = 360.0
ONE_OUTPUT_REVOLUTION = 360.0 * REDUCTION_RATIO
