# Document 27 Round 01 Diego Notes

## Scope

- Used only the raw schematic, allowed overlays/crops, `component_visual_ocr_labels.csv`, `wire_nodes.csv`, and visual inspection inside the allowed folder.
- Did not use Ground Truth, evaluator outputs, GT-derived feedback, or off-the-shelf OCR.
- Included every row from `component_visual_ocr_labels.csv` as a `physical_component` node.
- Added two visually supported physical nodes missed by the CSV: `PANEL-CTRL-MAIN` and `GND-EQ-B`.
- Added logical bus nodes only for visible/named shared conductors: `BUS-13.8KV`, `BUS-4160-A`, `BUS-4160-B`, `BUS-480-A`, `BUS-480-B`, `BUS-480-C`, `BUS-480-D`, `DC-BUS-125A`, and `DC-BUS-125B`.

## Counts

- Nodes: 201 total; 192 physical components; 9 logical buses.
- Included edge rows: 202.
- Edge kinds: bus_tie=3, control_interlock=16, ground=2, instrument_signal=27, power_feeder=154
- Confidence: high=194, medium=8

## Key Assumptions

- Solid one-line conductors are represented as `power_feeder`; bus tie breaker connections use `bus_tie`.
- Dashed control/status links are represented as `control_interlock`; dotted instrument links are represented as `instrument_signal`; dash-dot ground lines are represented as `ground`.
- Crossings without a filled dot or visually continuous terminal were not promoted to connections.
- Each 480 V load center is represented by a bus node connected to ten breaker branches; each breaker branch then connects through the shown disconnect/fuse to its served load.
- The 4160 V tie is represented as `BUS-4160-A -- CB-TIE-41 -- BUS-4160-B`, not as a direct bus-to-bus edge, so the tie breaker remains an explicit node.

## Ambiguities Kept In Graph

- `DS-A10 -> CHGR-125A` is medium confidence because the charger/battery block is visually close to the A10 branch and DC source enclosure, but the exact AC input route is crowded.
- `BUS-480-B -> CHGR-125B` is medium confidence because the visible solid tap to the B charger is not labelled with a separate breaker in the crop.
- `DC-BUS-125A -> DC-BUS-125B` is medium confidence: the drawing shows a continuous horizontal DC bus band with filled taps, but the A/B DC separation is not fully clear from the crop.
- `DC-BUS-125A/B -> PANEL-CTRL-MAIN` are medium-confidence dashed/status connections because the central panel tap is visually present but crowded by nearby vertical signal lines.
- `BUS-480-C -> GND-EQ-A` and `BUS-480-D -> GND-EQ-B` are medium-confidence ground edges following the dash-dot ground style to the labelled ground symbols.

## Files Written

- `results/document27_round01_diego_nodes.csv`
- `results/document27_round01_diego_edges.csv`
- `results/document27_round01_diego_adjacency_matrix.csv`
- `results/document27_round01_diego_matrix_summary.json`
