# Round 01 Diego Connectivity Notes

Extraction scope: doc34 Input resources and doc34 generated artifacts only. Ground-truth files, evaluator outputs, validation metrics, previous-doc score feedback, and outside resources were not opened or used.

## Node List Rationale

- Retained all 129 component labels from `component_visual_ocr_labels.csv` / `component_labels_list.csv`.
- Added 38 named visual endpoints/components needed to express connectivity without anonymous WN ids, unlabeled elbows/dots, or line-number-only labels.
- Added non-inventory labels are: DCS-001, YA-101, XS-101, XE-101, OPC-501, OPC-502, H-IA-101, H-N2-101, OPC-101, H-CCW-S, TIE-101, TIE-102, TIE-103, OPC-102, OPC-103, H-CCW-R, H-CLN-DIS, FLT-101B, HV-113B, H-HX-MRG, TIE-204, OPC-104, OPC-201, H-SW-S, TIE-301, H-SW-SPL, H-SW-MRG, OPC-202, OPC-401, TIE-401, H-CD-MIX, SP-101, AIT-401, H-DRN-101, H-VNT-101, H-SMP-101, H-WW-101, OPC-601.
- Wire-node ids from `wire_nodes.csv` were used only as visual aids and are not matrix nodes.
- `FLT-101B`, `HV-113B`, and `AIT-401` are visible items called out in the task risk areas, but are absent from the 129-row component CSV; they were added as visually supported non-inventory component exceptions.
- Named flanges and the visible non-inventory valve `SV-102` were not added as nodes; the routes are represented through adjacent inventory components and named H-/OPC-/TIE endpoints.

## Edge Evidence By Region

### Top control/data interfaces

`JB-401--JB-102`, `JB-102--JB-101`, `JB-101--PLC-101`, `PLC-101--CP-101`, `CP-101--DCS-001`, `CP-101--YI-101`, `DCS-001--YA-101`, `DCS-001--XE-101`, `XS-101--XE-101`, `MCC-101--HS-101A`, `MCC-101--HS-101B`, `MCC-101--HS-401A`, `MCC-101--HS-401B`, `MCC-101--P-501`.

### Left IA/N2 pressure utilities

`OPC-501--HV-501`, `HV-501--PRV-501`, `PRV-501--H-IA-101`, `OPC-502--HV-520`, `HV-520--PRV-520`, `PRV-520--H-N2-101`, `H-N2-101--PCV-501`, `H-N2-101--PT-501`, `PT-501--PIC-501`, `PIC-501--PAH-501`, `PIC-501--PCV-501`.

### Upper CCW supply header

`OPC-101--HV-101`, `HV-101--STR-101`, `STR-101--RED-101`, `RED-101--H-CCW-S`, `H-CCW-S--ZSO-101`, `ZSO-101--ZSC-101`, `ZSC-101--TIE-101`, `TIE-101--TIE-102`, `TIE-102--TIE-103`, `TIE-103--ZSO-102`, `ZSO-102--ZSC-102`, `ZSC-102--OPC-102`, `PI-101--PT-101`, `PT-101--TIE-102`.

### Cleanup pump/filter trains

`TIE-101--HV-110A`, `HV-110A--P-101A`, `P-101A--SV-101`, `SV-101--HV-112A`, `HV-112A--FLT-101A`, `FLT-101A--HV-113A`, `HV-113A--VV-101`, `VV-101--H-CLN-DIS`, `H-CLN-DIS--V-101`, `HS-101A--P-101A`, `TIE-101--HV-110B`, `HV-110B--P-101B`, `P-101B--CKV-111B`, `CKV-111B--HV-112B`, `HV-112B--FLT-101B`, `FLT-101B--HV-113B`, `HV-113B--LT-101`, `LT-101--TK-101`, `HS-101B--P-101B`, `PDT-101--HV-118`, `PDAH-101--PDT-101`, `PDT-101--FLT-101A`, `PDT-101--FLT-101B`, `FT-160--FIC-160`, `FIC-160--HV-119`, `HV-119--PSV-201`, `LIC-101--LT-101`, `LIC-101--HV-113B`.

### TK-101 / V-101 / HX-101 process area

`TK-101--LSHH-101`, `TK-101--LSLL-101`, `TK-101--LV-101`, `TK-101--DV-103`, `LT-101--LSHH-101`, `LIC-101--LSHH-101`, `LIC-101--LSLL-101`, `LIC-101--LV-101`, `DV-101--FLT-101B`, `DV-101--PT-201`, `PT-201--PIC-201`, `PT-201--DV-102`, `PIC-201--PCV-201`, `DV-102--PCV-201`, `PCV-201--LSLL-101`, `H-CCW-R--PCV-201`, `OPC-103--HV-201`, `HV-201--RED-201`, `RED-201--H-CCW-R`, `V-101--PSV-201`, `V-101--PI-301`, `V-101--FCV-101`, `FT-101--FIC-101`, `FIC-101--FCV-101`, `FT-101--V-101`, `PI-301--PSV-201`, `FCV-101--HV-130A`, `HV-130A--HX-101A`, `HX-101A--HV-131A`, `HV-131A--H-HX-MRG`, `FCV-101--HV-130B`, `HV-130B--HX-101B`, `HX-101B--HV-131B`, `HV-131B--H-HX-MRG`, `HX-101A--HX-101B`, `H-HX-MRG--TIE-204`, `TIE-204--MOV-201`, `MOV-201--OPC-104`, `SV-104--TIE-204`, `SV-104--SP-101`, `DV-103--H-DRN-101`.

