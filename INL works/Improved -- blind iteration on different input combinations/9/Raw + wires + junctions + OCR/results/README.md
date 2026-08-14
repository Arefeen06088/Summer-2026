# Document 9 Connectivity Extraction

Final saturated graph:

- Nodes: 180
- Edges: 192
- Matrix: `final_connectivity_matrix.csv`
- Edge list: `final_connectivity_edges.csv`

Final edge-kind counts:

{'solid_power': 132, 'solid_dc_control_power': 14, 'control_signal': 46}

Important decisions:

- Added 17 named bus/logical conductor nodes.
- Added visible missing nodes `RTD-PNL-A`, `RTD-PNL-B`, `TDR-SEQ-A`, `TDR-SEQ-B`.
- Corrected `JB-1A0/JB-2A0/JB-1BO/JB-2BO` to `JB-1A/JB-2A/JB-1B/JB-2B`.
- Corrected `CB-COMP-AI` to `CB-COMP-A`.
- Excluded uncertain `RTD-PNL-A -- RTD-PNL-B`.

No GT, GT-derived feedback, or off-the-shelf OCR was used.
