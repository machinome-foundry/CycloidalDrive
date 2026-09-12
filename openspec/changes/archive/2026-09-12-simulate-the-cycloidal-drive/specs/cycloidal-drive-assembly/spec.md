## ADDED Requirements

### Requirement: V4 product geometry remains upstream-owned
The simulation SHALL import each uniquely selectable product used by the cycloidal mechanism from `V4/Cycloidal_V4_02.stp` without copying or redrawing its geometry, and SHALL explicitly report any source product that cannot be selected unambiguously.

#### Scenario: Upstream STEP remains untouched
- **WHEN** the simulation is built
- **THEN** its rigid geometry originates from the existing V4 STEP document and the document has no project changes

#### Scenario: Ambiguous products are visible
- **WHEN** two source products have the same selector name
- **THEN** the simulation records both as an import limitation instead of choosing either silently

### Requirement: Authored V4 placements are preserved
The simulation SHALL place the input stack, paired cycloidal discs, output assembly, bearings, and pulley from the V4 occurrence transforms, with the reduction axis on +Y and the two disc centres at equal-and-opposite 5 mm eccentric offsets.

#### Scenario: Opposed disc centres
- **WHEN** the machine is at its authored home pose
- **THEN** the midpoint of the two disc centres lies on the input axis and both radial distances are 5 mm within 0.01 mm

#### Scenario: Source placement drift
- **WHEN** the recorded occurrence inventory is checked against the V4 document
- **THEN** every simulated occurrence name and placement agrees with the source-derived probe record

### Requirement: Mechanical interfaces are contract-tested
The simulation SHALL prove the shaft/cam/bearing stack, cycloidal ring engagement, and disc/output engagement from rendered geometry, and SHALL keep every rigid imported product connected.

#### Scenario: Input stack is coaxial
- **WHEN** the drive is at home
- **THEN** the shaft, cam, and their bearing axes coincide with the +Y input axis within 0.01 mm

#### Scenario: Source home-pose overlap inventory is stable
- **WHEN** exact interference checks are run at the authored home pose
- **THEN** the positive-volume overlap pairs and volumes equal the documented source-authored inventory

#### Scenario: Imported products remain solid
- **WHEN** each simulated rigid product is built
- **THEN** it contains no disconnected solid fragments
