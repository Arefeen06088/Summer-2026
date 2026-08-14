# Doc 30 / Iteration 1 Diego Connectivity Notes

## Source Boundaries

Used only doc 30 input resources and doc 30 generated inspection crops/artifacts. The raw schematic `raw -- left_side_readable_base_v2_synthetic_pid_aux_ccw.png` was treated as primary evidence; OCR/component overlays and wire-node overlays were used only as aids for labels, crops, and intersection checks. No ground truth, evaluator output, score feedback, or other document/iteration resources were used.

## Node List Rationale

- Retained all 150 supplied physical inventory components from `component_labels_list.csv`.
- Added raw-visible physical node `FLG-101`, which is called out in the prompt/raw inlet chain but is not present in the 150-component inventory CSV.
- Added raw-visible off-page connectors: `OPC-101` through `OPC-109` where visibly connected.
- Added raw-visible named headers: `VH-100`, `RH-100`, `IAH-100`, `H-101` through `H-107`, `SH-100`, and `DH-100`.
- Added `CAP-101` as a high-recall logical spare/cap node on the raw-visible `OPC-109` spare branch. This is the most review-sensitive added node because it appears as a named cap annotation rather than a boxed component.
- Excluded anonymous wire nodes (`WN-*`), branch dots (`BR-*`), unlabeled elbows/crossings, t-sections, continuation dots, and line-number-only labels such as `4IN-CCW-*`, `2IN-*`, and `0.75IN-*`.

## Inventory Labels Omitted Or Corrected

No inventory labels were omitted or renamed. All inventory component labels are present as matrix nodes. `FLG-101`, `OPC-109`, and `CAP-101` were added beyond the inventory because they are raw-visible and connected.

## Edge Evidence By Region

### Top Controls / Panels

- Included direct visible control endpoints: `CP-101`--`PLC-101`, `JB-101`--`JB-102`, `JB-101`--`DCS-001`, `JB-102`--`DCS-001`, plus direct instrument/panel signal candidates `FIC-120`--`DCS-001`, `PIC-101`--`JB-101`, and `TIC-101`--`JB-101`.
- Local instrument loops retained where dashed lines terminate on named objects: `PT-101`--`PIC-101`, `TT-101`--`TIC-101`, `FE-120`--`FT-120`, `FT-120`--`FIC-120`, `FIC-120`--`FCV-171`, and `TIC-101`--`FCV-171`.

### Top Left Inlet, TK-101, V-101

- Inlet chain: `OPC-101`--`HV-101`--`FLG-101`--`MOV-102`--`SB-101`--`STR-101`--`HV-103`--`RED-101`--`H-101`.
- Makeup: `OPC-102`--`HV-104`--`LV-105`--`TK-101`, with `LV-105`--`LIC-101` as a direct dashed control candidate.
- Tank relief/vent: `TK-101`--`VV-107`--`VH-100` and `TK-101`--`PSV-108`--`RH-100`; included dashed high-level candidates involving `LSHH-101`.
- Level loop: `TK-101` to `LT-101`, `LSHH-101`, `LSLL-101`, plus `LT-101`--`LIC-101`, `LSLL-101`--`LIC-101`, and `LSLL-101`--`LT-101`.
- Air separator: `TK-101`--`HV-106`--`V-101`, `V-101`--`HV-110`--`H-101`, `V-101`--`VV-111`--`VH-100`, and drains `DV-109`/`DV-112` to `DH-100`.

### P-101 Trains / Bypass

- Pump A/B chains from `H-101` through `HV-111A/B`, `P-101A/B`, `CV-112A/B`, `HV-113A/B` into `H-102`.
- Bypass/return-like line retained as adjacent path: `H-101`--`HV-114`--`MOV-115`--`H-102`--`HV-122`--`BV-123`--`H-103`.

### HX-101 And Service Water

- CCW process side: `H-102`--`MOV-120`--`FE-120`--`HX-101`--`HV-121`--`SB-102`--`H-103`.
- Service water side: `OPC-104`--`HV-170`--`STR-170`--`FCV-171`--`HX-101`--`HV-172`--`OPC-105`.
- `FCV-171`--`IAH-100` retained as a pneumatic/instrument-air candidate visible at the valve actuator/header area.

### Filters / Right Return

- Filter trains: `H-103`--`HV-131A/B`--`FLT-101A/B`--`HV-132A/B`--`H-104`.
- Differential pressure/alarm loop retained as `FLT-101A`--`PDT-101`, `FLT-101B`--`PDT-101`, and `PDT-101`--`PDAH-101`.
- Outlet path: `H-104`--`RED-102`--`FCV-140`--`MOV-141`--`H-105`.
- Spare branch: `MOV-141`--`CAP-101`--`OPC-109`.
- Added high-recall direct header adjacency `H-103`--`H-105` because the raw and wire-node overlay show a plausible downcomer/intersection at the H-105 supply line.

