# Round 01 Jennifer Connectivity Notes

Scope: doc34 Input resources and doc34 generated artifacts only. I did not open or use ground truth, evaluator output, validation metrics, previous-doc score feedback, or files outside the doc34 paths named in the task.

## Summary of Changes from Diego

- Node set retained: 167 nodes in Diego order.
- Inventory labels retained: all 129 component-inventory labels.
- Added/non-inventory named nodes retained from Diego: DCS-001, YA-101, XS-101, XE-101, OPC-501, OPC-502, H-IA-101, H-N2-101, OPC-101, H-CCW-S, TIE-101, TIE-102, TIE-103, OPC-102, OPC-103, H-CCW-R, H-CLN-DIS, FLT-101B, HV-113B, H-HX-MRG, TIE-204, OPC-104, OPC-201, H-SW-S, TIE-301, H-SW-SPL, H-SW-MRG, OPC-202, OPC-401, TIE-401, H-CD-MIX, SP-101, AIT-401, H-DRN-101, H-VNT-101, H-SMP-101, H-WW-101, OPC-601.
- Edge count changed from 197 to 181 unique undirected edges.
- Removed 21 Diego edges and added 5 local endpoint corrections.
- Main refinement pattern: actuator position instruments were not used as process-line bridges; controller-to-process shortcuts were removed unless a clear local termination was visible; the chemical sample/mix triangle was split into the visible local pairs.

## Accepted Final Node Policy

- Keep all visually supported labels from the 129-row component inventory.
- Keep named visual endpoints needed for connectivity: named OPC, H-, TIE, sample/drain/vent/waste endpoints, DCS/control endpoints, and visible non-inventory component exceptions FLT-101B, HV-113B, and AIT-401.
- Do not add WN ids, anonymous junctions, unlabeled elbows, continuation ticks, line-number-only labels, or line-description-only pseudo-headers.
- Do not promote additional non-inventory inline fittings/valves such as visible flange labels or SV-102/CKV-111A; they are represented by nearest named endpoints/components where needed.

## Added Local Corrections

| Node A | Node B | Evidence |
|---|---|---|
| `H-CCW-S` | `TIE-101` | Main CCW supply process path across the unlabeled actuated valve represented by nearest named endpoints. |
| `TIE-103` | `OPC-102` | Continuation from TIE-103 to the named off-page connector across the unlabeled actuated valve/fittings. |
| `HV-113A` | `H-CLN-DIS` | A-train filter discharge continues from HV-113A to the named clean-discharge endpoint. |
| `VV-101` | `TK-101` | VV-101 is visually tied to the TK-101 vent/tank branch. |
| `H-SW-S` | `TIE-301` | Service-water supply process path through an unlabeled actuated valve is represented by named endpoints. |

## Edge Evidence by Region

### Top control / data row
Accepted the visible box-to-box chain `JB-401--JB-102--JB-101--PLC-101--CP-101--DCS-001`, the CP drop to `YI-101`, and the DCS local signal endpoints `YA-101`, `XE-101`, and `XS-101--XE-101`. MCC was retained only to visible hand-switch drops `HS-101A`, `HS-101B`, `HS-401A`, and `HS-401B`; `MCC-101--P-501` was removed.

### IA / N2 / PCV-501
Accepted the solid IA chain `OPC-501--HV-501--PRV-501--H-IA-101` and N2 chain `OPC-502--HV-520--PRV-520--H-N2-101--PCV-501`. Accepted `PT-501--PIC-501--PAH-501` and `PIC-501--PCV-501`. Removed `PT-501--H-N2-101` because the direct tap to the N2 header is not locally resolved.

### Upper CCW supply and actuator positions
Accepted `OPC-101--HV-101--STR-101--RED-101--H-CCW-S--TIE-101--TIE-102--TIE-103--OPC-102`, with `PI-101--PT-101--TIE-102`. Kept actuator position pairs `ZSO-101--ZSC-101` and `ZSO-102--ZSC-102`, but did not use ZSO/ZSC instruments as process-line bridges.

### Cleanup pump / filter trains
Accepted A-train process adjacency `TIE-101--HV-110A--P-101A--SV-101--HV-112A--FLT-101A--HV-113A--H-CLN-DIS--V-101`, plus `VV-101--H-CLN-DIS` and `VV-101--TK-101` for the vent/tank branch. Accepted B-train adjacency `TIE-101--HV-110B--P-101B--CKV-111B--HV-112B--FLT-101B--HV-113B--LT-101--TK-101`. Kept visible local switch links `HS-101A--P-101A` and `HS-101B--P-101B`. Kept `PDT-101` to `PDAH-101`, `HV-118`, and both filters where the dashed DP detail spans the filter bodies.

