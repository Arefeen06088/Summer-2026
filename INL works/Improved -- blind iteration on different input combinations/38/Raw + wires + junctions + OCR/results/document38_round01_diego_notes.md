# Document 38 Round01 Diego Notes

## Scope And Sources

- Used only files in `C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\38\Raw + wires + junctions + OCR`.
- Raw schematic `raw -- synthetic_npp_schematic_improved.png` was treated as authoritative.
- Aids inspected: `component_visual_ocr_labels.csv`, `wire_nodes.csv`, `component_labels_banners_overlay.png`, `wires_mask_overlay.png`, `wire_nodes_overlay.png`, and precision review crops.
- No off-the-shelf OCR was used. Component text came from the provided visual OCR CSV and manual visual inspection of the raw/crops.

## Node Decisions

- Included all 47 detected physical components from `component_visual_ocr_labels.csv`.
- Added 8 visually labeled logical buses/trains: `BUS-4160A`, `BUS-4160B`, `BUS-480A`, `BUS-480B`, `125 VDC TRAIN A`, `125 VDC TRAIN B`, `BUS-120AC-A`, and `BUS-120AC-B`.
- MCC internal horizontal bars were represented by the physical MCC nodes (`MCC-2A1`, `MCC-2B1`) rather than separate unlabeled logical bus nodes.
- `GND-STA` is included as a physical component. I did not add a component edge to it because the visible dashed/dotted grounding route is not a clear terminal-to-terminal connection to any detected device; the general note also says station ground is shown single point only.

## Connectivity Rules Applied

- Filled dots and continuous same-line conductors were treated as connections.
- Crossings or near-crossings without filled dots were not treated as connectivity.
- The normally-open `CB-105` is represented as two terminal edges (`BUS-4160A`--`CB-105` and `CB-105`--`BUS-4160B`), not as a direct bus-to-bus edge.
- The 480 V tie gap between `BUS-480A` and `BUS-480B` was not connected because the raw sheet explicitly labels it reserved space with no connection shown.
- Dashed control edges were included only where a route visually reaches a bus/panel/relay terminal area. Lower-confidence dashed entries are marked and explained in the edge notes.

## Ambiguities

- `TR-CPT-A` appears to have a 480 V primary feed from the left-side `BUS-480A` auxiliary feeder, so `BUS-480A`--`TR-CPT-A` is included at 0.90 confidence. Its lower lead terminates left of `BUS-120AC-A` with an apparent gap, so no `TR-CPT-A`--`BUS-120AC-A` edge was included.
- `TR-CPT-B` has a visible lower vertical lead landing at the `BUS-120AC-B`/`RELAY-27B` area, so `TR-CPT-B`--`BUS-120AC-B` is included at 0.78 confidence.
- `RPS-PNL-A`--`RELAY-27A` and `RPS-PNL-B`--`RELAY-27B` are included as dashed control edges with reduced confidence because the dashed routes are visually plausible terminal routes but also resemble control boundary/riser routing.
- I did not directly connect `BUS-120AC-A` to `RELAY-27A`: the relay label says UV BUS A, but the raw drawing shows a clear gap from the thick AC bus endpoint to the relay box.
- I did not add dashed edges from `RELAY-86A/B` to the RPS panels because the visible dashed path most clearly supports 125 VDC train taps to the lockout relays, not a separate relay-to-panel terminal run.
