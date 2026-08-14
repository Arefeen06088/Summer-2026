# Document 6 Round Summaries

Resource folder: `C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\6\Raw + components`

Allowed visual resources used:
- `raw -- synthetic_npp_electrical_schematic_variant3_redo_clean_v7.png`
- `detected_components_and_logical_overlay.png`
- crop aids generated from those two files only

No ground truth or GT-derived feedback was used. No off-the-shelf OCR was used.

## Round Progression

| round | role | nodes | asserted edges in matrix | saturation | notes |
|---|---:|---:|---:|---|---|
| 1 | Diego high-recall | 105 | 103 | no | Proposed solid power, selected same-channel dashed control, and explicit ground-bond edges. |
| 1 | Jennifer precision | 105 | 103 | no | Kept Diego topology exactly; kept ambiguous CT/sensing/control trunks out of matrix. |
| 2 | Diego high-recall | 105 | 103 | yes | No deltas; confirmed uncertain edges should remain excluded. |
| 2 | Jennifer precision final | 105 | 103 | yes | Confirmed final 105-node, 103-edge graph and kept uncertain edges out of the matrix. |

## Final Policy

- Undirected connectivity, symmetric dense CSV matrix.
- Diagonal cells are zero.
- Filled terminals, solid feeders, bus taps, explicit tie/disconnect components, selected same-channel dashed terminal paths, and labeled ground bonds are asserted.
- Dashed shared corridors, crossings without filled dots, and ambiguous sensor/control trunks are excluded and recorded as uncertain/rejected.
