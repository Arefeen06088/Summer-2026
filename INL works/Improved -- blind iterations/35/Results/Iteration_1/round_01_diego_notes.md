# Round 01 Diego High-Recall Connectivity Notes

## Scope And Inputs

Used only doc35 Input resources and generated doc35 artifacts: the raw schematic image, component inventory CSV/list, component/wire overlays, wire-node aid overlay, resource summaries, and inspection crops. No ground truth, evaluator output, validation metrics, previous-doc feedback, or outside resources were used.

## Node List Rationale

All 144 visually supported inventory component labels from `component_visual_ocr_labels.csv` are retained exactly as normalized in the inventory. I added only visible named endpoints, headers, tie points, sample/control endpoints, and a few visible named non-inventory components where they prevent replacing a named schematic object with an anonymous WN/junction.

Added non-inventory nodes:

- `OPC-IA-2101`: visible named non-inventory endpoint/component/tie point used to avoid anonymous WN/junction nodes.
- `IA-H-2101`: visible named non-inventory endpoint/component/tie point used to avoid anonymous WN/junction nodes.
- `VNT-2101`: visible named non-inventory endpoint/component/tie point used to avoid anonymous WN/junction nodes.
- `VNT-2140`: visible named non-inventory endpoint/component/tie point used to avoid anonymous WN/junction nodes.
- `OPC-SW-2101`: visible named non-inventory endpoint/component/tie point used to avoid anonymous WN/junction nodes.
- `H-SW-2101`: visible named non-inventory endpoint/component/tie point used to avoid anonymous WN/junction nodes.
- `OPC-SW-2102`: visible named non-inventory endpoint/component/tie point used to avoid anonymous WN/junction nodes.
- `OPC-DMW-2101`: visible named non-inventory endpoint/component/tie point used to avoid anonymous WN/junction nodes.
- `OPC-2101`: visible named non-inventory endpoint/component/tie point used to avoid anonymous WN/junction nodes.
- `H-2101`: visible named non-inventory endpoint/component/tie point used to avoid anonymous WN/junction nodes.
- `SB-2101`: visible named non-inventory endpoint/component/tie point used to avoid anonymous WN/junction nodes.
- `STR-2101`: visible named non-inventory endpoint/component/tie point used to avoid anonymous WN/junction nodes.
- `T-2101`: visible named non-inventory endpoint/component/tie point used to avoid anonymous WN/junction nodes.
- `T-2102`: visible named non-inventory endpoint/component/tie point used to avoid anonymous WN/junction nodes.
- `T-2103`: visible named non-inventory endpoint/component/tie point used to avoid anonymous WN/junction nodes.
- `H-2102`: visible named non-inventory endpoint/component/tie point used to avoid anonymous WN/junction nodes.
- `T-2115`: visible named non-inventory endpoint/component/tie point used to avoid anonymous WN/junction nodes.
- `T-2120`: visible named non-inventory endpoint/component/tie point used to avoid anonymous WN/junction nodes.
- `T-2122A`: visible named non-inventory endpoint/component/tie point used to avoid anonymous WN/junction nodes.
- `T-2122B`: visible named non-inventory endpoint/component/tie point used to avoid anonymous WN/junction nodes.
- `T-2125`: visible named non-inventory endpoint/component/tie point used to avoid anonymous WN/junction nodes.
- `T-2130`: visible named non-inventory endpoint/component/tie point used to avoid anonymous WN/junction nodes.
- `T-2131`: visible named non-inventory endpoint/component/tie point used to avoid anonymous WN/junction nodes.
- `T-2132`: visible named non-inventory endpoint/component/tie point used to avoid anonymous WN/junction nodes.
- `OPC-2102`: visible named non-inventory endpoint/component/tie point used to avoid anonymous WN/junction nodes.
- `OPC-CHEM-2101`: visible named non-inventory endpoint/component/tie point used to avoid anonymous WN/junction nodes.
- `T-2110`: visible named non-inventory endpoint/component/tie point used to avoid anonymous WN/junction nodes.
- `T-2140`: visible named non-inventory endpoint/component/tie point used to avoid anonymous WN/junction nodes.
- `INJ-2140`: visible named non-inventory endpoint/component/tie point used to avoid anonymous WN/junction nodes.
- `SAP-2101`: visible named non-inventory endpoint/component/tie point used to avoid anonymous WN/junction nodes.
- `AN-2101`: visible named non-inventory endpoint/component/tie point used to avoid anonymous WN/junction nodes.
- `AIC-2101`: visible named non-inventory endpoint/component/tie point used to avoid anonymous WN/junction nodes.
- `OPC-DRN-2101`: visible named non-inventory endpoint/component/tie point used to avoid anonymous WN/junction nodes.
- `OPC-DATA-2101`: visible named non-inventory endpoint/component/tie point used to avoid anonymous WN/junction nodes.
- `HV-SW-DRAIN`: visible named non-inventory endpoint/component/tie point used to avoid anonymous WN/junction nodes.

