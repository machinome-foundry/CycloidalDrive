## Context

The upstream project contains no source model or build instructions beyond its title and MIT licence. Its mechanical source is a set of STEP documents: V1-V4 of a cycloidal reducer and a separate strain-wave reducer. V4 is the newest revision and its document identifies an input shaft, eccentric cam, nested output assembly, two cycloidal discs, bearings, an HTD pulley assembly, and two anonymously named `COMPOUND` products.

The V4 document is an assembly, not a set of loose print files. A `solid import-step` survey shows that most products are authored at the document identity, that the transmission axis is +Y, that the pulley occurrence is rotated -90 degrees about X and translated to Y = 81 mm relative to its nested assembly (109 mm inside a parent placed at 190 mm), and that the discs share a -9 degree rest rotation about Y with opposing XZ translations `(-0.782172325, 0, -0.061558297)` and `(0.782172325, 0, 0.061558297)` mm. Radial measurement of the product geometry shows that each disc centre is 5 mm from the input axis; the smaller translations are the chord corrections that hold those eccentric centres while applying the authored -9 degree phase. Those occurrence values are evidence from the source document, not inferred dimensions.

The generated scaffold also reveals two import hazards: an identity-only nested assembly needs an explicit no-op body to remain valid Python, and the document has two different products both named `COMPOUND`, which the public `StepNode` selector correctly treats as ambiguous. The implementation must preserve an honest inventory rather than silently select one.

### Coordinates

- The machine frame is the V4 root-product frame.
- The reduction axis is +Y and the origin is the authored shaft/cam/bearing centreline.
- `input_angle` is degrees of positive rotation about +Y from the authored STEP pose.
- Disc orbit phase is measured about +Y from each disc's authored 5 mm eccentric offset. The two disc centres remain 180 degrees apart.
- Output angle is measured about +Y from the authored output pose and moves opposite the input at the measured 20:1 ratio of the one-pin-difference cycloidal stage.

## Goals / Non-Goals

**Goals:**

- Import every uniquely selectable V4 product without copying its geometry.
- Reproduce the authored occurrence placements and keep those transcriptions checked against a repeatable probe.
- Expose a single meaningful input control and derive all other rigid-body motion from it.
- Demonstrate home, one input revolution, and one output revolution with finite durations.
- Prove the bearing/shaft stack, opposed disc phasing, output coupling, motion ratio, connectivity, and the exact inventory of any source-authored overlaps.
- Record measurements and any ambiguity or interference found while assembling the source.

**Non-Goals:**

- V1-V3 and the independent strain-wave reducer.
- Redesigning or repairing upstream STEP geometry.
- Inventing omitted motors, fasteners, enclosure structure, loads, torque, compliance, or manufacturing tolerances that the repository does not document.
- Selecting either ambiguous `COMPOUND` product by guesswork. They remain a recorded upstream/import limitation unless an unambiguous public selector becomes available.

## Decisions

### Use V4 as the simulated machine

V4 is the latest committed cycloidal-drive revision and exposes the most detailed product inventory. Simulating every revision would create multiple machines and a comparison project the pilot did not request. Earlier revisions and `StrainWave` remain untouched.

### Import product geometry through `StepNode`

Each uniquely named product is represented by a thin `StepNode` with the original V4 file as `step_source` and a coarse `angular_deflection = 0.5` suitable for a filleted vendor-style document. This retains exact OCCT solids for certified contracts and lets the source file participate in rebuild tracking. Copying, re-exporting, or redrawing the products would create a second source of truth.

### Preserve occurrence evidence in `layout.py` and `docs/measurements.md`

The import scaffold's occurrence transforms and a repeatable probe are recorded before motion is added. A source-drift test compares the recorded inventory/placements with fresh probe output. This makes the necessarily transcribed matrix chain reviewable without reading private framework internals.

### Drive the mechanism from input angle only

The machine has one actuator-level meaning: input-shaft angle. Shaft, cam, and input pulley turn together. Each 5 mm-eccentric disc centre orbits at input speed, the discs remain opposed, and each disc counter-rotates at 1/20 input speed. The output follows that same reduced angle. The ratio is fixed by the measured 20-lobe disc and its one-pin-difference ring, not by a user knob. Per-part sliders would expose wiring rather than the machine.

### Treat source-authored home-pose interference as an inventory

The STEP document may model bearing fits or coincident solids with positive overlap. Initial exact checks will enumerate those pairs and volumes in `simulation/seats.py`; the root contract will require exactly that measured set. No epsilon or blanket exemption is introduced, so any new, changed, or removed overlap remains visible.

The imported disc tessellation proved non-manifold, so it cannot support a
faceted Boolean inventory through motion. The moving scenario instead samples
the derived ratio, opposed eccentric centres, and bounded disc/ring gap every
five seconds. This retains a meaningful moving contract without promoting a
mesh failure into a false collision-free claim.

### Keep the demonstration small

`Home` returns the authored pose, `One Input Revolution` shows the eccentric action, and `One Output Revolution` exposes the reduction. Instruction durations are based on a deliberately modest demonstration input rate recorded with the constants, not a claim about an undocumented motor.

## Findings

- The two discs are authored on equal-and-opposite 5 mm eccentric centres, providing direct evidence for their 180-degree balance phase. The approximately 0.78459 mm occurrence translations are chord corrections for the shared -9 degree rest phase, not the eccentric radius.
- Fourier analysis of the disc's measured radial profile has a dominant 20th harmonic and the rendered profile visibly carries 20 lobes. With the source's one-pin-difference ring this establishes a 20:1 reverse reduction.
- All observed drive-axis rotations are about +Y.
- The document contains two distinct products named `COMPOUND`; the public STEP selector cannot disambiguate them by name.
- The repository supplies no BOM, tooth/pin counts, motor speed, tolerance, or assembly narrative. Counts and clearances therefore have to be measured from geometry and documented as findings, while speed remains a stated demo-only choice.
- Exact home-pose checks find 20 positive-volume contacts, all between disc
  bodies and output pins or bearings. They are preserved pair-by-pair rather
  than waived.

## Risks / Trade-offs

- **Ambiguous `COMPOUND` products may hide housing or output geometry** → omit only those unselectable products, identify both omissions in the README and measurements, and do not claim a complete manufactured assembly.
- **Authored bearing fits may overlap exactly** → establish the exact overlap inventory before writing the integrity expectation.
- **A wrong lobe/pin count would publish a plausible but false ratio** → count both independently from geometry, record the readings, and make the motion contract recompute the reduction from those inputs.
- **STEP tessellation makes faceted checks expensive or noisy** → use `angular_deflection = 0.5` for the development loop and certify once on the exact kernel.
- **No upstream timing data exists** → label durations as demonstration timing and avoid performance claims.