### Branch Matrix 201-208

- Each branch uses the same local chain from `H-105` to `H-106`: `H-105`--`HV-20x1`--`FE-20x`--equipment--`CV-20x1`--`HV-20x2`--`H-106`.
- Equipment mapping: 201 `HX-201`, 202 `HX-202`, 203 `CLR-203`, 204 `V-204`, 205 `HX-205`, 206 `HX-206`, 207 `CLR-207`, 208 `V-208`.
- Flow and temperature instruments retained as direct local dashed ties: `FI-20x`--`FE-20x` and `TI-20x`--corresponding equipment.
- `H-106`--`OPC-108` retained at the right return off-page connector.

### Chemical Injection / Dosing

- Chemical tanks/pumps: `TK-201`--`HV-201`--`P-201A`; `P-201A` connects through the visible discharge/check-valve area to `HV-152`, `CV-202`, `HV-203`, `FCV-301`, and `MX-201`.
- Lower dosing/neutralization: `TK-202`--`HV-204`--`P-201B`--`CV-205`--`HV-206`--`MX-201`, plus `TK-202`--`RO-208`--`MX-201`.
- Mixer/control injection: `MX-201`--`FCV-301`--`HV-302`--`IQ-201`--`H-107`--`HX-201`; `PT-201`--`H-107` retained as the chemical-header pressure signal candidate.
- Flow control loop: `FT-301`--`FIC-301`, `FIC-301`--`FCV-301`, and `FT-301`--`FCV-301`.

### Bottom Sample / Drain / Sump

- Unlabeled row-G run represented as adjacent path: `FCV-301`--`SV-201`--`DV-201`--`SV-203`--`DV-203`--`PCV-151`--`HV-150`--`H-106`.
- Named header drops: `SV-201`/`SV-203` to `SH-100`, and `DV-201`/`DV-203` to `DH-100`.
- Added high-recall local branch taps from `H-106` to `SV-201`, `DV-201`, `SV-203`, and `DV-203` where vertical branch drops are visible.
- Drain pit/pump: `V-401`--`P-401`--`CV-402`--`HV-401`--`SH-100`; `V-401`--`DH-100`--`HV-403`--`OPC-107`.

## Ambiguous High-Recall Candidates For Precision Review

| Candidate | Why included | Review risk |
|---|---|---|
| `CAP-101` node and `MOV-141`--`CAP-101`--`OPC-109` | Raw-visible named spare/cap annotation on the off-page spare branch | May be treated as a branch tag/annotation instead of a true node |
| `H-103`--`H-105` | Raw and wire-node overlay show a plausible downcomer/intersection to the clean CCW supply header | Could be an orthogonal crossing or background continuation rather than process connection |
| `VV-111`--`H-101` | V-101 upper branch visually ties into the nearby suction header/vent geometry | Could instead be only the V-101 vent path to `VH-100` |
| `FCV-171`--`IAH-100` | Control valve actuator area appears tied to instrument-air header | Pneumatic supply may be schematic context rather than direct connectivity |
| Panel/JB edges involving `FIC-120`, `PIC-101`, `TIC-101`, `JB-101`, `JB-102`, `DCS-001` | Dashed trunks visibly terminate in this region | Control trunks are bundled; exact endpoint ownership is not fully resolved |
| Bottom row-G chain through `SV-201`, `DV-201`, `SV-203`, `DV-203`, `PCV-151`, `HV-150` | Solid unlabeled horizontal run connects these local valves | Header is unlabeled; adjacent chain is a modeling choice to avoid anonymous nodes |
| `H-106` taps to `SV-201`/`DV-201`/`SV-203`/`DV-203` | Vertical branch drops from return area are visible | Some may represent branch-specific sample/drain lines rather than direct header adjacency |
| `PT-201`--`H-107` | Dashed local pressure line is visibly associated with the chemical injection header | Exact endpoint could be the HV-302/IQ-201 riser rather than the named header |
| `LSHH-101` links to `VV-107`/`PSV-108` | Dashed high-level line is visible in the relief/vent area | Could be alarm/annotation rather than direct control connectivity |

## Final Validation Counts

- Nodes: 173
- Inventory component nodes retained: 150
- Extra raw-visible physical nodes: 1
- Added logical/header/off-page nodes: 22
- Undirected edges: 211
- Matrix symmetric: True
- Diagonal zero: True
- Duplicate edges collapsed before writing: 0
- Matrix values valid: True
- Row/column labels identical: True
- Isolated nodes: none
