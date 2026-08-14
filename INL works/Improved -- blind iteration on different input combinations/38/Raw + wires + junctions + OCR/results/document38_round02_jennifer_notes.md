# Document 38 Round02 Jennifer Notes

## Scope And Sources

- Precision review used only files in `C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\38\Raw + wires + junctions + OCR`.
- Raw schematic `raw -- synthetic_npp_schematic_improved.png` was treated as authoritative. Overlays, wire-node files, crops, and `component_visual_ocr_labels.csv` were used only as aids.
- No GT, GT-derived feedback, evaluator output, or external files were used. No off-the-shelf OCR was used.

## Node Review

- Retained Diego's 47 physical component nodes and 8 logical bus/train nodes.
- The 8 logical bus/train names are visually justified: `BUS-4160A`, `BUS-4160B`, `BUS-480A`, `BUS-480B`, `125 VDC TRAIN A`, `125 VDC TRAIN B`, `BUS-120AC-A`, and `BUS-120AC-B` all correspond to visible labeled heavy busbars/trains.
- `GND-STA` remains included as a visible physical ground symbol, but isolated in the graph. The raw sheet shows station ground as a single-point ground symbol and no clear terminal-to-terminal edge to a component.

## Edge Review Decisions

- Retained the top 4.16 kV sequence `GEN-U2A -- CB-101 -- TR-UAT-2A -- BUS-4160A`, `DG-2A -- CB-103 -- BUS-4160A`, `TR-SUT-2B -- CB-102 -- BUS-4160B`, and `DG-2B -- CB-104 -- BUS-4160B`.
- Retained `BUS-4160A -- CB-105` and `CB-105 -- BUS-4160B` as terminal edges only. No direct `BUS-4160A -- BUS-4160B` edge is included.
- Retained the 4.16 kV to 480 V feeder chains through `CB-201A/TR-201A/CB-301A` and `CB-201B/TR-201B/CB-301B`, plus `BUS-480A/B -- CB-401A/B -- MCC-2A1/2B1`.
- Retained exactly six MCC load feeders per MCC: RHR pump, CCW pump, SW pump, CR fan, RHR MOV, and SI MOV on each train. No extra MCC fan-out edges were added.
- Retained lower power edges from `BUS-480A` to `TR-CPT-A` and `CHGR-2A`; `CHGR-2A`, `BAT-125A`, and `INV-2A` to `125 VDC TRAIN A`; `INV-2A` to `BUS-120AC-A`; and `BUS-120AC-A` to `RPS-PNL-A`.
- Retained B-side equivalents, including `TR-CPT-B -- BUS-120AC-B` and `BUS-120AC-B -- RELAY-27B`, because the raw schematic shows a solid vertical CPT-B lead landing on the 120 VAC B bus/relay terminal area. No symmetric `TR-CPT-A -- BUS-120AC-A` edge was added because the A-side CPT lower lead stops at an isolated dot with a visible gap to the 120 VAC A bus.
- Retained `125 VDC TRAIN A -- RELAY-86A` and `125 VDC TRAIN B -- RELAY-86B`; each has a visible dashed vertical tap from the 125 VDC train to the lockout relay box.

## Removed From Diego Round01

- Removed `RPS-PNL-A -- RELAY-27A`. The relay is visually labelled for UV BUS A, but the dashed path near the panel reads as a boundary/routing line and does not clearly enter the relay as a terminal-to-terminal connection. The thick `BUS-120AC-A` conductor also ends with a visible gap before the relay.
- Removed `RPS-PNL-B -- RELAY-27B`. Although `RELAY-27B` has a clear solid bus connection to `BUS-120AC-B`, the dashed route from `RPS-PNL-B` does not provide clear terminal-to-terminal support and appears boundary/routing-like.

## Ambiguity Notes

- The A/B CPT secondary treatment is intentionally asymmetric because only the B-side has visually supported contact with the 120 VAC bus. The A-side label and transformer rating alone were not used to infer a missing connection.
- The `RELAY-27A` node remains visible but isolated after precision review because no terminal-supported edge is clear in the raw schematic.
- Crossings without filled dots were not treated as connections.

## Matrix

- Final round02 graph: 55 included nodes and 53 included edge rows. The adjacency matrix was regenerated from the round02 edge CSV using `codes\build_matrix_from_edges.py`.