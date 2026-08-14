# Document 26 Round 03 Diego Notes

## Scope And Method

- Reviewed Jennifer's round-02 graph against the raw schematic and allowed aids only: component/label overlays, wire masks, wire-node overlays, component index, and precision crops.
- Did not use Ground Truth, evaluator outputs, previous-document connectivity, or off-the-shelf OCR.
- Applied the round-03 high-recall rule: keep an edge only where the raw/aids show a visually plausible direct termination or named routed control abstraction; reject proximity-only alignments and crossings without connection support.

## Agreement With Jennifer

- I agree with Jennifer's round-02 matrix.
- No nodes were added, removed, or relabeled.
- No edges were added or removed.
- The round-03 edge set remains the same 209 undirected edges and the same 200-node order as round 02.

## Six Ambiguous Edge Recheck

- `CB-4A03 -- MTR-RCP-A`: retained at low confidence. The dashed control/protection line exits CB-4A03 and drops along the RCP-A motor-side branch; it is a plausible named route to the RCP branch rather than a random crossing.
- `CB-4B03 -- MTR-RCP-B`: retained at low confidence. The B-side crop mirrors A: the dashed lead leaves CB-4B03 and runs along the RCP-B motor-side branch with visible route continuity.
- `STR-A1-1 -- BAT-31A`: retained at medium confidence. The dashed control route leaves the STR-A1-1 area and lands on the lower Train A dashed DC control run with explicit BAT-31A endpoints in the node overlay.
- `STR-B1-1 -- BAT-31B`: retained at medium confidence. The B-side route is visible through the corresponding lower Train B dashed control run and terminates in the BAT-31B/CHG-31B area.
- `CB-480A13 -- STR-A3-3`: retained at low confidence. The dashed route exits CB-480A13, descends along LC-31A3, and has a short dashed spur into the STR-A3-3 branch area; it is weak but visually plausible as a routed interlock.
- `CB-480B13 -- STR-B3-3`: retained at low confidence. The B-side crop shows the same structure, including the short dashed spur from STR-B3-3 into the dashed vertical route.

## Upgraded Lower Feeder Confirmation

- `CB-INV-A -- INV-31A` and `CB-INV-B -- INV-31B` remain supported by solid vertical inverter feeders.
- `BUS-INV-A -- PNL-AC-A` and `BUS-INV-B -- PNL-AC-B` remain supported by solid bus taps.
- `PNL-AC-A -- BUS-120N-A` and `PNL-AC-B -- BUS-120N-B` remain supported by solid lower AC bus terminations.
- `BAT-31A -- CHG-31A` and `BAT-31B -- CHG-31B` remain supported by local dashed control links with visible endpoints at both devices.

## Counts

- Node count: 200
- Edge count: 209
- Edge kind counts: `bus_tie`: 6, `control_interlock`: 10, `ground`: 8, `instrument_signal`: 16, `power_feeder`: 169
- Confidence counts: `high`: 203, `low`: 4, `medium`: 2

## Validation

- No unknown nodes in edges: True
- No duplicate undirected pairs: True
- Symmetric adjacency matrix: True
- Diagonal zero: True
