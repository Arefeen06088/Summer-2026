# Jennifer Round 02 Precision Review - Document 18

## Scope

Worked only inside `Raw + wires + junctions + OCR` for document 18. I used the raw schematic and local aid/review crops; no Ground Truth, evaluator feedback, outside files, or off-the-shelf OCR were used.

## Counts

- Diego candidate edges reviewed: 204
- Final kept edges: 193
- Diego edges removed/dropped: 13
- Replacement edges added by rewiring around unsupported `CB-SWYD-230`: 2
- Endpoint/node label renames: 2
- RPS dashed relay memberships dropped: 8
- Kind corrections: 2 (`RPS-PNL-A -- PLC-RPS-A` and `RPS-PNL-B -- PLC-RPS-B` changed to `rps_dashed_control`)

## Major Decisions

- Renamed Diego's `BUS-SWYD-230` to `BB-SWYD-230`. The raw top-left source bus label reads `BB-SWYD-230`.
- Rejected `CB-SWYD-230` as an unsupported intermediate node. I replaced the two source-breaker paths with direct final edges `CB-GRID-A -- BB-SWYD-230` and `CB-GRID-B -- BB-SWYD-230`.
- Renamed `BUS-GEN-TERMINAL` to `GEN-MAIN-1-TERMINAL` so the edge and node decision labels consistently describe the common conductor after `CB-GEN-ISO` that ties `GEN-MAIN-1` to the UAT primary taps.
- Removed `CB-UAT-A -- BUS-4160B` and `CB-UAT-B -- BUS-4160B`. The UAT breaker symbols are present, but I do not see a visible lower conductor or filled landing from either breaker to `BUS-4160B`.
- Kept `BUS-480B -- CHG-125A` and `BUS-480C -- CHG-125B`; both long solid drops visibly land on the charger row.
- Kept `RPS-A-DASHED-NET` and `RPS-B-DASHED-NET` only as limited logical nodes for the visually landed dashed PLC/JB/annunciator bundle endpoints. Dropped relay memberships where the relay box is merely inside or adjacent to the dashed routing without a clear landed terminal.
- Corrected `RPS-PNL-A -- PLC-RPS-A` and `RPS-PNL-B -- PLC-RPS-B` from `ac_control_power` to `rps_dashed_control` because the raw links are dashed control/signal lines.

## Final Edge Counts By Kind

- ac_control_power: 6
- bus_tie: 2
- dc_control_power: 12
- grounding: 4
- instrumentation_control: 10
- power_480_feeder: 120
- power_primary_230_4160: 19
- power_transformer_infeed: 12
- rps_dashed_control: 8

## Residual Uncertainty

The retained RPS dashed-net edges remain medium confidence because the drawing shows a shared dashed bundle more clearly than exact point-to-point wiring order. I intentionally dropped the relay memberships instead of guessing at terminal connections. I also did not add recall-only edges outside Diego's candidate set except for the two direct source-bus replacements required after removing the unsupported `CB-SWYD-230` intermediate.
