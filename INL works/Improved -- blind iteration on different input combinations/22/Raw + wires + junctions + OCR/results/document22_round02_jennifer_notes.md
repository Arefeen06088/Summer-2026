# Document 22 Round 02 Jennifer Notes

## Scope

- Inspected only the allowed document 22 resource folder and its `results`, `codes`, and `precision_review_crops` children.
- Used the raw schematic as authoritative, with Diego Round 01 files and the provided manual visual/OCR-style aids only as review aids.
- Did not use Ground Truth, evaluator outputs, prior document results, or off-the-shelf OCR.
- Applied the raw schematic rule: dots denote bus/junction connections; crossings without dots are not connected.

## Summary

- Nodes: 200.
- Edges: 203.
- Edge kinds: {'power_solid': 154, 'control_signal_dashed': 37, 'instrument_dashed': 6, 'ground': 6}.
- Removed 6 Round 01 edges that were not directly supported by the raw schematic.
- Confirmed visible D-train additions absent from the component CSV: INST-PT-D, CB-CH-D, CB-VLV1-D, CB-VLV2-D, CB-SPARE-D.

## Removed Edges

- Removed MCC-AA -> CB-RHR-A, MCC-BA -> CB-RHR-B, MCC-CA -> CB-RHR-C, and MCC-DA -> CB-RHR-D. The RHR branches are represented through INST-CT-A/B/C/D, so the direct MCC-to-RHR breaker shortcuts were overconnected.
- Removed SOL-SDV-A -> DIODE-OR-A and SOL-SDV-B -> DIODE-OR-B. The raw schematic shows SDV dashed control links from the DC MCCs and separate solid diode-to-125 VDC bus branches, but no visible SDV-to-diode bridge.

## Corrected / Retained Cases

- Kept SWYD-345 -> CB-13A1 and SWYD-345 -> CB-13B1 after visual check of the compact top source branch.
- Kept RELAY-87U dashed edges to BUS-13A and CB-4B-IN at medium confidence; the dashed path is visible, but the exact protective function remains ambiguous.
- Kept SYNC-PNL-1 dashed edges to CB-DG-A and BUS-4160-A; both are visible dashed/control adjacencies, not solid bus cliques.
- Kept BUS-480-A -> CB-DC-A1 and BUS-480-B -> CB-DC-B1 at medium confidence because the upstream AC charger taps are visually long/compressed but raw-supported.
- Reclassified BUS-480-A/B/C/D -> INST-PT-A/B/C/D as `instrument_dashed`.
- Reclassified UPS bus taps to INST-RACK, PNL-RPS, PLC-SAF, ANN-PNL-CR, and REC-SEQ-1 as `control_signal_dashed` because the raw taps are dashed from visible bus dots.
- Kept XFMR-PT-1 -> METER-V01 and XFMR-PT-1 -> METER-A01 as `instrument_dashed`; no upstream XFMR-PT-1 source edge was added.

## Remaining Ambiguities

- RELAY-87U and the DC charger upstream taps remain the main medium-confidence endpoints.
- No unnamed wire nodes were created, and no all-pairs bus cliques were added.
