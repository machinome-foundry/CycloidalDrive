# CycloidalDrive

This repository now includes a machinome simulation of the latest cycloidal
revision, `V4/Cycloidal_V4_02.stp`. The simulation imports the original STEP
geometry, preserves its authored placements, and drives the complete reducer
from one `input_angle` control.

## Run the simulation

Use a machinome checkout or environment that provides the `solid` command,
then run these commands from the repository root:

```sh
machinome build
machinome develop
```

The viewer exposes one control, `input_angle`, from 0 to 7200 degrees. The
input shaft, cam, and reducer pulley follow it directly. The opposed 5 mm
eccentric discs orbit at input speed while the discs and output turn in the
opposite direction at the measured 20:1 reduction.

The useful viewing sequence is:

1. Select `Home` to restore the authored STEP pose.
2. Select `One Input Revolution` to see one eccentric cycle and -18 degrees
   of disc/output rotation.
3. Select `One Output Revolution` to run 20 input revolutions and one reverse
   output revolution.

The 1-second and 20-second instruction durations are presentation timing, not
a motor-speed claim.

## Verify it

The fast development regression covers every simulation node file:

```sh
SOLID_TEST_KERNEL=faceted machinome test --faceted simulation/parts.py
SOLID_TEST_KERNEL=faceted machinome test --faceted simulation/subassemblies.py
SOLID_TEST_KERNEL=faceted machinome test --faceted simulation/machine.py
machinome build
```

Run the exact certification once when the source or contracts change:

```sh
SOLID_TEST_KERNEL=exact machinome test --exact simulation/parts.py
SOLID_TEST_KERNEL=exact machinome test --exact simulation/subassemblies.py
SOLID_TEST_KERNEL=exact machinome test --exact simulation/machine.py
```

`python -m simulation.tools.probe` repeats the source inventory and radial
profile measurements. Detailed source readings and mutation evidence are in
[`docs/measurements.md`](docs/measurements.md).

## Scope and findings

- The model includes 49 rigid bodies: the reducer-side input stack and pulley,
  paired discs, output pins/bearings/plate, and fixed ring/stations.
- V1-V3, the separate strain-wave design, the remote pulley, motor, and
  anonymous frame bodies are outside this simulation.
- The V4 STEP has two products both named `COMPOUND`. Because a product-name
  selector cannot distinguish them, the necessary output plate and ring
  housing are guarded by the V4 file digest, exact solid index, and bounds;
  no anonymous product is selected by a guessed name.
- Exact home-pose certification preserves 20 positive-volume source-authored
  disc/output overlaps instead of describing the source as interference-free.
  Their pairwise volumes are recorded in `simulation/seats.py`.
- The source disc tessellation is non-manifold. Exact STEP solids therefore
  certify the home overlap inventory; the faceted moving scenario samples the
  20:1 relation, opposed disc centres, and bounded disc/ring gap every five
  seconds.

Generated `_build/` artifacts and snapshots are intentionally ignored.

## Licensing

The original CycloidalDrive materials are by James Bruton, from
<https://github.com/XRobots/CycloidalDrive>, and remain available under the
MIT License in the root [`LICENSE`](LICENSE). This includes the V4 CAD and
other upstream files and exports.

The original simulation software, supporting documentation and tools added in
this repository are Copyright (C) 2026 Luis Henrique Cassis Fagundes and are
licensed under the GNU Affero General Public License, version 3 or later
(`AGPL-3.0-or-later`); its text is in
[`simulation/LICENSE`](simulation/LICENSE). The simulation reads and measures
MIT-licensed upstream material and does not claim ownership of that design or
its exported geometry. See [`CREDITS`](CREDITS), [`NOTICE`](NOTICE), and
[`simulation/README.md`](simulation/README.md) for the exact scopes and
attribution.
