# Document 40 Round 03 Diego Saturation Notes

Scope followed: only resources inside the document-40 folder were used. I did not use GT, GT-derived feedback, evaluator output, outside folders, previous-document final answers, or off-the-shelf OCR. The raw schematic remained authoritative; the in-folder label CSV, wire-node table, overlays, and local crops were used only as visual aids.

## Round Decision

No changes were made from Jennifer round02. I copied the round02 57-node / 58-edge graph forward to `document40_round03_diego_nodes.csv` and `document40_round03_diego_edges.csv`.

Saturation is likely reached for the visible connectivity in this schematic: the remaining uncertain edges are long dashed or dash-dot routes, but each still has visual endpoint support and no new defensible node or edge candidates were found.

## Focus Recheck

### MCC Enclosure And Bus Split

Kept `MCC-21A` plus `MCC-21A-480V-3PH`, and kept `MCC-21B` plus `MCC-21B-480V-3PH`.

Visual basis: on each train, the transformer feeder lands at the MCC enclosure/top termination, while a separate heavy 480 V 3PH rail inside the MCC carries multiple tapped loads. Modeling the enclosure component and the internal multi-tap bus as separate nodes connected by an `internal_bus` edge preserves both drawn facts. Collapsing them would remove either the visible MCC component/enclosure or the true internal busbar node.

### Excluded Labels

Kept excluded:

- `TRAIN-A-480V-SAFETY-CHANNEL`
- `TRAIN-B-480V-SAFETY-CHANNEL`
- `SOURCE-NORMAL`
- `SOURCE-ALTERNATE`
- `RPS-CH-A-CONTROL-LANE`
- `RPS-CH-B-CONTROL-LANE`
- `VOLTAGE-SIG-A`
- `VOLTAGE-SIG-B`

These are title boundaries, source notes, lane captions, or route labels. They are not drawn terminal symbols, buses, switchgear, or components. The voltage signal routes are represented by endpoint edges instead of label nodes.

### Medium-Confidence Edges

Kept all six medium-confidence edges:

- `CT-21A` -- `RPS-PNL-A`: short-dash CT signal route continues down to an RPS panel top terminal.
- `VT-21A` -- `RPS-PNL-A`: dashed voltage-signal route continues from the VT route to the RPS panel; `VOLTAGE-SIG-A` is only a route label.
- `RELAY-86A` -- `CB-MPA1`: dash-dot trip route reaches the `TRIP MPA1` breaker terminal and the `RELAY-86A` chain.
- `CT-21B` -- `RPS-PNL-B`: short-dash CT signal route continues down to an RPS panel top terminal.
- `VT-21B` -- `RPS-PNL-B`: dashed voltage-signal route continues from the VT route to the RPS panel; `VOLTAGE-SIG-B` is only a route label.
- `RELAY-86B` -- `CB-MPB1`: dash-dot trip route reaches the `TRIP MPB1` breaker terminal and the `RELAY-86B` chain.

### Missing-Edge Search

No missing supported edges were found in the requested areas:

- LOCA/JB/RPS paths remain `LOCA-SIG-A` -- `JB-21A` -- `RPS-PNL-A` and `LOCA-SIG-B` -- `JB-21B` -- `RPS-PNL-B`.
- Inverters remain connected both to their DC buses by solid 125 VDC feeders and to their RPS panels by dashed control lines.
- DC buses remain connected to rectifiers, batteries, and inverters only where solid feeders meet junction dots.
- CPT/AC panel/rectifier chains remain complete on both trains.
- Source/ATS/SWGR paths remain complete, with the only A-B switchgear connection through `TIE-BKR-21AB`.

### Crossings Without Dots

No line crossing without a dot was treated as a connection. The most important cases are the voltage-signal routes near `MOV-RWST21A` and `MOV-RWST21B`; both are visually non-junction crossings, and the A-side crop explicitly labels the crossing as `NO DOT = NO JUNCTION`.

## Changes From Jennifer Round02

None. No nodes were added or removed, and no edges were added or removed.
