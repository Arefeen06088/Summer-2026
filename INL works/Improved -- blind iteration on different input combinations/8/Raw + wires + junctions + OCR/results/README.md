# Document 8 Connectivity Extraction

Final saturated graph:

- Nodes: 120
- Edges: 138
- Matrix: `final_connectivity_matrix.csv`
- Edge list: `final_connectivity_edges.csv`

Important label decisions:

- Corrected `NCC-*` load centers to `MCC-*`.
- Corrected `MOV-8816A/B` to `MOV-8810A/B`.
- Corrected `GND-AJ` to `GND-A`.
- Removed false CSV component `CB-303`; added visually supported missing `CB-52B`.
- Added visible missing nodes `MCC-2C`, `PN-125B`, and `PUMP-AF-2B`.
- Did not include `TB01`-`TB15`; their short stubs did not show supported schematic connectivity.

Final edge-kind counts:

{'solid_ac_power': 85, 'ct_pt_signal': 8, 'interlock_trip_permit': 20, 'equipment_ground': 2, 'solid_dc_125': 14, 'solid_120vac_control': 9}

No GT, GT-derived feedback, or off-the-shelf OCR was used. The title-block connection count was treated as sanity metadata; unsupported symmetry edges were rejected in favor of visual precision.