### TK-101 / V-101 / HX-101
Accepted TK-101 local devices `LT-101`, `LSHH-101`, `LSLL-101`, `LV-101`, `DV-103`, and `VV-101`. Accepted `LT-101--LIC-101--LV-101`, but removed LIC/LT shortcuts to level switches and HV-113B. Accepted pressure/control detail `DV-101--PT-201--PIC-201--PCV-201`, `PT-201--DV-102--PCV-201`, and `H-CCW-R--PCV-201--LSLL-101`. Accepted V-101 local connections to `PSV-201`, `PI-301`, `FT-101`, `FCV-101`, and `H-CLN-DIS`, while removing `PSV-201--PI-301`. Accepted the HX branches `FCV-101--HV-130A--HX-101A--HV-131A--H-HX-MRG` and `FCV-101--HV-130B--HX-101B--HV-131B--H-HX-MRG`, plus `H-HX-MRG--TIE-204--MOV-201--OPC-104` and `SV-104--TIE-204--SP-101`.

### Service water / return
Accepted the left supply path `OPC-201--HV-210--STR-201--H-SW-S--TIE-301--TCV-101--H-SW-SPL`. Kept `FT-201--FIC-201`, `FT-201--TIE-301`, and `FT-201--HS-201` where the local linework is clear, but removed `H-SW-S--HS-201` and `HS-201--TIE-301` as process bridges. Accepted `TT-101--TIC-101--TCV-101` and `TT-101--TI-101`. Accepted `PI-202` to `H-SW-S`, `VV-103`, and `DV-104`, with `DV-104--H-DRN-101`. Accepted split/merge paths through `H-SW-SPL`, `HV-220A/B`, `HV-221A/B`, `H-SW-MRG`, `TI-202`, `HV-222`, and `OPC-202`.

### Chemical dosing
Accepted `OPC-401--VV-104--HV-410--TIE-401`, `VV-104--TK-401`, and `TIE-401` branches to `HV-411`, `HV-401`, and `HV-402`. Accepted level/alarm loop `LAH-401--LT-401--LIC-401` and `LT-401--LAL-401`; removed LT/LIC shortcuts to TK-402 and HV-410/HV-411. Accepted A-train `TK-401--HV-401--STR-401--P-401A--CKV-401A--FCV-401--ORF-401--H-CD-MIX` and B-train `TK-402--HV-402--STR-402--P-401B--CKV-402B--HV-403B--ORF-402--H-CD-MIX`, plus local pump switches. Accepted `FT-401--FIC-401--FCV-401`, `FT-401--FI-401`, and `FT-401--FCV-401`. Accepted `H-CD-MIX--SV-105`, `H-CD-MIX--Q-401`, and `SV-105--SP-101`; removed `SV-105--Q-401`. Accepted `AIC-401--AIT-401--SP-101`; removed direct `AIC-401--SP-101`.

### Sample / drain / vent / waste
Accepted named headers/endpoints `H-DRN-101`, `H-VNT-101`, `H-SMP-101`, `H-WW-101`, and `OPC-601` because they are visibly named and needed. Accepted tank/service drain routes to `H-DRN-101`, `H-DRN-101--SP-501`, `H-WW-101--SP-501`, `SP-501--P-501--CKV-501--HV-501D--OPC-601`, `LT-501--SP-501`, `LT-501--LIC-501`, `LIC-501--P-501`, and `H-VNT-101--LT-501`. Accepted `SP-101--H-SMP-101`; removed `H-SMP-101--SP-501` because that bridge was not locally clear.

## Removed / Rejected Diego Candidates

