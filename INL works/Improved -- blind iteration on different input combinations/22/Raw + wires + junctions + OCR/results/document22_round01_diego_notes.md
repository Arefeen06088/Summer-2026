# Document 22 Round 01 Diego Notes

## Scope

- Inspected only the allowed resource folder: `C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\22\Raw + wires + junctions + OCR`.
- Used the raw schematic, component label overlay/CSV, wire masks/overlays, wire node overlay/CSV, and precision review crops as visual aids.
- Did not use Ground Truth, evaluator outputs, prior document results, or off-the-shelf OCR.
- Applied the visible schematic rule: orthogonal wires; dots indicate bus/junction connections; wire crossings without dots are not treated as connected.

## Output Summary

- Nodes: 200 total.
- Edges: 209 total.
- Edge kinds: {'power_solid': 170, 'control_signal_dashed': 33, 'ground': 6}.
- Edge confidence counts: {'high': 168, 'medium': 40, 'low': 1}.

## Node Decisions

- Included every detected physical component from `component_visual_ocr_labels.csv`.
- Added explicit named bus/logical nodes for BUS-13A/B, BUS-4160-A/B/C/D, BUS-480-A/B/C/D, BUS-125A/B, and BUS-UPS-A/B.
- Added five visually supported D-train physical nodes not present in the CSV: INST-PT-D, CB-CH-D, CB-VLV1-D, CB-VLV2-D, and CB-SPARE-D. These are marked medium confidence and `added_visible_not_in_component_csv`.

## Connectivity Assumptions

- Edges are direct adjacent electrical objects and named bus segments, not all-pairs cliques across a full bus.
- Solid power and bus links are `power_solid`; dashed relay/control/instrumentation links are `control_signal_dashed`; grounding symbols are `ground`.
- MCC load branches are represented through their visible feeder breaker and load. CT/RHR branches include both CT adjacency and a medium-confidence direct MCC-to-RHR-breaker edge to preserve recall.

## Ambiguous / Lower-Confidence Items

- SWYD-345 to CB-13A1/CB-13B1 is high-level source branching; both are retained at medium confidence because the top source geometry is visually compact.
- RELAY-87U dashed/protection wiring appears associated with the upper 13 kV/incoming section; retained to BUS-13A and CB-4B-IN at medium confidence.
- SYNC-PNL-1 dashed/control wiring is near the DG-A/4160-A section; retained to CB-DG-A at medium confidence and BUS-4160-A at low confidence.
- CB-DC-A1 and CB-DC-B1 upstream AC taps are retained to BUS-480-A and BUS-480-B at medium confidence because the DC charger source area is visually compressed.
- XFMR-PT-1 has clear instrument/control links to METER-V01 and METER-A01, but its upstream bus/source was not clear enough to add a bus edge.
- ANN-PNL-CR and REC-SEQ-1 UPS/control connections are retained at medium confidence where they share the visible lower control/UPS wiring area.
