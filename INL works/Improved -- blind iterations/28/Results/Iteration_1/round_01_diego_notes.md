# Round 01 Diego Notes - Doc 28 Iteration 1

## Scope statement
I inspected only `C:\Asif_all_python_projects\INL\Improved -- blind iterations\28\Input resources` and derived/crop artifacts already present in `C:\Asif_all_python_projects\INL\Improved -- blind iterations\28\Codes and artifacts`. The raw schematic image was treated as primary evidence; OCR/component/wire overlays and prepared crops were used only as aids. No GT, GT-derived evaluator output, score feedback, or resources from any other document/iteration were used.

## Node list rationale
- Matrix node count: 188.
- Edge count: 196 undirected adjacencies.
- Nodes were seeded from `component_labels_list.csv`, then checked against the raw/crop images.
- Corrected OCR inventory labels to raw-visible tags: `TIC-203` -> `TCV-203`; `M-301` -> `MX-301`.
- Added named logical/header/terminal nodes beyond inventory where the raw drawing shows a named box or named terminal directly tied to piping/control: H-N2-001, H-CCW-SUC, H-CCW-DIS, H-SW-RET, H-CCW-RET, H-CD-001, H-SMP-001, H-CD-REL, H-WW-001, H-DR-001, H-IA-001, VSR, TIE-IN, HV-103, LI-301, TCV-203, MX-301.
- Excluded anonymous wire nodes and unlabeled elbows/intersections. Long headers were represented by adjacent connected named items rather than clique-expanded across every component on the same line.

## Raw-visible non-inventory nodes added
- `H-N2-001`
- `H-CCW-SUC`
- `H-CCW-DIS`
- `H-SW-RET`
- `H-CCW-RET`
- `H-CD-001`
- `H-SMP-001`
- `H-CD-REL`
- `H-WW-001`
- `H-DR-001`
- `H-IA-001`
- `VSR`
- `TIE-IN`
- `HV-103`
- `LI-301`
- `TCV-203`
- `MX-301`

## Inventory labels or OCR artifacts omitted/corrected
- TIC-203 (OCR/component-list misread; raw label is TCV-203)
- M-301 (OCR/component-list split/misread; raw label is MX-301/static mixer)
- C1/C2 and numbered triangle/bubble continuation marks
- Line-number tags such as 6"-CCW-0008-A, 1"-REL-0007-A, etc.
- NSR/spare-blind/cap text annotations where no connected named object was drawn

## Edge evidence by schematic region

### 02_tank101_feed_and_level
- SW/feed line traced as `HV-210 - STR-201 - MOV-210`, with `VV-101` down to `TK-101`.
- Makeup line traced as `HV-131 - STR-131 - LV-101 - TK-101`; `LIC-101 - LT-101` and `LIC-101 - LV-101` retained as visible dashed instrument/control relationships.
- Level instruments `LSHH-101`, `LSLL-101`, and `LT-101` are tied to `TK-101` as raw-visible tank-level instrumentation.
- Nitrogen blanket line traced as `HV-701 - H-N2-001 - PCV-701 - TK-101`.
- CCW suction path uses `HV-101 - STR-101 - MOV-102 - H-CCW-SUC`, and `TK-101 - H-CCW-SUC` for the visible suction header connection. `HV-103`/`DV-101` are retained on the tank drain/bottom branch.

### 03_filter_pump_101_trains
- Train A: `H-CCW-SUC - HV-104A - P-101A - CV-105A - HV-106A - FLT-101A - HV-107A - HV-108A - H-CCW-DIS`.
- Train B: `H-CCW-SUC - HV-104B - P-101B - CV-105B - HV-106B - FLT-101B - HV-107B - HV-108B - H-CCW-DIS`.
- `PDT-101A/B` retained as visible differential-pressure instruments on the filter trains. `PT-102` is tied locally to `H-CCW-SUC`. The `HV-109 - DPV-110 - HV-111` bypass/relief run is included locally.

### 04_heat_exchanger_201_top
- CCW side: `H-CCW-DIS` feeds `HV-201A/B - HX-201A/B - HV-202A/B - H-CCW-RET`.
- SW/control side retained as local paths through `HV-211A/B`, `FT-211A/B`, `FCV-211A/B`, `HX-201A/B`, `HV-212A/B`, and `H-SW-RET`.
- Return/control path retained as `H-CCW-RET - FT-201 - FCV-201 - MOV-205 - TIE-IN`, with `FIC-201 - FCV-201` and `FT-201 - FIC-201` as visible control links.
- Pressure-control line retained as `PT-213 - PIC-213 - PCV-213`, with local process path through `PSV-215 - HV-213 - PCV-213 - H-SW-RET`.
- Temperature/control bypass retained as `H-CCW-DIS - HV-203 - TCV-203 - HV-204 - H-CCW-RET`, with `TT-211B - TCV-203` signal.

