# Round 02 Jennifer Final Saturation Notes

## Scope
Final precision/saturation check used only doc 11 input resources, generated crops/artifacts, inspection crops, and Round 1/Round 2 files in `Results\Iteration_1`. No ground truth, evaluator output, scores, validation metrics, or answer keys were used.

## Final Saturation Decision
Final saturation reached. I found no additional clean direct named endpoint edges beyond Diego Round 2's four promoted panel-to-DC-bus edges, and I found no node changes beyond the existing 120-node Jennifer policy.

## Final Counts
- Nodes: 120.
- Accepted edges: 132.
- Uncertain/removed/relabel/verified decisions: 52.

## Node Set
- Kept 120 nodes: physical components, named buses, and named grounds/reference symbols.
- No reference-area nodes are present: `SAFETY-TRAIN-*`, `125-VDC-DIVISION-*`, and `CTRL-RPS-INTERLOCKS` remain excluded as printed area labels.
- Diesel generator component tags remain `DG-1A/B/C/D`; `DG-2A/B/C/D` are feeder/conductor labels, not component nodes.
- `CB-MCC-A1` remains accepted as a raw-visible recovered breaker on the Train A MCC-A1 branch.
- Buses and grounds remain valid, including `BUS-DC-125A/B`, all 13.8 kV/4160/480 buses, and `GND-A/B/C/D`.

## Panel-To-DC-Bus Promotions
Accepted the four Diego Round 2 panel-to-bus edges:
- `PANEL-IC-A -- BUS-DC-125A`: crops 21, 25, and 31 show DC-A125 landing on `BUS-DC-125A` at a visible bus dot.
- `PANEL-IC-B -- BUS-DC-125B`: crops 22, 26, 29, and 32 show DC-B125 into the `BUS-DC-125B` lower bus area.
- `PANEL-IC-C -- BUS-DC-125B`: crops 23, 29, and 30 show DC-C125 routed to the Division B / `BUS-DC-125B` bus area; this is visual, not symmetry-based.
- `PANEL-IC-D -- BUS-DC-125B`: crops 24, 28, 30, and 32 show DC-D125 to the `BUS-DC-125B` bus area.

## Ground Edges
Kept `PANEL-IC-X -- GND-X` in addition to the panel-to-DC-bus edges. The ground symbols are visible named ground endpoints with local dots on their own ground/reference branches; the lower DC-bus landings are separate visible bus junctions. I did not add `GND-X -- BUS-DC-125*` because no clean direct ground-to-bus endpoint path is shown.

## Still Excluded
No MCC-to-ATS input edge was promoted; the `ATS-A1/B1/C1/D1` routes remain long and crossing-heavy. No relay-to-SSPS, SSPS-to-RPS, SSPS-to-ATS, DC-bus-to-SSPS, rectifier-to-bus skip, or ground-to-bus edge was promoted. Crossings without dots were not treated as taps.

## 480 Bus Ties
The four 480 V split-bus tie edges remain accepted: `BUS-480-A1--BUS-480-A2`, `BUS-480-B1--BUS-480-B2`, `BUS-480-C1--BUS-480-C2`, and `BUS-480-D1--BUS-480-D2`; the focused 480 crops show `TIE-*12` segments with visible dots.
