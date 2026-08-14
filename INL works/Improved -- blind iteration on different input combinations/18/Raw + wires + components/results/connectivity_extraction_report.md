# Connectivity Extraction Report - Document 18

Only the raw schematic and Input resources-derived visual aids/crops were used. No GT/GT-derived feedback and no off-the-shelf OCR were used.

## Jennifer Corrections
- Corrected Diego R1 switchyard bus label from BUS-MAIN-230 to BB-SWYD-230.
- Promoted visually clear GRID-SWYD 1/2 source breakers into the accepted edge list.
- Added BB-SWYD-230 -> CB-GEN-ISO -> GEN-MAIN-1 and GEN-MAIN-1 taps to TR-UAT-1A/TR-UAT-1B.
- Kept SAT 1A to BUS-4160A and SAT/UAT/DG 1B paths to BUS-4160B.
- Confirmed BUS-4160A feeds BUS-480A/B and BUS-4160B feeds BUS-480C/D.
- Removed broad PLC-to-all-relays fan-out edges and replaced them with local dashed RPS harness segments.
- Excluded a B08 feeder because only B01-B07 are visually present on BUS-480B.

## Saturation
Diego R2 and Jennifer R2 use the same final edge set after Jennifer R1 corrections. No additional visually supported edge changes remained.

Final node count: 200

Final undirected edge count: 204

Primary artifacts: final_connectivity_matrix.csv, final_sparse_edges.csv, round matrices, uncertain_excluded_edges.csv, token_usage_estimate.md.
