# Document 8 Round Summaries

Resource folder: `C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\8\Raw + components`

Allowed visual resources used:
- `raw -- synthetic_npp_schematic_improved_local_refined_v3.png`
- `detected_components_and_logical_overlay.png`
- crop aids generated from those two files only

No ground truth or GT-derived feedback was used. No off-the-shelf OCR was used.

## Round Progression

| round | role | nodes | asserted edges in matrix | saturation | notes |
|---|---:|---:|---:|---|---|
| 1 | Diego high-recall | 120 | 125 | no | Proposed top 4.16 kV, safety buses, 480 V buses, load feeders, selected sensing/control paths, and held congested dashed bundles uncertain. |
| 1 | Jennifer precision | 120 | 127 | no | Corrected `MCC-2C` ownership, removed unsupported `PN-480-A/B` shortcuts, and promoted supported B charger/valve edges. |
| 2 | Diego high-recall | 120 | 127 | yes | Accepted Jennifer's edge ownership revision. |
| 2 | Jennifer precision final | 120 | 127 | yes | Confirmed saturated graph; dashed interlock bundles and `CB-EDG-C--BUS-4160-S2B` remain uncertain. |

## Final Policy

- Undirected connectivity, symmetric dense CSV matrix.
- Diagonal cells are zero.
- Filled terminals, solid feeders, bus taps, explicit tie/disconnect components, clear sensing/control links, and explicit ground references are asserted.
- Terminal block references, annotation boxes, phase labels, cable labels, crossings without filled dots, and ambiguous dashed interlock/raceway bundles are excluded and recorded as uncertain/rejected.
