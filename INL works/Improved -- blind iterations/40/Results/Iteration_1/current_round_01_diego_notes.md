# Round 1 Diego Connectivity Notes - Doc 40 / Iteration_1

## Scope and Sources

Blind input-only pass. I used the raw schematic in `Input resources`, the prepared component inventory and wire-node summary in `Codes and artifacts`, the overview/contact/3x3 crops, and the added focus crops under `inspection_crops_doc40_current/focus`. I did not use ground truth, validation metrics, evaluation files, or previous Results as evidence.

## Node Inventory Decisions

- Retained the 65 nodes from `component_inventory_doc40_current.csv` in inventory order for the matrix.
- Added no nodes and renamed no nodes.
- Removed no nodes from the matrix. Contextual labels with no visible electrical/logical conductor attachment were retained as isolated rows/columns: `TRAIN-A-480V-SAFETY-CHANNEL`, `TRAIN-B-480V-SAFETY-CHANNEL`, `SOURCE-NORMAL`, `SOURCE-ALTERNATE`, `RPS-CH-A-CONTROL-LANE`, `RPS-CH-B-CONTROL-LANE`.
- Promoted no `WIRE-NODE-*` points into the matrix. The wire-node overlay was used only as contact/junction aid; buses and named logical nodes represent the meaningful rails/trunks.
- No ground symbols were visually identified in the allowed raw/focus crops.

## Evidence Summary

- Solid top feeders connect the A source path `UAT-2A -> DS-21A -> ATS-21A` and `DG-21A -> ATS-21A`, with `ATS-21A` landing on `SWGR-21A` by a filled dot.
- Solid top feeders connect the B source path `SAT-2B -> DS-21B -> ATS-21B` and `DG-21B -> ATS-21B`, with `ATS-21B` landing on `SWGR-21B` by a filled dot.
- `TIE-BKR-21AB` is visibly in series between the `SWGR-21A` and `SWGR-21B` buses.
- `SWGR-21A` drops through `CB-21A1` and `TR-21A` into `MCC-21A`; `SWGR-21B` mirrors through `CB-21B1` and `TR-21B` into `MCC-21B`.
- The MCC focus crops show named 480 V 3PH bus rails and solid taps to pumps, fans, MOVs, CPT transformers, and breaker-fed SI pumps.
- CPT branches feed AC panels, AC panels feed rectifier/chargers, and rectifier/charger outputs land on the 125 VDC buses.
- DC buses have filled-dot solid taps to batteries, rectifier/chargers, and inverters.
- Dashed and dash-dot wiring is separated by line style: trip-control lines from MCC breakers to 86 relays; dashed control/logic relay/RPS/inverter and LOCA/JB paths; short-dash instrumentation from CT/VT/voltage-signal trunks into RPS/MOV-related signal points.

## Uncertain or Lower-Confidence Edges

- `VT-21A` -- `VOLTAGE-SIG-A` confidence 0.75: Raw overview/top Train A shows VT-21A short-dash instrument lead descending into the VOLTAGE-SIG-A trunk; contact is partly off focus crop.
- `VOLTAGE-SIG-A` -- `RPS-PNL-A` confidence 0.82: Raw DC/RPS Train A focus shows VOLTAGE SIG A short-dash trunk dropping to a top terminal of RPS-PNL-A.
- `VOLTAGE-SIG-A` -- `MOV-RWST21A` confidence 0.70: Raw MCC Train A focus shows VOLTAGE SIG A trunk meeting the dashed vertical signal line associated with MOV-RWST21A; no-dot callout separates it from the solid feeder.
- `VT-21B` -- `VOLTAGE-SIG-B` confidence 0.75: Raw overview/top Train B shows VT-21B short-dash instrument lead descending into the VOLTAGE-SIG-B trunk; contact is partly off focus crop.
- `VOLTAGE-SIG-B` -- `RPS-PNL-B` confidence 0.82: Raw DC/RPS Train B focus shows VOLTAGE SIG B short-dash trunk dropping to a top terminal of RPS-PNL-B.
- `VOLTAGE-SIG-B` -- `MOV-RWST21B` confidence 0.70: Raw MCC Train B focus shows VOLTAGE SIG B trunk meeting the dashed vertical signal line associated with MOV-RWST21B; solid feeder remains separate.

## Output Consistency

- Edge rows written: 62.
- Matrix nodes: 65.
- Matrix is symmetric with zero diagonal by construction and was validated after writing.
- Every nonzero off-diagonal matrix pair has exactly one corresponding edge CSV row, and every edge CSV row has symmetric matrix entries.
