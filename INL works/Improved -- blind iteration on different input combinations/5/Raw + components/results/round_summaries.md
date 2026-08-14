# Document 5 Round Summaries

Resource folder: `C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\5\Raw + components`

Allowed visual resources used:
- `raw -- synthetic_npp_electrical_schematic_final_cleaned_v4.png`
- `detected_components_and_logical_overlay.png`
- crop aids generated from those two files only

No ground truth or GT-derived feedback was used. No off-the-shelf OCR was used.

## Round Progression

| round | role | nodes | asserted edges in matrix | saturation | notes |
|---|---:|---:|---:|---|---|
| 1 | Diego high-recall | 112 | 129 | no | Included four CP-ESFAS-to-INST-NSSS dashed trunk edges as high-recall assertions. |
| 1 | Jennifer precision | 112 | 129 | no | Kept Diego topology but marked several alternatives uncertain/rejected. |
| 2 | Diego high-recall | 112 | 125 | near | Confirmed MCC labels are `MCC-1A1` style, kept ATS feeds, demoted CP-to-instrument links. |
| 2 | Jennifer precision final | 112 | 125 | yes | Agreed with 125 asserted edges and demoted four CP-to-instrument links to uncertain. |

## Final Demoted Edges

These were asserted in round 1 and excluded from the final matrix:
- `CP-ESFAS-1 -- INST-NSSS-A`
- `CP-ESFAS-2 -- INST-NSSS-A`
- `CP-ESFAS-1 -- INST-NSSS-B`
- `CP-ESFAS-2 -- INST-NSSS-B`

## Final Matrix Policy

- Undirected connectivity, symmetric dense CSV matrix.
- Diagonal cells are zero.
- Filled bus taps/component terminals are asserted.
- Crossings without filled dots are not asserted.
- Dashed control/sensing connections are asserted only where terminal assignment is visually supported.
- `GND-GRID` is included as a labeled node but left isolated because the agents treated dotted grounding as a separate grounding layer rather than asserted power/control adjacency.