| Node A | Node B | Reason |
|---|---|---|
| `MCC-101` | `P-501` | No visible direct MCC drop to P-501; P-501 is locally tied to LIC-501/SP-501. |
| `PT-501` | `H-N2-101` | PT-501 signal line to PIC-501 is clear, but a direct N2 process tap is not visually terminated. |
| `H-CCW-S` | `ZSO-101` | ZSO-101 is an actuator position instrument, not a process-line bridge from the header endpoint. |
| `ZSC-101` | `TIE-101` | ZSC-101 is paired with ZSO-101 on the actuator signal line; it is not the named process endpoint. |
| `TIE-103` | `ZSO-102` | ZSO-102 is an actuator position instrument, not the process path from TIE-103. |
| `ZSC-102` | `OPC-102` | ZSC-102 is paired with ZSO-102 on the actuator signal line; process path is handled by TIE-103--OPC-102. |
| `PSV-201` | `PI-301` | Both are local to V-101 but no direct line between the PSV and PI is visible. |
| `LT-101` | `LSHH-101` | Both are tank level devices; direct LT-to-LSHH linkage is not visually supported. |
| `LIC-101` | `LSHH-101` | Controller-to-level-switch shortcut; LSHH-101 is locally associated with TK-101. |
| `LIC-101` | `LSLL-101` | Controller-to-level-switch shortcut; LSLL-101 is locally associated with TK-101/PCV-201 route. |
| `LIC-101` | `HV-113B` | Controller-to-hand-valve/process shortcut; direct termination is not clear. |
| `HV-113A` | `VV-101` | VV-101 is on a vent/tank branch, not the inline discharge continuation from HV-113A. |
| `H-SW-S` | `HS-201` | HS-201 is an actuator/hand-switch association, not the service-water process endpoint. |
| `HS-201` | `TIE-301` | HS-201 is not used as the process bridge to TIE-301. |
| `LT-401` | `TK-402` | LT-401 is visibly local to TK-401; extension to TK-402 is an unsupported association. |
| `LIC-401` | `HV-410` | LIC-401-to-HV-410 control/association shortcut is not a clear local termination. |
| `LIC-401` | `HV-411` | LIC-401-to-HV-411 control/association shortcut is not a clear local termination. |
| `SV-105` | `Q-401` | H-CD-MIX has separate local routes to SV-105 and Q-401; SV-105--Q-401 closes an unsupported triangle. |
| `AIC-401` | `SP-101` | AIC-401 connects through AIT-401; direct AIC-to-sample-box shortcut removed. |
| `H-VNT-101` | `LIC-501` | Vent line adjacency is represented through LT-501--LIC-501; direct H-VNT-to-LIC skips LT-501. |
| `H-SMP-101` | `SP-501` | Plausible sample/waste bridge, but no clear local termination into SP-501 was visible. |

## Uncertain / Plausible but Not Accepted

| Candidate | Why Not Accepted |
|---|---|
| `PT-501--H-N2-101` | PT/PIC signal loop is clear, but no clean local process tap from PT-501 to the N2 header is visible. |
| `H-IA-101--H-N2-101` | A vertical dashed line passes near both named points, but it is not a process connection between IA and N2 headers. |
| `MCC-101--P-501` | P-501 is plausibly motor-controlled, but the visible local linework ties it to LIC-501/SP-501 rather than the MCC trunk. |
| ZSO/ZSC process bridging to CCW endpoints | Position instruments are visibly tied to actuator symbols; without a named valve node, the process path is represented by nearest named process endpoints. |
| `PDT-101--HV-119` | The long dashed route is visually plausible but not a clear local PDT termination; retained only the clearer PDT-to-HV-118/filter/PDAH links. |
| `LIC-101--LSHH-101`, `LIC-101--LSLL-101` | Plausible loop association, but direct controller-to-switch terminations are not clear. |
| `LIC-401--HV-410`, `LIC-401--HV-411` | Dashed control/association linework is near these valves, but no unambiguous direct termination is visible. |
| `SV-105--Q-401` | Nearby geometry could suggest a triangle, but the visible local pairs are H-CD-MIX to SV-105 and H-CD-MIX to Q-401. |
| `H-SMP-101--SP-501` | Long sample/waste routing is plausible but not locally terminated into SP-501. |
| `H-VNT-101--LIC-501` | The vent line reaches the LT/LIC area, but direct adjacency skips `LT-501`; represented through `H-VNT-101--LT-501--LIC-501`. |

## Basic Validation Summary

- Node count: 167
- Unique undirected edges: 181
- Row labels equal column labels in the same order: True
- Symmetric matrix: True
- Values are 0/1 only: True
- Diagonal zero: True
- Isolated nodes: 0 (none)
- Output CSV: `C:\Asif_all_python_projects\INL\Improved -- blind iterations\34\Results\Iteration_1\round_01_jennifer_matrix.csv`
