# Round 02 Diego Saturation Review Notes

## Scope

Reviewed only doc33 local resources and permitted round files:

- Raw schematic: `Input resources/raw -- synthetic_aux_ccw_pid_v14_highres_clean.png`
- Component inventory and resource summaries in `Codes and artifacts`
- Inspection crops and derived overlays in `Codes and artifacts`
- Jennifer Round 01 matrix/notes in `Results/Iteration_1`

No ground truth, evaluator output, score feedback, or outside resources were used.

## Decision

I agree with Jennifer Round 01 and copied `round_01_jennifer_matrix.csv` exactly to `round_02_diego_matrix.csv`.

No node changes and no edge changes were made relative to Jennifer Round 01.

## Node List Rationale

Jennifer retained the full 193-node set from Diego Round 01, consisting of inventory components plus visible named non-inventory endpoints such as headers, manifolds, off-page connectors, control/data buses, and named logical boxes. This remains appropriate for the final saturated pass.

I did not add anonymous wire nodes, WN ids, junction ids, elbows, bend points, line-number-only labels, or unlabeled crossing points. No additional visible named endpoint was found that required a new node.

## Edge Evidence By Region

### Left surge / makeup area

The disputed TK-101/TK-102/SV-101/HV-104 area supports Jennifer's stricter local adjacency. `SV-101` is visually local to the TK-101 makeup/control branch and does not clearly land directly on `TK-102`. The visible local route supports retaining `HV-104 -- SV-101` and not restoring the shortcut `SV-101 -- TK-102`.

### Filter / bypass / relief area

The filter DP instrumentation supports Jennifer's correction. `DPI-21A` and `DPI-21B` have local visual association/taps to the corresponding filter trains, while `DPT-21A` and `DPT-21B` appear on separate dashed signal runs toward the PDI/PDT/JB marshalling path. I therefore accept `DPI-21A -- FLT-201A` and `DPI-21B -- FLT-201B`, and do not restore `DPI-21A -- DPT-21A`, `DPI-21B -- DPT-21B`, `DPT-21A -- FLT-201A`, or `DPT-21B -- FLT-201B`.

Jennifer's added `4" FILTER INLET MANIFOLD -- PT-202` is also visually supported by the local pressure tap on the inlet manifold.

### Service-water / heat-exchanger controls

The HX temperature and vent/valve area supports Jennifer's removals. The `TT-31A/B` to `TY-31A/B` signal lines pass near the `VV-31A/B` vertical valve symbols without a clear endpoint dot or termination at the vent valves. I do not restore `TY-31A -- VV-31A` or `TY-31B -- VV-31B`.

The instrument-air removals remain appropriate where lines are only plausible by proximity. `AFR-301 -- PCV-302`, `AFR-301 -- TCV-301`, `AFR-401 -- AV-501`, and `AFR-401 -- FCV-401` are not clearly supported as direct named endpoint connections in the raw schematic.

### Chemical dosing skid

The chemical skid supports Jennifer's changes. `CAL-301` is drawn with a solid connection toward the upper metering/suction side near `P-301A`, not as a direct connection to `TK-301` or `JB-302`. I accept `CAL-301 -- P-301A` and do not restore `CAL-301 -- TK-301` or `CAL-301 -- JB-302`.

The analyzer/controller/final-control path supports `AIC-301 -- FV-301`. A direct process-header edge `1/2" CHEMICAL DOSING HEADER -- AIC-301` would skip the visible final-control endpoint, so I do not restore it.

### Bottom control / instrument-air bay

The data bus and junction-box removals remain consistent with the node policy. The visible `DCS / PLC DATA BUS` is a named logical bus, but the removed shortcuts to `DCS-001`, `JB-101`, `JB-301`, `JB-302`, and `JB-501` are not clear direct endpoint connections. Where a control-room link or local marshalling path is visible, the graph should use those local named adjacencies rather than clique-expanding the bus.

For instrument air, I retained Jennifer's supported local AFR-to-valve links and did not re-add speculative long or crossing-based connections such as `AFR-201 -- FCV-230`, `AFR-301 -- PCV-302`, `AFR-301 -- TCV-301`, `AFR-401 -- AV-501`, or `AFR-401 -- FCV-401`.

## Ambiguous / Plausible But Not Included

The following remain plausible by nearby geometry but not sufficiently supported as direct edges:

- `SV-101 -- TK-102`
- `CAL-301 -- TK-301`
- `CAL-301 -- JB-302`
- `1/2" CHEMICAL DOSING HEADER -- AIC-301`
- `AFR-201 -- FCV-230`
- `AFR-301 -- PCV-302`
- `AFR-301 -- TCV-301`
- `AFR-401 -- AV-501`
- `AFR-401 -- FCV-401`
- `DCS / PLC DATA BUS -- DCS-001`
- `DCS / PLC DATA BUS -- JB-101`
- `DCS / PLC DATA BUS -- JB-301`
- `DCS / PLC DATA BUS -- JB-302`
- `DCS / PLC DATA BUS -- JB-501`
- `DPI-21A -- DPT-21A`
- `DPI-21B -- DPT-21B`
- `DPT-21A -- FLT-201A`
- `DPT-21B -- FLT-201B`
- `TY-31A -- VV-31A`
- `TY-31B -- VV-31B`

## Round 02 Changes Relative To Jennifer Round 01

None.

- Nodes added: 0
- Nodes removed: 0
- Edges added: 0
- Edges removed: 0

## Basic Validation

- Node count: 193
- Edge count: 222
- Matrix values: 0/1 only
- Row/column order: same order and same 193 node names
- Symmetry check: pass
- Diagonal check: all zero
- Isolated accepted nodes: 0
- Round 02 matrix content: exact copy of Jennifer Round 01 matrix
