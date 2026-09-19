"""Mechanical contracts for the complete V4 cycloidal drive."""

# SPDX-FileCopyrightText: 2026 Luis Henrique Cassis Fagundes
# SPDX-License-Identifier: AGPL-3.0-or-later

import hashlib
import os
from pathlib import Path
from itertools import combinations

import trimesh

from machinome.simulation import ScenarioTest
from machinome.test import TestCase

from .layout import (
    DISC_ECCENTRICITY,
    FRONT_DISC_TRANSLATION,
    REAR_DISC_TRANSLATION,
    REDUCTION_RATIO,
    SOURCE_SHA256,
)
from .machine import CycloidalDrive
from .seats import EXPECTED_OVERLAPS


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "V4" / "Cycloidal_V4_02.stp"


class CycloidalDriveTest(TestCase):
    node = CycloidalDrive

    def test_v4_source_digest(self):
        self.assertEqual(hashlib.sha256(SOURCE.read_bytes()).hexdigest(), SOURCE_SHA256)

    def test_source_derived_layout(self):
        self.assertEqual(FRONT_DISC_TRANSLATION, (-0.782172325, 0.0, -0.061558297))
        self.assertEqual(REAR_DISC_TRANSLATION, (0.782172325, 0.0, 0.061558297))
        self.assertAlmostEqual(DISC_ECCENTRICITY, 5.0, delta=0.01)
        self.assertEqual(REDUCTION_RATIO, 20)

    def test_solid_integrity(self):
        self.node.set_state(input_angle=0.0)
        self.assertNoDisconnectedSolids(self.node)

    def test_assembly_integrity(self):
        self.node.set_state(input_angle=0.0)
        if os.environ.get("SOLID_TEST_KERNEL") == "exact":
            groups = {
                "shaft": self.node.input_stack.drive_shaft.bodies,
                "cam": self.node.input_stack.cam.bodies,
                "pulley": [self.node.input_stack.pulley],
                "front": self.node.front_discs.bodies,
                "rear": self.node.rear_discs.bodies,
                "pin": self.node.output_stack.pins,
                "bearing": self.node.output_stack.bearings,
                "output_plate": [self.node.output_stack.plate],
                "station": self.node.fixed_ring.stations,
                "housing": [self.node.fixed_ring.housing],
            }
            parts = [
                (f"{group}-{index}", body)
                for group, bodies in groups.items()
                for index, body in enumerate(bodies)
            ]
            overlaps = []
            for (name_a, body_a), (name_b, body_b) in combinations(parts, 2):
                expected = EXPECTED_OVERLAPS.get((name_a, name_b))
                if expected is None:
                    self.assertNotIntersecting(body_a, body_b)
                else:
                    self.assertIntersectVolumeAbove(body_a, body_b, expected - 0.01)
                    self.assertIntersectVolumeBelow(body_a, body_b, expected + 0.01)

    def test_input_reference_axis(self):
        self.node.set_state(input_angle=0.0)
        reference_bodies = [
            *self.node.input_stack.drive_shaft.bodies,
            *self.node.input_stack.cam.bodies[5:],
        ]
        for body in reference_bodies:
            bounds = body.mesh.bounds
            centre_x = (bounds[0][0] + bounds[1][0]) / 2
            centre_z = (bounds[0][2] + bounds[1][2]) / 2
            self.assertAlmostEqual(centre_x, 0.0, delta=0.01)
            self.assertAlmostEqual(centre_z, 0.0, delta=0.01)

    @staticmethod
    def _radial_bounds_centre(body):
        bounds = body.mesh.bounds
        return (
            (bounds[0][0] + bounds[1][0]) / 2,
            (bounds[0][2] + bounds[1][2]) / 2,
        )

    def test_disc_centres_are_opposed(self):
        self.node.set_state(input_angle=0.0)
        front = self._radial_bounds_centre(self.node.front_discs.bodies[0])
        rear = self._radial_bounds_centre(self.node.rear_discs.bodies[0])
        self.assertAlmostEqual((front[0] + rear[0]) / 2, 0.0, delta=0.01)
        self.assertAlmostEqual((front[1] + rear[1]) / 2, 0.0, delta=0.01)
        self.assertAlmostEqual((front[0] ** 2 + front[1] ** 2) ** 0.5, 5.0, delta=0.01)
        self.assertAlmostEqual((rear[0] ** 2 + rear[1] ** 2) ** 0.5, 5.0, delta=0.01)

    def test_cycloidal_ring_engagement(self):
        self.node.set_state(input_angle=0.0)
        for disc in (self.node.front_discs.bodies[0], self.node.rear_discs.bodies[0]):
            distances = trimesh.proximity.closest_point(
                self.node.fixed_ring.housing.mesh, disc.mesh.vertices
            )[1]
            minimum_gap = float(distances.min())
            self.assertGreater(minimum_gap, 0.8)
            self.assertLess(minimum_gap, 1.0)
            if os.environ.get("SOLID_TEST_KERNEL") == "exact":
                self.assertNotIntersecting(disc, self.node.fixed_ring.housing)

    def test_output_pin_and_bearing_sites_are_coaxial(self):
        self.node.set_state(input_angle=0.0)
        pin_sites = [
            tuple(round(value, 2) for value in self._radial_bounds_centre(pin))
            for pin in self.node.output_stack.pins
        ]
        bearing_sites = [
            tuple(round(value, 2) for value in self._radial_bounds_centre(bearing))
            for bearing in self.node.output_stack.bearings
        ]
        for site in pin_sites:
            self.assertEqual(bearing_sites.count(site), 2)

    def test_output_plate_is_on_reduction_axis(self):
        self.node.set_state(input_angle=0.0)
        centre_x, centre_z = self._radial_bounds_centre(self.node.output_stack.plate)
        # The faceted bounding box shifts by up to 0.16 mm after reversible
        # driven transforms; 0.25 mm still catches the proven 1 mm mutation.
        self.assertAlmostEqual(centre_x, 0.0, delta=0.25)
        self.assertAlmostEqual(centre_z, 0.0, delta=0.25)

    def test_one_input_revolution_relations(self):
        self.node.set_state(input_angle=360.0)
        self.assertAlmostEqual(self.node.input_stack.spin.value, 360.0)
        self.assertAlmostEqual(self.node.front_discs.orbit.value, 360.0)
        self.assertAlmostEqual(self.node.rear_discs.orbit.value, 360.0)
        self.assertAlmostEqual(self.node.front_discs.spin.value, -18.0)
        self.assertAlmostEqual(self.node.rear_discs.spin.value, -18.0)
        self.assertAlmostEqual(self.node.output_stack.spin.value, -18.0)

    def test_driven_disc_centres_remain_balanced(self):
        self.node.set_state(input_angle=90.0)
        front = self._radial_bounds_centre(self.node.front_discs.bodies[0])
        rear = self._radial_bounds_centre(self.node.rear_discs.bodies[0])
        self.assertAlmostEqual((front[0] + rear[0]) / 2, 0.0, delta=0.01)
        self.assertAlmostEqual((front[1] + rear[1]) / 2, 0.0, delta=0.01)
        self.assertAlmostEqual((front[0] ** 2 + front[1] ** 2) ** 0.5, 5.0, delta=0.01)
        self.assertAlmostEqual((rear[0] ** 2 + rear[1] ** 2) ** 0.5, 5.0, delta=0.01)

    def test_instruction_targets(self):
        self.assertEqual(
            set(CycloidalDrive.instructions),
            {"Home", "One Input Revolution", "One Output Revolution"},
        )