I intentionally excluded WN ids, unlabeled dots, elbows, continuation ticks, and line-number-only labels such as pipe spec tags. Long headers are represented by adjacent named pairs through explicit `H-*`, `OPC-*`, and `T-*` nodes where visible.

## Edge Evidence By Region

- **Left makeup, IA, service water, and TK-210** (51 edges): OPC-IA-2101-HV-IA-2101, HV-IA-2101-PCV-IA-2101, PCV-IA-2101-IA-H-2101, IA-H-2101-PI-IA-2101, VNT-2101-HV-2103, HV-2103-TK-210, PSV-2102-VNT-2140, OPC-SW-2101-H-SW-2101, H-SW-2101-HV-SW-2101, HV-SW-2101-STR-SW-2101, STR-SW-2101-FT-SW-2101, FT-SW-2101-FCV-SW-2101, FT-SW-2101-FIC-SW-2101, FIC-SW-2101-FCV-SW-2101, PT-SW-2101-STR-SW-2101, HS-2101-FIC-SW-2101, FCV-SW-2101-HV-SW-2102, HV-SW-2102-CV-SW-2101, CV-SW-2101-OPC-SW-2102, TT-SW-2101-TIC-2130, TIC-2130-HV-SW-2102, OPC-DMW-2101-HV-2150, HV-2150-FT-2150, FT-2150-FCV-2150, FCV-2150-LV-2101, LV-2101-TK-210, FIC-2150-FT-2150, FIC-2150-FCV-2150, LIC-2101-LT-2101, LIC-2101-LV-2101, LT-2101-TK-210, LI-2101-TK-210, LSHH-2101-LAHH-2101, LSHH-2101-TK-210, LAHH-2101-TK-210, LSL-2102-LALL-2102, LSL-2102-TK-210, LALL-2102-TK-210, TK-210-HV-2104, HV-2104-DRN-2101, TK-210-HV-1102, HV-1102-T-2101, OPC-2101-H-2101, H-2101-HV-2101, HV-2101-SB-2101, SB-2101-STR-2101, STR-2101-T-2101, PDI-2101-STR-2101, PI-2101-T-2101, PT-2101-T-2101, PI-2101-PT-2101.
- **A/B cleanup trains and pump discharge header** (38 edges): T-2101-HV-2110A, HV-2110A-STR-2110A, STR-2110A-P-2101A, P-2101A-CV-2110A, CV-2110A-HV-2111A, HV-2111A-MOV-2112A, MOV-2112A-T-2102, T-2102-H-2102, T-2101-HV-2110B, HV-2110B-STR-2110B, STR-2110B-P-2101B, P-2101B-CV-2110B, CV-2110B-HV-2111B, HV-2111B-MOV-2112B, MOV-2112B-T-2103, T-2103-H-2102, H-2102-T-2115, T-2115-FT-2110, FT-2110-HV-2113, HV-2113-T-2120, TS-2110A-PT-2110A, PT-2110A-PI-2110A, PT-2110A-P-2101A, PI-2110A-P-2101A, TS-2110A-P-2101A, TS-2110B-PT-2110B, PT-2110B-PI-2110B, PT-2110B-P-2101B, PI-2110B-P-2101B, TS-2110B-P-2101B, HS-2101-MOV-2112A, HS-2102-MOV-2112B, FIC-2110-FT-2110, FIC-2110-SV-2110, FIC-2110-FAH-2110, FAH-2110-FT-2110, SV-2110-PSV-2110, PSV-2110-T-2130.
- **Filters, HX, bypass, and service-water return** (46 edges): T-2120-T-2130, T-2130-HV-2130, HV-2130-FCV-2130, FCV-2130-HV-2131, HV-2131-T-2132, T-2132-T-2131, T-2130-HV-2120A, HV-2120A-FLT-2120A, FLT-2120A-HV-2121A, HV-2121A-T-2122A, T-2122A-T-2125, T-2120-HV-2120B, HV-2120B-FLT-2120B, FLT-2120B-HV-2121B, HV-2121B-T-2122B, T-2122B-T-2125, T-2125-HV-2125, HV-2125-HX-2120, HX-2120-T-2131, T-2131-MOV-2125, MOV-2125-FCV-2125, FCV-2125-R-2125, R-2125-OPC-2102, T-2131-HV-SW-DRAIN, HV-SW-DRAIN-DRN-SW-2101, PI-2120A-T-2130, DPIT-2120A-FLT-2120A, DPIT-2120A-DPAH-2120, PI-2120B-FLT-2120B, DPIT-2120B-FLT-2120B, DPIT-2120B-DPAH-2120, FT-2130-FIC-2130, FT-2130-FCV-2130, FIC-2130-FCV-2130, SV-2130-FIC-2130, SV-2130-FCV-2130, PIC-2101-FCV-2130, PI-2125-T-2125, TT-2120I-HX-2120, TT-2120I-TT-2120O, TT-2120O-TAH-2120, TT-2120O-HX-2120, TI-2120-HX-2120, TAL-2120-TI-2120, TAL-2120-FCV-2125, SV-2125-FCV-2125.
- **Chemical tank and chemical injection pumps** (45 edges): OPC-CHEM-2101-HV-2140, HV-2140-FLT-2140, FLT-2140-TK-2110, TK-2110-LT-2110, TK-2110-LSH-2110, TK-2110-HV-2141, HV-2141-T-2110, TK-2110-HV-2147, HV-2147-T-2110, VNT-2140-HV-2146, HV-2146-TK-2110, TK-2110-HV-2145, HV-2145-DRN-2140, DRN-2140-H-DRN-2101, T-2110-P-2110A, P-2110A-CV-2140A, CV-2140A-HV-2142A, HV-2142A-T-2140, T-2110-P-2110B, P-2110B-CV-2140B, CV-2140B-HV-2142B, HV-2142B-T-2140, T-2140-PI-2140, PI-2140-PCV-2132, PCV-2132-FCV-2114, FCV-2114-HV-2114, HV-2114-T-2103, FIC-2140-FI-2140, FIC-2140-PCV-2132, FIC-2140-FCV-2114, PSV-2140-T-2140, FI-2140-PI-2140, HS-2102-FIC-2140, HS-2102-P-2110A, HS-2102-P-2110B, AIT-2140-AI-2140, AIT-2140-FCV-2114, T-2140-HV-2143, HV-2143-XV-2144, XV-2144-INJ-2140, XV-2144-FCV-2114, XV-2144-SV-2144, SV-2144-HV-DRN-2107, HV-2142B-R-2114, R-2114-XV-2144.
- **Sample panels, drains, and control/data bay** (35 edges): T-2125-HV-SAM-2101, HV-SAM-2101-SP-2101, SP-2101-SAP-2101, T-2122B-HV-SAM-2102, HV-SAM-2102-SP-2102, SP-2102-SAP-2101, T-2131-HV-SAM-2103, HV-SAM-2103-SP-2103, SP-2103-SAP-2101, SAP-2101-AN-2101, AN-2101-AIC-2101, DRN-2101-HV-DRN-2102, HV-DRN-2102-HV-DRN-2103, HV-DRN-2103-CP-CHEM-2101, CP-CHEM-2101-SV-2144, SV-2144-HV-DRN-2107, HV-DRN-2107-H-DRN-2101, H-DRN-2101-HV-DRN-2104, HV-DRN-2104-HV-DRN-2105, HV-DRN-2105-DRN-SW-2101, DRN-SW-2101-OPC-DRN-2101, DRN-2101-H-DRN-2101, XA-2140-CP-CHEM-2101, XA-2140-JB-2101, CP-CHEM-2101-JB-2101, JB-2101-JB-2102, JB-2102-JBX-2103, JBX-2103-PLC-2101, PLC-2101-DCS-2101, DCS-2101-OPC-DATA-2101, JB-2102-XA-2110, HS-2110-XA-2110, XA-2110-KQI-2101, KQI-2101-KQI-2102, KQI-2102-PLC-2101.

