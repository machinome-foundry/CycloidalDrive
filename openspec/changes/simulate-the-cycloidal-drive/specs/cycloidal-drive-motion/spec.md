## ADDED Requirements

### Requirement: Input angle is the sole machine driver
The complete drive SHALL expose one `input_angle` control in degrees and SHALL derive shaft, cam, pulley, disc-orbit, disc-spin, and output motion from that value.

#### Scenario: Input members turn together
- **WHEN** `input_angle` advances by 360 degrees
- **THEN** the shaft, cam, and input pulley each advance by 360 degrees about +Y

#### Scenario: Disc eccentric balance is maintained
- **WHEN** `input_angle` changes anywhere in its declared range
- **THEN** both disc centres orbit the input axis at the measured eccentric radius while remaining 180 degrees apart

### Requirement: Cycloidal reduction follows the source geometry
The discs and output SHALL rotate opposite the input at the 20:1 reduction independently derived from the source's 20-lobe disc and one-pin-difference ring.

#### Scenario: One input revolution
- **WHEN** `input_angle` advances by 360 degrees
- **THEN** the output and each disc advance by exactly -18 degrees relative to their authored phases

#### Scenario: One output revolution
- **WHEN** `input_angle` advances by 7200 degrees
- **THEN** the output lands exactly one revolution opposite the input direction

### Requirement: Demonstration instructions land on exact states
The machine SHALL provide `Home`, `One Input Revolution`, and `One Output Revolution` instructions with finite demonstration durations.

#### Scenario: Home instruction
- **WHEN** `Home` completes
- **THEN** `input_angle` is exactly 0 degrees and the source-authored pose is restored

#### Scenario: Input-revolution instruction
- **WHEN** `One Input Revolution` completes
- **THEN** `input_angle` is exactly 360 degrees

#### Scenario: Output-revolution instruction
- **WHEN** `One Output Revolution` completes
- **THEN** `input_angle` is exactly 7200 degrees

### Requirement: Demonstrated motion preserves the assembly contract
The simulation SHALL check rigid-body integrity and the documented overlap inventory throughout every instruction path at a cadence commensurate with the demonstration durations.

#### Scenario: Complete demonstration
- **WHEN** the three instructions run in sequence
- **THEN** each instruction lands on its target and no rigid-body overlap outside the documented source inventory appears at any sampled state