class CycloidalDriveScenarioTest(ScenarioTest):
    node = CycloidalDrive
    dt = 1.0
    meshes = True

    def test_complete_demonstration_lands_on_targets(self):
        sim = self.simulation()

        def assert_sampled_motion():
            expected_output = -sim.state["input_angle"] / REDUCTION_RATIO
            self.assertAlmostEqual(self.node.front_discs.spin.value, expected_output)
            self.assertAlmostEqual(self.node.rear_discs.spin.value, expected_output)
            self.assertAlmostEqual(self.node.output_stack.spin.value, expected_output)

            front = CycloidalDriveTest._radial_bounds_centre(
                self.node.front_discs.bodies[0]
            )
            rear = CycloidalDriveTest._radial_bounds_centre(
                self.node.rear_discs.bodies[0]
            )
            self.assertAlmostEqual((front[0] + rear[0]) / 2, 0.0, delta=0.01)
            self.assertAlmostEqual((front[1] + rear[1]) / 2, 0.0, delta=0.01)

            for disc in (
                self.node.front_discs.bodies[0],
                self.node.rear_discs.bodies[0],
            ):
                distances = trimesh.proximity.closest_point(
                    self.node.fixed_ring.housing.mesh, disc.mesh.vertices
                )[1]
                self.assertGreater(float(distances.min()), 0.8)
                self.assertLess(float(distances.min()), 1.0)

        # Five seconds is 1/4 of the long instruction duration and keeps the
        # expensive mesh-proximity checks to eight samples over this demo.
        sim.every(5.0, assert_sampled_motion)
        sim.at(0.0).trigger("One Input Revolution")
        sim.run(1.0)
        self.assertEqual(sim.state["input_angle"], 360.0)
        sim.at(sim.time).trigger("One Output Revolution")
        sim.run(20.0)
        self.assertEqual(sim.state["input_angle"], 7200.0)
        sim.at(sim.time).trigger("Home")
        sim.run(20.0)
        self.assertEqual(sim.state["input_angle"], 0.0)
        self.assertEqual(sim.assertion_stats[0], 8)