## Ambiguous / Plausible But Uncertain Candidates

- `PSV-2102` - `VNT-2140`: relief/vent routing is visible but crosses dense IA/SW/tank area.
- `PSV-2110` - `T-2130`: safety valve is near the filter/bypass inlet header; exact tap point is small.
- `VNT-2140` - `HV-2146`: long vertical line appears continuous but spans a large sheet region.
- `HV-2146` - `TK-2110`: probable vent/top connection into lower chemical tank; visually distant.
- `HV-SW-DRAIN` - `DRN-SW-2101`: named drain valve is not in inventory and the long drain run is partially outside crop.
- `HV-2114` - `T-2103`: chemical/process tie-in uses a dense vertical riser near B-train discharge.
- `T-2122B` - `HV-SAM-2102`: sample takeoff routing is visually plausible but partly dashed/overlapping.
- `T-2131` - `HV-SAM-2103`: sample takeoff routing is visually plausible but partly routed through the HX outlet area.
- `XA-2140` - `JB-2101`: control/data line continues into the bay but exact landing point is sparse.
- `KQI-2102` - `PLC-2101`: bottom interlock/control bundle is represented as a local chain, not a bay clique.

## High-Recall Edges Jennifer Should Scrutinize

- Vent/relief links around `PSV-2102`, `VNT-2140`, and `HV-2146` because the vertical routing spans multiple crop regions.
- Header/tie modeling around `T-2130`, `T-2120`, `T-2122A/B`, `T-2125`, `T-2131`, and `T-2132`; I represented local adjacent pairs only, not header cliques.
- Chemical injection riser edges `HV-2114`-`T-2103`, `FCV-2114`-`HV-2114`, and `XV-2144`-`FCV-2114` because the lower-middle riser is visually dense.
- Sample panel takeoffs `T-2125`/`T-2122B`/`T-2131` to `HV-SAM-*`; these are visually plausible dashed/sample routes but should be checked against the raw crop.
- Bottom control bay chain `JB-2101`-`JB-2102`-`JBX-2103`-`PLC-2101`-`DCS-2101` and `HS-2110`/`XA-2110`/`KQI-*`; intentionally sparse but uncertain at exact landing points.

## Basic Validation Summary

- Matrix path: `C:\Asif_all_python_projects\INL\Improved -- blind iterations\35\Results\Iteration_1\round_01_diego_matrix.csv`
- Nodes: 179 total = 144 inventory + 35 added named non-inventory nodes.
- Unique undirected accepted edges: 214.
- Row count equals column count: True.
- Row/column label order identical by construction: True.
- Symmetric: True.
- Values restricted to 0/1: True.
- Diagonal zero: True.
- Isolated accepted nodes: 0 (minimum degree 1, maximum degree 10).
