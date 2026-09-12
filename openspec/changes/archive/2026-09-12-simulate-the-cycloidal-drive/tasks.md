## 1. Project Record and Source Evidence

- [x] 1.1 Add the solid-node manifest, builder profile, ignore rules, and a minimal `simulation:CycloidalDrive` root that renders the imported input shaft.
- [x] 1.2 Add `simulation/tools/probe.py` and `docs/measurements.md` recording the V4 product inventory, occurrence transforms, ambiguous `COMPOUND` products, disc eccentricity, counted pins/lobes, and derived ratio.
- [x] 1.3 Write and run a red source-drift/placement contract, then add the source-derived `simulation/layout.py` values and make it green.

## 2. Input and Fixed Stack

- [x] 2.1 Write and run red contracts for imported-product connectivity and +Y coaxiality of the shaft, cam, and bearings.
- [x] 2.2 Add the thin V4 `StepNode` parts and input/fixed-stack assembly needed to make those contracts green.
- [x] 2.3 Mutate the input-axis or bearing placement in node code, confirm the intended contract fails, restore it, and record the result.

## 3. Cycloidal and Output Assemblies

- [x] 3.1 Write and run red contracts for opposed disc centres, cycloidal-ring engagement, and disc/output engagement.
- [x] 3.2 Add the paired discs, ring, and output assembly from authored occurrence placements and make the interface contracts green.
- [x] 3.3 Measure all source-authored positive-volume overlaps into `simulation/seats.py`, enforce the exact inventory, and record any unselectable source geometry as a finding.
- [x] 3.4 Mutate one disc phase/offset and one output placement, confirm the corresponding contracts fail, restore them, and record the results.

## 4. Motion and Demonstration

- [x] 4.1 Write and run red contracts for input-member rotation, balanced disc orbit, counter-rotation/output ratio, exact instruction endpoints, and the complete scenario.
- [x] 4.2 Declare the input, disc, and output freedoms; relate them to the sole `input_angle` driver; and add `Home`, `One Input Revolution`, and `One Output Revolution` instructions.
- [x] 4.3 Make the motion and scenario contracts green on the faceted kernel, sampling the integrity inventory at a cadence justified by the demo durations.
- [x] 4.4 Mutate the reduction sign or ratio in node code, confirm the ratio/scenario contract fails, restore it, and record the result.

## 5. Delivery and Certification

- [x] 5.1 Run faceted regression for every simulation node file and `solid build`; inspect `viewer.json` for the complete tree, the sole driver, instruction targets, symbolic motion, and existing rigid artifacts.
- [x] 5.2 Render and inspect an isometric home snapshot, an actuated snapshot, and a +Y-axis alignment snapshot.
- [x] 5.3 Update the README with exact build/test/run commands, controls, instructions, viewing sequence, limitations, and findings.
- [x] 5.4 Run the full exact regression once, validate the OpenSpec change, sync the accepted specifications, archive the change, and commit the completed implementation record.