### Service water, cooling, and return

`OPC-201--HV-210`, `HV-210--STR-201`, `STR-201--H-SW-S`, `H-SW-S--HS-201`, `HS-201--FT-201`, `FT-201--FIC-201`, `FT-201--TIE-301`, `HS-201--TIE-301`, `TIE-301--TCV-101`, `TCV-101--H-SW-SPL`, `TT-101--TIC-101`, `TT-101--TI-101`, `TIC-101--TCV-101`, `H-SW-S--PI-202`, `PI-202--VV-103`, `PI-202--DV-104`, `DV-104--H-DRN-101`, `H-SW-SPL--SV-103`, `SV-103--SP-101`, `H-SW-SPL--HV-220A`, `HV-220A--HV-221A`, `HV-221A--H-SW-MRG`, `H-SW-SPL--HV-220B`, `HV-220B--HV-221B`, `HV-221B--H-SW-MRG`, `TI-202--H-SW-MRG`, `H-SW-MRG--HV-222`, `HV-222--OPC-202`.

### Chemical dosing tanks and pumps

`OPC-401--VV-104`, `VV-104--HV-410`, `VV-104--TK-401`, `HV-410--TIE-401`, `TIE-401--HV-411`, `TIE-401--HV-401`, `TIE-401--HV-402`, `LT-401--TK-401`, `LT-401--TK-402`, `LT-401--LAH-401`, `LT-401--LIC-401`, `LT-401--LAL-401`, `LIC-401--HV-410`, `LIC-401--HV-411`, `TK-401--HV-401`, `HV-401--STR-401`, `STR-401--P-401A`, `HS-401A--P-401A`, `P-401A--CKV-401A`, `CKV-401A--FCV-401`, `FCV-401--ORF-401`, `ORF-401--H-CD-MIX`, `FT-401--FIC-401`, `FT-401--FI-401`, `FIC-401--FCV-401`, `FT-401--FCV-401`, `TK-401--DV-105`, `DV-105--TK-402`, `TK-402--HV-402`, `HV-402--STR-402`, `STR-402--P-401B`, `HS-401B--P-401B`, `P-401B--CKV-402B`, `CKV-402B--HV-403B`, `HV-403B--ORF-402`, `ORF-402--H-CD-MIX`, `TK-402--VV-105`, `VV-105--DV-106`, `DV-106--H-DRN-101`, `TK-402--RD-101`, `RD-101--H-VNT-101`, `H-CD-MIX--SV-105`, `SV-105--Q-401`, `H-CD-MIX--Q-401`, `SV-105--SP-101`, `AIT-401--AIC-401`, `AIT-401--SP-101`, `AIC-401--SP-101`.

### Sample / drain / vent / waste

`SP-101--H-SMP-101`, `H-SMP-101--SP-501`, `H-DRN-101--SP-501`, `H-VNT-101--LT-501`, `H-VNT-101--LIC-501`, `H-WW-101--SP-501`, `LT-501--SP-501`, `LT-501--LIC-501`, `LIC-501--P-501`, `SP-501--P-501`, `P-501--CKV-501`, `CKV-501--HV-501D`, `HV-501D--OPC-601`.

## Ambiguous / Plausible But Uncertain Candidates

- `SV-102` is visible on the center sample/drain route but is not in the 129-component inventory; it was not promoted to a matrix node.
- Named flange labels such as `FLG-101`, `FLG-111A`, and `FLG-111B` are visible, but were treated as inline fittings rather than matrix nodes.
- Several long dashed/dotted sample and vent lines cross process headers; edges were only added where a named endpoint/component adjacency was locally plausible.
- The N2 vertical route near the return/service-water area has filled crossings, but no named node at those crossings; no anonymous node or line-number-only node was added.

## High-Recall Edges For Jennifer To Scrutinize

- `MCC-101` links to the local hand-switch/pump controls rather than the top JB/PLC/CP horizontal chain.
- `H-CCW-S--ZSO-101--ZSC-101--TIE-101` treats the unlabeled actuated supply-header valve through its visible ZSO/ZSC instruments.
- `PDT-101` was linked to both filter housings because the differential-pressure dashed line spans the A/B filter detail.
- `H-CCW-R--PCV-201--LSLL-101--TK-101` captures the named return-header route without inserting anonymous intermediate junctions.
- `SP-101--H-SMP-101--SP-501` is a recall-oriented sample-header bridge; line style and long routing make this one worth reviewing.
- `H-CD-MIX`, `SV-105`, and `Q-401` are kept as a local high-recall mini-triangle due to close solid/dotted/slanted sample-line geometry.

## Basic Validation Summary

- Node count: 167
- Inventory components retained: 129 of 129
- Added non-inventory named endpoints/components: 38
- Unique undirected edges: 197
- Row/column labels: identical order by construction
- Values: 0/1 only by construction
- Symmetry: enforced by mirrored writes
- Diagonal: zero by construction
- Isolated nodes: none
- Validation errors: none
