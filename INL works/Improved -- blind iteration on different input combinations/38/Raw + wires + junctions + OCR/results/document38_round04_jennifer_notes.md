# Document 38 Round04 Jennifer Final Precision Sign-Off

## Scope And Sources

- Final precision sign-off used only resources under `C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\38\Raw + wires + junctions + OCR`.
- Reviewed `document38_round02_jennifer_nodes.csv`, `document38_round02_jennifer_edges.csv`, `document38_round02_jennifer_notes.md`, `document38_round03_diego_nodes.csv`, `document38_round03_diego_edges.csv`, and `document38_round03_diego_notes.md`.
- Reinspected the raw schematic and allowed visual aids/crops. The raw schematic remained authoritative; overlays, wire masks, wire nodes, and CSV aids were secondary.
- No GT, GT-derived feedback, evaluator output, external files, or off-the-shelf OCR were used.

## Saturation / Agreement

- Diego round03 mechanically matches Jennifer round02: no node-row differences and no edge-row differences were found.
- The saturated graph is accepted unchanged for Jennifer round04: 55 included nodes and 53 included undirected edge rows.
- Round04 nodes and edges were copied unchanged from the agreed round03/round02 graph.

## Final Precision Checks

- The eight logical bus/train nodes remain visually justified by labeled heavy busbars/trains: `BUS-4160A`, `BUS-4160B`, `BUS-480A`, `BUS-480B`, `125 VDC TRAIN A`, `125 VDC TRAIN B`, `BUS-120AC-A`, and `BUS-120AC-B`.
- Solid top power topology remains supported: source/generator/diesel paths to the 4.16 kV buses, the feeder chains through `CB-201/TR-201/CB-301`, and `BUS-480A/B -- CB-401A/B -- MCC-2A1/2B1`.
- The normally-open tie remains represented only by terminal edges `BUS-4160A -- CB-105` and `CB-105 -- BUS-4160B`. No direct `BUS-4160A -- BUS-4160B` edge is included.
- MCC fan-out remains exactly six visible load feeders per MCC, one to each visible pump/fan/MOV load.
- `RPS-PNL-A -- RELAY-27A` remains excluded. The dashed route near 27A/RPS-PNL-A reads as boundary/routing/control tray geometry and does not show clear terminal-to-terminal support; the thick `BUS-120AC-A` conductor stops before the relay area.
- `RPS-PNL-B -- RELAY-27B` remains excluded. `RELAY-27B` has a solid bus-side contact, but the dashed route from the RPS panel remains boundary/routing-like rather than a clear terminal-to-terminal connection.
- `125 VDC TRAIN A -- RELAY-86A` and `125 VDC TRAIN B -- RELAY-86B` remain included because each has a visible dashed vertical tap from the 125 VDC train to the corresponding lockout relay box.
- B-side asymmetry remains visually supported: `TR-CPT-B -- BUS-120AC-B` and `BUS-120AC-B -- RELAY-27B` are included. No `TR-CPT-A -- BUS-120AC-A` or `BUS-120AC-A -- RELAY-27A` equivalent is added because the A-side CPT/27A area lacks clear terminal contact.
- `GND-STA` remains an included visible node with no edge. The station ground symbol is shown as a single point only, and no clear terminal-to-terminal station-ground edge is visible.
- Crossings without filled dots were not treated as connectivity.

## Matrix

- The round04 adjacency matrix was regenerated from `document38_round04_jennifer_edges.csv` and `document38_round04_jennifer_nodes.csv` using `codes\build_matrix_from_edges.py`.
- Final round04 graph: 55 included nodes, 53 included edge rows, 53 unique undirected edges, and 0 duplicate edge rows.