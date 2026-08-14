# Document 40 Round 02 Jennifer Notes

Scope followed: only resources inside the document-40 folder were used. I did not use GT, evaluator feedback, outside folders, previous-document answers, or off-the-shelf OCR. The raw schematic was treated as authoritative; the in-folder visual-label CSV, wire-node overlays, and precision crops were used only as review aids.

## Round Decision

No graph changes were made from Diego round01. I copied the round01 node and edge CSVs forward to `document40_round02_jennifer_nodes.csv` and `document40_round02_jennifer_edges.csv`.

The reviewed graph remains at 57 included nodes and 58 unique undirected included edges.

## Node Review

- Kept `SWGR-21A` and `SWGR-21B`: each is a thick switchgear bus with explicit junction dots to ATS, feeder breaker, and tie-breaker paths.
- Kept `MCC-21A-480V-3PH` and `MCC-21B-480V-3PH`: each is the actual heavy 480 V 3PH rail with multiple tapped loads.
- Kept physical `MCC-21A` and `MCC-21B` as enclosure/component nodes linked to their internal bus nodes by `internal_bus`: the TR feeder lands on the MCC enclosure/top termination while the internal rail is the separate multi-tap busbar shown inside the enclosure.
- Kept `DC-BUS-21A` and `DC-BUS-21B`: each is a thick 125 VDC rail with drawn junction dots for rectifier, battery, and inverter branches.
- Kept Diego's exclusions for train title boundaries, RPS control-lane captions, `VOLTAGE-SIG-A/B` route labels, and `SOURCE-NORMAL/ALTERNATE` feed notes. These are text/route annotations, not real terminal, bus, or component nodes.

## Edge Review

- Power topology is visually supported end to end: source/disconnect/ATS paths into SWGR buses; SWGR tie only through `TIE-BKR-21AB`; feeder breaker/transformer paths into MCCs; MCC bus taps to pump, fan, MOV, and CPT loads; CPT to AC panel; AC panel to rectifier; rectifier, battery, and inverter to the train-specific DC bus.
- `CT-21A` -- `RPS-PNL-A` and `CT-21B` -- `RPS-PNL-B` remain included: the short-dash instrument routes continue vertically from the CT symbols down to top terminals on the corresponding RPS panels.
- `VT-21A` -- `RPS-PNL-A` and `VT-21B` -- `RPS-PNL-B` remain included: the voltage-signal routes are continuous endpoint-to-endpoint instrument routes; the `VOLTAGE-SIG` text is only a route label and is not modeled as a node.
- `RELAY-86A` -- `CB-MPA1` and `RELAY-86B` -- `CB-MPB1` remain included: the dash-dot trip-control routes leave the 86 relays, run around the lower control-lane boundary, and return to the pump-breaker trip terminals marked `TRIP MPA1/MPB1`.
- No edges were added at line crossings without dots. The voltage-signal crossing near `MOV-RWST21A` and the analogous right-side route were treated as non-connections, consistent with the drawing note that crossings without dots are not connections.

## Changes From Diego Round01

None.

No nodes were added or removed. No edges were added or removed.
