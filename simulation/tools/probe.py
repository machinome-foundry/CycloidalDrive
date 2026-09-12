"""Measure the V4 STEP document without changing it.

The solid indices used below are guarded by the document SHA-256 and by each
solid's bounding box.  They identify the first front-disc body and the fixed
ring housing in this exact upstream document.  Run from the repository root:

    ../.venv/bin/python -m simulation.tools.probe
"""

# SPDX-FileCopyrightText: 2026 Luis Henrique Cassis Fagundes
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Measurements derive from the upstream V4 STEP document. The document and its
# geometry remain MIT-licensed upstream material; see ../../NOTICE.

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import cadquery as cq
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "V4" / "Cycloidal_V4_02.stp"
EXPECTED_SHA256 = "343b23d7e8ff4416e9a51121171a301fd77ce4353b371567bd1c0dfe15a18cc8"
DISC_SOLID_INDEX = 31
RING_SOLID_INDEX = 51


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _dominant_radial_harmonic(
    solid: cq.Shape,
    *,
    centre: tuple[float, float],
    radial_limit: float | None = None,
    take_minimum: bool = False,
) -> int:
    vertices, _ = solid.tessellate(0.1, 0.15)
    points = np.asarray([vertex.toTuple() for vertex in vertices])
    x = points[:, 0] - centre[0]
    z = points[:, 2] - centre[1]
    radii = np.hypot(x, z)
    if radial_limit is not None:
        selected = radii < radial_limit
        x, z, radii = x[selected], z[selected], radii[selected]

    angles = (np.arctan2(z, x) + 2 * np.pi) % (2 * np.pi)
    edges = np.linspace(0, 2 * np.pi, 721)
    profile = []
    for index in range(720):
        bucket = radii[(angles >= edges[index]) & (angles < edges[index + 1])]
        if len(bucket) == 0:
            profile.append(np.nan)
        elif take_minimum:
            profile.append(bucket.min())
        else:
            profile.append(bucket.max())

    profile_array = np.asarray(profile)
    known = np.flatnonzero(~np.isnan(profile_array))
    profile_array = np.interp(
        np.arange(len(profile_array)), known, profile_array[known], period=len(profile_array)
    )
    spectrum = np.abs(np.fft.rfft(profile_array - profile_array.mean()))
    band = spectrum[2:100]
    # The rounded lobes carry a strong second harmonic.  Select the lowest
    # fundamental whose amplitude is at least 75% of the strongest response.
    strong = np.flatnonzero(band >= 0.75 * band.max()) + 2
    return int(strong.min())


def _import_scaffold() -> tuple[list[str], list[str]]:
    solid = Path(sys.executable).with_name("solid")
    with tempfile.TemporaryDirectory(prefix="cycloidal-probe-") as temporary:
        target = Path(temporary) / "simulation"
        subprocess.run(
            [
                str(solid),
                "import-step",
                str(SOURCE),
                "--into",
                str(target),
                "--model",
                "CycloidalDrive",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        assembly = (target / "assembly.py").read_text()
        parts = (target / "parts.py").read_text()
    transforms = [
        line.strip()
        for line in assembly.splitlines()
        if ".rotate(" in line or ".translate(" in line
    ]
    selectors = re.findall(r"part = '([^']*)'", parts)
    return transforms, selectors


def measure() -> dict[str, object]:
    source_hash = _sha256(SOURCE)
    if source_hash != EXPECTED_SHA256:
        raise RuntimeError(
            "V4 STEP changed; review solid indices and measurements before updating the guard"
        )

    text = SOURCE.read_text(errors="replace")
    products = re.findall(r"PRODUCT\('([^']*)'", text)
    transforms, selectors = _import_scaffold()
    document = cq.importers.importStep(str(SOURCE)).val()
    solids = document.Solids()

    disc = solids[DISC_SOLID_INDEX]
    disc_bounds = disc.BoundingBox()
    disc_centre = (
        (disc_bounds.xmin + disc_bounds.xmax) / 2,
        (disc_bounds.zmin + disc_bounds.zmax) / 2,
    )
    disc_lobes = _dominant_radial_harmonic(disc, centre=disc_centre)
    ring_pins = _dominant_radial_harmonic(
        solids[RING_SOLID_INDEX],
        centre=(0.0, 0.0),
        radial_limit=115.0,
        take_minimum=True,
    )

    bounds = document.BoundingBox()
    return {
        "source": str(SOURCE.relative_to(ROOT)),
        "sha256": source_hash,
        "products": products,
        "generated_selectors": selectors,
        "duplicate_selectors": sorted(
            {name for name in selectors if selectors.count(name) > 1}
        ),
        "solid_count": len(solids),
        "bounds_mm": [bounds.xlen, bounds.ylen, bounds.zlen],
        "disc_lobes": disc_lobes,
        "ring_pins": ring_pins,
        "reduction_ratio": disc_lobes,
        "scaffold_transforms": transforms,
    }


def main() -> None:
    print(json.dumps(measure(), indent=2))


if __name__ == "__main__":
    main()
