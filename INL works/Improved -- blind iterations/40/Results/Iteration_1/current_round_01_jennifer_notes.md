# Round 1 Jennifer Connectivity Notes - Doc 40 / Iteration_1

## Scope

Precision review of Diego Round 1 using only input resources, prepared input-only artifacts, and Diego's Round 1 proposal files. I did not use ground truth, validation metrics, evaluation files, GT-derived feedback, or prior validation/evaluation directories. The raw schematic was treated as primary evidence; overlays, inventories, wire-node files, and crops were used only as aids.

## Node Inventory Decisions

- Final matrix nodes: 57.
- Excluded label-only banners/notes: `TRAIN-A-480V-SAFETY-CHANNEL`, `TRAIN-B-480V-SAFETY-CHANNEL`, `SOURCE-NORMAL`, `SOURCE-ALTERNATE`, `RPS-CH-A-CONTROL-LANE`, and `RPS-CH-B-CONTROL-LANE`. In the raw schematic these are area, source, or lane labels and have no electrical/logical terminal.
- Excluded MCC enclosure labels: `MCC-21A` and `MCC-21B`. The raw crops show these as enclosure/equipment titles around the actual 480 V 3PH bus rails. Connectivity is placed on `MCC-21A-480V-3PH` and `MCC-21B-480V-3PH` instead.
- Kept actual connected buses/logical signal nodes: `SWGR-21A`, `SWGR-21B`, `MCC-21A-480V-3PH`, `MCC-21B-480V-3PH`, `DC-BUS-21A`, `DC-BUS-21B`, `VOLTAGE-SIG-A`, and `VOLTAGE-SIG-B`.
- No `WIRE-NODE-*` points were promoted into the matrix.
- No visible ground nodes were identified in the allowed raw/focus evidence.

## Answers To Specific Review Questions

1. The two train-channel labels, `SOURCE-NORMAL`, `SOURCE-ALTERNATE`, and the two RPS control-lane labels are not actual connected nodes. They are excluded.
2. Diego's `VOLTAGE-SIG-A/B -- MOV-RWST21A/B` edges are not supported. The raw crops show no terminal/dot into the MOV symbols; the apparent intersections are no-dot/crossing cases.
3. `MCC-21A` and `MCC-21B` should not remain as connected matrix nodes. Final connectivity lands on the named 480 V 3PH bus nodes, with `TR-21A -- MCC-21A-480V-3PH` and `TR-21B -- MCC-21B-480V-3PH` used as the practical feeder connections.
4. Dashed, dash-dot, and short-dash lines were checked for shortcut crossings. I did not add edges at crossings without dots or terminal landings.

## Edges Removed Or Reworked From Diego

- Removed `VOLTAGE-SIG-A -- MOV-RWST21A` and `VOLTAGE-SIG-B -- MOV-RWST21B`: unsupported no-dot crossings near the RWST MOVs.
- Removed `TR-21A -- MCC-21A`, `MCC-21A -- MCC-21A-480V-3PH`, `TR-21B -- MCC-21B`, and `MCC-21B -- MCC-21B-480V-3PH`: MCC enclosure labels are not final connectivity nodes.
- Added direct feeder assignments `TR-21A -- MCC-21A-480V-3PH` and `TR-21B -- MCC-21B-480V-3PH` to preserve the visible transformer-to-MCC bus feed without retaining enclosure-title nodes.
- Kept Diego's remaining supported power, DC, trip-control, control-logic, LOCA/JB/RPS, CT/RPS, and VT/voltage-signal/RPS edges.

## Uncertain Or Lower-Confidence Cases

- `TR-21A -- MCC-21A-480V-3PH` and `TR-21B -- MCC-21B-480V-3PH` are kept at 0.90 because the raw feeder visibly lands at the MCC enclosure above the named bus rail; the bus is the correct final node after removing the enclosure title.
- `VT-21A -- VOLTAGE-SIG-A` and `VT-21B -- VOLTAGE-SIG-B` are kept at 0.85 because the short-dash VT leads continue into the labeled voltage-signal trunks across the top/MCC crops, but the connection spans crop boundaries.
- `JB-21A -- RPS-PNL-A` and `JB-21B -- RPS-PNL-B` are kept at 0.92 because the dashed JB paths terminate on RPS top terminals, while nearby crossings without terminal dots are ignored.

## Validation Summary

- Edge rows written: 58.
- Matrix nodes written: 57.
- Matrix is symmetric with a zero diagonal.
- Node names are unique.
- Every edge CSV endpoint appears in the matrix.
- Every nonzero off-diagonal matrix entry has exactly one corresponding undirected edge CSV row, and every edge CSV row has symmetric matrix entries.
