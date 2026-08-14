# Document 23 Round 01 Diego Notes

## Method
- Worked only inside the allowed document 23 resource folder.
- Used the raw schematic, provided label overlays/crops, wire-node visual aids, and `component_visual_ocr_labels.csv` as a manual aid.
- Did not use Ground Truth, evaluator outputs, prior document results, Tesseract, RapidOCR, or off-the-shelf OCR.
- Modeled an undirected high-recall graph with adjacent component-to-bus/component-to-component edges; named buses are explicit nodes to avoid bus cliques.

## Outputs
- Nodes included: 200 (184 CSV physical components, 15 named logical buses, 1 added visible physical node `DC-DC-1`).
- Edges included: 231.
- Edge kind counts: {'power_solid': 142, 'control_signal_dashed': 65, 'instrument_dashed': 14, 'ground': 10}.
- Edge confidence counts: {'high': 163, 'medium': 55, 'low': 13}.
- Adjacency matrix entries are symmetric 1/0 connectivity flags using the same node order as the node/header list.

## Key Assumptions
- Solid heavy conductors are `power_solid`; short dashed local interlocks are `control_signal_dashed`; long dashed meter/instrument taps are `instrument_dashed`; light solid ground drops are `ground`.
- Crossings without dots were treated as non-connections, especially the 4160V-to-480V feeder drops crossing ESF buses in the upper half of the sheet.
- The six 480V load-center interiors use the repeated visible pattern: feeder breaker -> disconnect -> transformer -> main breaker -> named 480V bus, then three MCCs, panel, instrument, ground, and local loads.
- Local JB/relay/heater/valve dashed paths in each 480V load center were retained with medium/low confidence for high recall.
- `BUS-125DC-A` and `BUS-125DC-B` are connected only through `CB-DCTIE`, not as a direct bus-to-bus edge.
- `BUS-120AC-A/B` are fed through `INV/UPS/CB-UPS` chains from their corresponding 125VDC buses.
- `DC-DC-1` is visibly named in the bottom distribution but was not present in the component CSV; it was added as a medium-confidence physical node between the lower AC/control area and `BUS-24DC-C`.

## Ambiguous Or Lower Confidence Items
- `CB-1C-FDR` and `CB-2C-FDR` were modeled from `BUS-4160-ESF-A`; the visible routing supports the lower ESF-A path, but long conductor runs and crossings make these medium-confidence.
- `CB-DC-A` and `CB-DC-B` were connected upstream to `BUS-480-2A` and `BUS-480-2B` respectively as medium-confidence inferred feeder sources into the DC distribution.
- RPS/control-strip edges among fuses, relays, annunciators, recorders, RPS panels, DCS panels, and control JBs are modeled as adjacent dashed/control relationships, not guaranteed functional signal direction.
- `RELAY-KTIE` to `BUS-24DC-C` is low confidence; a clearer direct path is via `PNL-RADMON`.

## Rejected/Not Modeled
- Title block, reference drawing tables, system block diagram boxes, and the visible `AUX METERING BUS` schedule were not added as graph nodes because they do not show connected schematic wiring in the raw sheet.
- No unnamed wire nodes were introduced; only named logical buses and the visible named `DC-DC-1` device were added beyond the CSV components.
