# Document 7 Round Summaries

Resource folder: `C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\7\Raw + components`

Allowed visual resources used:
- `raw -- synthetic_npp_electrical_schematic_clean (1).png`
- `detected_components_and_logical_overlay.png`
- crop aids generated from those two files only

No ground truth or GT-derived feedback was used. No off-the-shelf OCR was used.

## Round Progression

| round | role | nodes | asserted edges in matrix | saturation | notes |
|---|---:|---:|---:|---|---|
| 1 | Diego high-recall | 120 | 123 | no | Proposed all main solid feeders, MCC branches, selected clear dashed terminal paths, and held congested control paths uncertain. |
| 1 | Jennifer precision | 120 | 125 | no | Promoted two solid feeder edges (`LC-480A--BAT-125A`, `LC-480D--BCHG-125B`); rejected unsupported charger/battery shortcuts. |
| 2 | Diego high-recall | 120 | 125 | yes | Agreed with Jennifer's precision revision and kept `SR-101` isolated. |
| 2 | Jennifer precision final | 120 | 125 | yes | Confirmed saturated 120-node, 125-edge graph; uncertain dashed interlocks remain out of matrix. |

## Final Policy

- Undirected connectivity, symmetric dense CSV matrix.
- Diagonal cells are zero.
- Filled terminals, solid feeders, bus taps, explicit tie/disconnect components, and clear dashed terminal-to-terminal control lines are asserted.
- Raceway labels, area titles, crossings without filled dots, and congested dashed interlocks without clear terminal ownership are excluded and recorded as uncertain/rejected.
