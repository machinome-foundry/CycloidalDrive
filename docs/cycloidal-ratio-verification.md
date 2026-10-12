# Cycloidal ratio migration verification

This narrow refactor names the measured 20-lobe/21-pin signed output/input
ratio with `machinome_mechanics.cycloidal_ratio`. It preserves the separate,
positive `REDUCTION_RATIO`, the 7,200-degree output-cycle target, the two disc
orbit relations, instructions, phases, and the independent scenario-test
oracle `-input / REDUCTION_RATIO`.

## Tested source identity

- Project base: `28b5963e0f78a92566542a4684bab83aa593a92b`
- Project branch: `mechanics-cycloidal-ratio`
- Mechanics planning commit: `07dd6b4d37fa2b4e161f295ae0828381bcaff5bd`
- Tested uncommitted mechanics `machinome_mechanics/gears.py` SHA-256:
  `808d1a07a1980d35591bd5f4b837d902caa1ac62ddddbcac6c434b06a8efb73b`
- Framework before and after validation:
  `8d2bd71171be81f13ba5dd492851ed8b3a9ababb` (clean, locally ahead of its
  remote)
- Viewer before and after validation:
  `4355da1a7f64dacd7d86eb27dbdfdf7ced94598f` (clean)

The mechanics implementation is source-worktree content beyond its planning
commit, so the file digest—not the planning commit alone—identifies the helper
that was tested. This tool-only project has no package dependency table; the
README records the required source checkout or installation instead of
inventing project packaging.

## Lightweight parity probe

Run:

```sh
PYTHONPATH="$PWD:/home/asa/devel/machinome-studio/WTs/mechanics-cycloidal-ratio" \
  /home/asa/devel/machinome-studio/.venv/bin/python \
  docs/probes/cycloidal_ratio.py
```

The probe instantiates both production assembly classes and checks six valid
guarded states, including multi-turn values, against the independent legacy
law. It also sends the real animation-time expression through each production
output relation and evaluates six signed, unwrapped values, while guarding the
unchanged positive reduction and cycle target. A negative actual machine state
is deliberately not attempted because the preserved 0..7,200-degree joint
range correctly refuses it.

The first run passed with `PASS: 12 actual production states and 36 deferred
relation evaluations` in 3.76 seconds (maximum RSS 524,772 KiB, no swaps).
Although initially classified as lightweight, importing and posing the actual
model loaded substantial geometry. It was below the campaign's 768 MiB ceiling
but did not run in a cgroup; the final evidence run will therefore repeat it
under the same process-tree cgroup used for CAD validation. This initial result
is retained rather than silently relabelled as capped evidence.

## Bounded validation

Each command ran alone in a unique `systemd-run --user --wait --pipe --collect`
unit with `MemoryMax=768M`, `MemorySwapMax=0`, `RuntimeMaxSec=300`, and both
`OPENBLAS_NUM_THREADS` and `OMP_NUM_THREADS` set to `1`. The project and
mechanics source roots were explicit on `PYTHONPATH`; `/usr/bin/time -v`
wrapped each inner command. Logs are retained under `.cache/` and excluded by
the narrow `.gitignore` pattern `.cache/cycloidal-ratio*`.

The first capped probe attempt used the systemd manager's different resolved
source root and failed before checking behavior with a permission error while
creating `/mnt/home/...`; `.cache/cycloidal-ratio-probe.log` records it. The
successful retry explicitly selected a project-owned `SOLID_BUILD_DIR`:

```sh
/usr/bin/time -v /home/asa/devel/machinome-studio/.venv/bin/python \
  docs/probes/cycloidal_ratio.py
```

Result: PASS, 12 actual production states and 36 deferred evaluations in 3.38
seconds, maximum process RSS 524,932 KiB, no swap. Log:
`.cache/cycloidal-ratio-probe2.log`.

The established full-machine commands were then attempted without weakening
assertions or changing tolerances:

```sh
SOLID_TEST_ENGINE=mesh machinome test --mesh simulation/machine.py
SOLID_TEST_ENGINE=brep machinome test --brep simulation/machine.py
```

Both runs passed `test_assembly_integrity`, then the cgroup killed the process
at the pre-existing mesh-heavy `test_cycloidal_ring_engagement` when charged
memory reached exactly 768 MiB (faceted 10.85 seconds; exact 37.27 seconds;
swap 0). They are incomplete runs, not suite passes. Logs:
`.cache/cycloidal-ratio-faceted.log` and
`.cache/cycloidal-ratio-exact.log`.

An untouched detached worktree at the recorded base ran the identical faceted
command under identical limits. It too passed assembly integrity and was
killed at ring engagement at exactly 768 MiB after 10.34 seconds. This supports
classifying the cap failure as unchanged rather than helper-induced. Log:
`.cache/cycloidal-ratio-base-faceted.log`; the temporary worktree was removed
afterward.

A direct `unittest` method invocation did not supply Machinome's node fixture
and failed with an unbound `AssemblyNode.set_state`; its log is retained as
`.cache/cycloidal-ratio-relation-faceted.log` but it is not regression
evidence. The supported `machinome test` interface selects a model, not an
individual method. The production-state probe above is therefore the focused
motion gate.

The project build completed successfully:

```sh
/usr/bin/time -v machinome build
```

Result: exit 0 in 14.24 seconds, maximum process RSS 515,708 KiB, no swap.
Log: `.cache/cycloidal-ratio-build.log`.

The fresh established nonzero pose used the visual-evidence-only assembly,
whose default driver is 1,890 degrees:

```sh
/usr/bin/time -v machinome snapshot \
  simulation.machine:ActuatedCycloidalDrive --viewer web \
  --autocenter --viewall --imgsize 1280x720 \
  -o .cache/cycloidal-ratio-driven-web.png
```

Result: exit 0 in 14.04 seconds, maximum process RSS 647,248 KiB, no swap.
Log: `.cache/cycloidal-ratio-snapshot.log`. The image shows the complete
housing, ring, opposed lobed discs, shaft and output hardware assembled with
no gross detached closure. Fine hidden contacts are not proven by these
pixels. The clean viewer commit above rendered the image, so no dirty-renderer
qualification is required.
