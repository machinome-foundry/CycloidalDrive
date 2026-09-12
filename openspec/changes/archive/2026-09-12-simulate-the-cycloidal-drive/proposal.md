## Why

The repository publishes assembled STEP geometry but no executable machine, so a maker cannot inspect how the eccentric input, paired cycloidal discs, and output member move together or prove that their interfaces remain aligned. A simulation of the latest V4 design makes those mechanical relationships visible and testable without altering the upstream CAD.

## What Changes

- Add a thin `simulation/` package that imports the V4 STEP products in their authored frames and assembles the drive from the document's own occurrence placements.
- Expose one `input_angle` driver in builder terms and derive the eccentric-disc and reduced-output motion from the measured tooth/pin relationship.
- Add a small demonstration consisting of `Home`, `One Input Revolution`, and `One Output Revolution` instructions.
- Give the imported parts material-oriented colours and publish concise build, test, and operation instructions.
- Add mechanical contracts for the input stack, cycloidal engagement, output engagement, reduction law, printed-solid integrity, and interference behavior across the demonstration.

## Capabilities

### New Capabilities

- `cycloidal-drive-assembly`: The V4 shaft, cam, bearings, paired discs, output member, pulley, and surrounding hardware are present and seated according to the authored STEP assembly.
- `cycloidal-drive-motion`: One input-angle control drives the eccentric and counter-phased discs and produces the source-derived reduced output motion through demonstrable instructions.

### Modified Capabilities

None.

## Impact

The change adds a project manifest, a `simulation/` Python package and tests, project-owned OpenSpec records, README operating notes, and ignore rules for generated artifacts. It depends on the workspace's installed solid-node stack and the existing `V4/Cycloidal_V4_02.stp`; it does not modify any STEP file, simulate V1-V3 or `StrainWave`, replace authored product geometry, or fetch third-party geometry.