### 05_pressure_control_121_130 and 06_junction_boxes_right
- Pressure branch retained as `H-CCW-DIS - HV-120 - PCV-121 - RO-122 - H-CCW-RET`, with `PIC-121 - PCV-121` control link.
- `PSV-130` and `PSV-131` included as visible relief valves; `PSV-131 - FLT-501 - HV-501 - VSR` captures the vent-filter path, and `PT-501 - FLT-501` captures the pressure tap.
- `JB-101`, `JB-201`, `JB-301`, and `DCS-001` are raw-visible named control objects; only conservative direct panel/system adjacencies were added where the schematic shows connected signal routing.

### 07_vv_header_and_sample
- Vacuum/vent valve header retained as the visible sequence `VV-151A - VV-151B - VV-152A - VV-152B - VV-153A - VV-153B - VV-154`.

### 08_tank301_suction, 09_pump301_discharge, 10_spray_header_501
- Tank/instrument ties retained for `TK-301` with `VV-301`, `V-301`, `LT-301`, `LI-301`, `LSL-301`, and `DV-301`/`VV-302` branch.
- Chemical dosing train A: `TK-301 - HV-301 - STR-301 - P-301A - CV-301A - HV-302A - H-CD-001`.
- Chemical dosing train B: `TK-301 - HV-303 - P-301B - CV-301B - HV-302B - H-CD-001`.
- Dosing header downstream retained as `H-CD-001 - HV-306 - FT-301 - FCV-301 - HV-307 - MX-301 - HV-308 - IQ-301`, with `FIC-301 - FCV-301` and `FT-301 - FIC-301`.
- Sample line retained as `H-SMP-001 - SPV-501 - SPV-502 - SPV-503 - SPV-504 - SPV-505 - SPV-506 - SC-501 - SPN-501`.

### 11_tank302_and_p302
- Biocide tank train retained as `TK-302 - HV-304 - P-302 - CV-302 - HV-305 - H-CD-001`.
- `LT-302`, `VV-302`, and `DV-302` are tied locally to `TK-302`; relief path `P-302 - PSV-302 - H-CD-REL` is retained.

### 12_level_control_401
- Waste collection tank/pump trains retained as `V-401 - HV-401A - P-401A - CV-401A - H-WW-001` and `V-401 - HV-401B - P-401B - CV-401B - H-WW-001`.
- Waste-water outlet retained as `H-WW-001 - MOV-402 - HV-403`.
- Level/control links retained among `V-401`, `LT-401`, `LIC-401`, `LI-401`, `LSHH-401`, `LSL-401`, `LCP-401`, `CP-101`, and `PLC-101` where visible dashed lines terminate on named objects.

### 13_bottom_sov_header
- Drain header sequence retained as `H-DR-001 - DV-141 - DV-142A - DV-142B - DV-143A - DV-143B - DV-144A - DV-144B - DV-201A - DV-201B - H-WW-001`.
- Instrument-air/solenoid header retained as `H-IA-001 - SOV-201 - SOV-203 - SOV-301 - SOV-121 - SOV-213 - SOV-401 - SOV-101`.
- `PT-601 - PSL-601` retained as a visible low-pressure signal/instrument relationship.

## Ambiguous cases
- `HV-103` is raw-visible on the TK-101 bottom/drain branch but was not in the component inventory; included as a high-recall node.
- `LI-301` is raw-visible at TK-301 but absent from the component-label inventory; included as a high-recall tank-level node.
- `H-CD-REL` text is partially obscured in crops, but the boxed chemical relief header is raw-visible and directly tied to the relief line; included with this normalized tag.
- Junction boxes/panels have sparse visible endpoint terminations in the crops; only conservative direct edges to `DCS-001`/`PLC-101` were added, while many passing dashed lines were not treated as endpoints.
- `C1`, `C2`, and numbered triangular continuation bubbles were not promoted to nodes because they are continuation/reference marks, not named logical components.
- Several long dashed process/relief/sample headers were represented as adjacent local paths, not as complete cliques.
