# Document 38 Round03 Diego Saturation Notes

## Scope And Sources

- Used only resources under `C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\38\Raw + wires + junctions + OCR`.
- Reviewed `document38_round01_diego_nodes.csv`, `document38_round01_diego_edges.csv`, `document38_round01_diego_notes.md`, `document38_round02_jennifer_nodes.csv`, `document38_round02_jennifer_edges.csv`, and `document38_round02_jennifer_notes.md`.
- Reinspected the raw schematic and aids/crops including `raw__row3_col1.png`, `raw__row3_col2.png`, `raw__bottom_left.png`, `raw__bottom_right.png`, `nodes__bottom_left.png`, `nodes__bottom_right.png`, `raw__top_band.png`, `raw__middle_band.png`, `nodes__top_band.png`, and `nodes__middle_band.png`.
- Raw schematic remained authoritative. Overlays and CSVs were used only as visual aids. No off-the-shelf OCR, GT, GT-derived feedback, evaluator output, or outside files were used.

## Round03 Decision

- I agree with Jennifer round02 and copied her 55-node / 53-edge graph for Diego round03.
- The only graph difference between Diego round01 and Jennifer round02 was the removal of two dashed control edges:
  - `RPS-PNL-A -- RELAY-27A`
  - `RPS-PNL-B -- RELAY-27B`
- After reinspection, neither removed edge has clear terminal-to-terminal visual support. The dashed paths near the RPS panels and 27 relays read as boundary/routing/control tray lines and do not visibly enter both component terminals. They remain removed in round03.

## Dispute Checks

- `125 VDC TRAIN A -- RELAY-86A` remains included. The raw lower-left area shows a dashed vertical tap descending from the 125 VDC train tap into the RELAY-86A lockout relay box.
- `125 VDC TRAIN B -- RELAY-86B` remains included. The raw lower-right area shows the corresponding dashed vertical tap from the 125 VDC train B bus into RELAY-86B.
- The B-side asymmetry remains justified. `TR-CPT-B -- BUS-120AC-B` and `BUS-120AC-B -- RELAY-27B` have visible solid conductor support in the raw drawing: the CPT-B lower lead lands at the 120 VAC B bus / relay-27B terminal area.
- No symmetric `TR-CPT-A -- BUS-120AC-A` edge was added. The CPT-A lower lead stops at an isolated filled dot with a visible gap to the 120 VAC A bus.
- No `BUS-120AC-A -- RELAY-27A` edge was added. RELAY-27A is visually labeled as UV BUS A, but the thick 120 VAC A bus ends before the relay area and there is no clear solid or dashed terminal landing.
- No `GND-STA` edge was added. The station ground symbol is visible, but the dashed/dotted route is not a clear component terminal-to-ground connection; it is consistent with the note that station ground is shown single point only.

## Solid Power And Bus Review

- Top 4.16 kV source/generator/diesel paths, the normally-open `CB-105` terminal edges, and the 4.16 kV-to-480 V transformer feeder chains remain as Jennifer round02 modeled them.
- `CB-105` is kept as two device terminal edges only; no direct `BUS-4160A -- BUS-4160B` edge is added.
- The 480 V tie gap between `BUS-480A` and `BUS-480B` remains non-connective because the raw drawing explicitly marks the reserved space with no connection shown.
- Six MCC load feeders per train remain included, one to each visible motor/MOV/fan load. No additional MCC internal bucket or unlabeled logical nodes were added.

## Matrix

- The round03 adjacency matrix was regenerated from `document38_round03_diego_edges.csv` and `document38_round03_diego_nodes.csv` using `codes\build_matrix_from_edges.py`.
