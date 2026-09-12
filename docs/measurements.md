# V4 source measurements

These readings describe `V4/Cycloidal_V4_02.stp` at SHA-256
`343b23d7e8ff4416e9a51121171a301fd77ce4353b371567bd1c0dfe15a18cc8`.
They were taken with `python -m simulation.tools.probe`; the tool refuses to
reuse its solid indices if that source digest changes.

## Document inventory

- Root product: `Cycloidal V4_02`
- Overall bounds: 434 x 188 x 248 mm
- Exact solids in the root document: 59
- Named products used by the reducer: `driveShaftInner`, `cam`, `output`,
  `8mm`, `bearing2287 (1)`, `cycDisc`, `cycDisc (2)`, `bearring8227`,
  `HTD 5M - 50 v2`, and `HTD 5M Pulley`
- Ambiguity: two distinct products are both named `COMPOUND`. `StepNode`
  cannot choose between them by product name. The simulation therefore uses
  guarded whole-document solid selections only for the output plate and fixed
  ring housing that are mechanically necessary; it does not guess at the
  other anonymous bodies.

The named product bodies measured through exact `StepNode` selection are:

| Product | Solid bodies | Relevant reading |
| --- | ---: | --- |
| `driveShaftInner` | 2 | coaxial, 65 mm diameter bodies |
| `cam` | 8 | coaxial input/cam stack |
| `8mm` | 6 | six output pins at about 69 mm radius |
| `bearing2287 (1)` | 12 | paired 22 mm bearings at the six output sites |
| `cycDisc` | 2 | front disc pair, 20-lobe radial profile |
| `cycDisc (2)` | 2 | rear disc pair, same profile in opposite eccentric position |
| `bearring8227` | 14 | seven outer stations, each with a bearing and shaft body |
| `HTD 5M Pulley` | 2 | reducer pulley and remote motor pulley; only the reducer pulley is in scope |

## Authored occurrence placement

The generated STEP scaffold reports:

- Both cycloidal products rotate -9 degrees about +Y.
- Front translation: `(-0.782172325, 0, -0.061558297)` mm.
- Rear translation: `(0.782172325, 0, 0.061558297)` mm.
- The pulley product rotates -90 degrees about +X, translates -109 mm in its
  nested assembly, then that assembly translates +190 mm in Y. The resulting
  direct placement is +81 mm in Y.

The disc product geometry is already authored on centres 5 mm either side of
the input axis. Applying the -9 degree phase would move those centres; the
0.78459 mm translations are the chord corrections that return them to
`(0, 0, -5)` and `(0, 0, 5)` mm. They are not the eccentricity.

## Reduction

The first front-disc solid's radial profile has a dominant 20th Fourier
harmonic. The fixed ring housing's inner profile has a dominant 21st harmonic.
The source therefore carries 20 disc lobes against 21 ring pins, establishing
a 20:1 reduction with output rotation opposite the input.

## Deliberate model boundary

The simulation models the reducer mechanism, its fixed ring, its output plate,
and the reducer-side input pulley. It omits the remote pulley and the remaining
anonymous frame/motor bodies because the repository gives neither their
kinematic relationship nor unambiguous product selectors. No omitted geometry
is silently represented as part of the validated reducer.

## Contract mutation evidence

- Translating the input shaft 1 mm off +Y makes
  `test_input_reference_axis` fail on the measured X centre by 1 mm. The
  mutation was removed and the faceted contract returned green.
- Moving the front disc product 1 mm radially makes the bounded ring-gap
  contract fail (0.285 mm measured against the 0.8 mm lower bound). Moving
  the output stack 1 mm makes `test_output_plate_is_on_reduction_axis` fail.
  Both mutations were removed.
- Changing only the output relation from -1/20 to -1/19 makes the one-input-
  revolution contract report -18.947 degrees instead of -18 degrees, and the
  five-second scenario cadence reports the same ratio error in motion. The
  mutation was removed.

The 41-second demonstration samples driven ratio, opposed eccentric centres,
and the 0.8--1.0 mm faceted disc/ring gap every five seconds. This is one
quarter of each 20-second long instruction and produces eight sampled checks;
the exact all-pairs source inventory remains a home-pose certification because
the source disc tessellation is non-manifold.

## Source-authored overlap finding

The exact home-pose inventory contains 20 positive-volume clashes, all between
the cycloidal disc bodies and the nominal output pins or bearings. Volumes
range from 99.367716 to 1255.240118 mm³ and are recorded pair-by-pair in
`simulation/seats.py`. The simulation preserves and checks that inventory; it
does not call the source geometry interference-free. The disc STL emitted by
the source is also non-manifold, so broad all-pairs interference is certified
on exact STEP solids while the faceted loop checks the measured ring gap and
output-site alignment without a volume epsilon.

## Visual inspection

Web-renderer snapshots were inspected at home, at 1890 degrees of input, and
straight down +Y. The isometric pair shows the output plate/pins and eccentric
disc set rotating while the housing remains fixed. The axial view confirms
the input bore and output plate are concentric in the authored frame, and the
opposed orange disc profiles remain visible on opposite sides of the ring.
The actuated proof pose is a separate non-manifest node only because snapshot
parameter overrides do not bind a `Driver`; the interactive model still has
exactly one driver and defaults to home.
