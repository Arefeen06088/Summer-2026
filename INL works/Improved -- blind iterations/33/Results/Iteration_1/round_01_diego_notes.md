# Round 01 Diego Connectivity Notes

Scope: derived only from the doc33 raw schematic and local doc33 aids/crops listed in the prompt. The raw schematic was treated as authoritative; overlays were used only as visual aids for labels, wire nodes, and filled-dot junctions.

## Node list rationale

- Matrix node count: 193.
- Inventory components were included when they participate in a visible process, pneumatic, electrical, or instrument/control connection.
- Added named non-inventory/logical endpoints because they are visible real endpoints: named headers/manifolds, off-page connectors, control/data buses, DCS/control-room boxes, HS boxes, and a few visible named instruments/valves/equipment omitted from the CSV inventory.
- Added non-inventory nodes: OPC-CCW-R01, 6" CCW RETURN HEADER, 6" PUMP SUCTION HEADER, RECIRC TO SURGE TANK, 6" PUMP DISCHARGE HEADER, 4" FILTER INLET MANIFOLD, 4" FILTER OUTLET MANIFOLD, 4" HX INLET MANIFOLD, 4" HX OUTLET MANIFOLD, 6" CCW SUPPLY HEADER, OPC-CCW-S01, OPC-SW-IN, 8" SERVICE WATER SUPPLY HEADER, 8" SERVICE WATER RETURN HEADER, OPC-SW-OUT, 1/2" CHEMICAL DOSING HEADER, SAMPLE / ANALYZER PANEL, 3" FLOOR DRAIN / RADWASTE RETURN HEADER, OPC-IA-IN, 1" IA HEADER - 80 PSIG, DCS / PLC DATA BUS, CONTROL ROOM LINK, DCS-001, HS-13A, HS-13B, PT-202, PY-202, PDT-201, QI-301, XV-22A, XV-22B, HV-31A, HV-32A, HV-31B, HV-32B, PD-301A, PD-301B, SV-301A, SV-301B, AIT-301, AIC-301, CAL-301, FV-301, AFR-230.
- I did not add anonymous WN ids, unnamed elbows/bends, unlabeled T-sections, continuation marks, or line-number-only labels.

## Edge evidence by region

### Left surge/makeup
- `OPC-CCW-R01 -> HV-101 -> FE-101 -> 6" CCW RETURN HEADER`; `FE-101 -> FT-101 -> FI-101`; `TT-101 -> TY-101`.
- Surge/makeup connections represented as `6" CCW RETURN HEADER -> MOV-102 -> HV-103 -> TK-101`, `TK-101 -> PSV-101 -> HV-105`, `TK-101 -> SV-101 -> TK-102`, `TK-101 -> HV-104 -> TK-102`, and `TK-102 -> LV-105`.
- Level/control links: `LT-101 -> LIC-101 -> LV-105`, `LIC-101 -> SV-101`, plus LSHH/LSL/LIC routes to `JB-101`.
- Suction path: `TK-101 -> DV-101 -> HV-106 -> HV-107 -> 6" PUMP SUCTION HEADER` and `TK-102 -> DV-102 -> HV-107`; recirc path includes `RECIRC TO SURGE TANK -> HV-405 -> MOV-404`.

### Pump trains
- Train A: `6" PUMP SUCTION HEADER -> HV-12A -> STR-12A -> P-12A -> CV-12A -> HV-13A -> MOV-13A -> 6" PUMP DISCHARGE HEADER`, with `STR-12A -> VV-12A`, `P-12A -> DV-12A`, and `P-12A -> PY-12A`.
- Train B mirrors A with `HV-12B/STR-12B/P-12B/CV-12B/HV-13B/MOV-13B`, plus `VV-12B`, `DV-12B`, and `PY-12B`.
- Control chains: `PT-13A -> HS-13A -> JB-12A`, `HS-13A -> MOV-13A`; and `PT-13B -> HS-13B -> JB-12B`, `HS-13B -> MOV-13B`.

### Filters/bypass/relief
- Discharge to filter inlet: `6" PUMP DISCHARGE HEADER -> FE-201 -> FCV-201 -> HV-201 -> 4" FILTER INLET MANIFOLD`; flow control `FE-201 -> FT-201 -> FIC-201 -> FCV-201`; chemical injection from `1/2" CHEMICAL DOSING HEADER` near `FE-201`.
- Filter A: `4" FILTER INLET MANIFOLD -> HV-21A -> FLT-201A -> HV-22A -> XV-22A -> 4" FILTER OUTLET MANIFOLD`, with `VV-21A`, `DV-21A`, and DP chain `DPI-21A -> DPT-21A -> PDI-201 -> PDT-201 -> JB-201`.
- Filter B: `4" FILTER INLET MANIFOLD -> HV-21B -> FLT-201B -> HV-22B -> XV-22B -> 4" FILTER OUTLET MANIFOLD`, with `VV-21B`, `DV-21B`, and DP chain `DPI-21B -> DPT-21B -> JB-201`.
- Bypass/relief: `4" FILTER INLET MANIFOLD -> HV-230 -> FCV-230 -> HV-231 -> 4" FILTER OUTLET MANIFOLD`; relief `4" FILTER INLET MANIFOLD -> PSV-201 -> RD-201 -> VV-202`.

### Heat exchangers/service water/right controls
- SW inlet: `OPC-SW-IN -> SW-HV-301 -> SW-FE-301 -> SW-FCV-301 -> 8" SERVICE WATER SUPPLY HEADER`; control loop `SW-FE-301 -> FT-301 -> FIC-301 -> SW-FCV-301`, with `JB-201` wiring to FT/FIC-301.
- SW supply/return headers connect to both `HX-31A` and `HX-31B`; return exits through `8" SERVICE WATER RETURN HEADER -> SW-HV-302 -> SW-CV-302 -> OPC-SW-OUT`, with `SW-DV-301` on the return drain branch.
- CCW side: `4" FILTER OUTLET MANIFOLD -> MOV-301 -> 4" HX INLET MANIFOLD`; HX branches `4" HX INLET MANIFOLD -> HV-31A -> HX-31A -> HV-32A -> 4" HX OUTLET MANIFOLD` and B equivalent.
- HX outlet/supply: `4" HX OUTLET MANIFOLD -> TCV-301 -> PCV-302 -> HV-303 -> 6" CCW SUPPLY HEADER -> HV-401 -> OPC-CCW-S01`; controls `TE-301 -> TIC-301 -> TCV-301`, `PT-302 -> PIC-302 -> PCV-302`, `TAH-301 -> PAL-302 -> JB-301`.
- Right-side flow/control bypass: `6" CCW SUPPLY HEADER -> FE-401`, `PY-401 -> FE-401 -> PT-401`, `FE-401 -> FT-401 -> FIC-401 -> FCV-401`, and lower path `FE-401 -> FCV-401 -> HV-402 -> CV-402 -> HV-403 -> MOV-404`.

### Chemical dosing
- Tank/skid: `TK-301 -> HV-301 -> FLT-301`, with `TK-301 -> VV-301`, `TK-301 -> DV-301`, `TK-301 -> LT-301`, and level wiring `LT-301 -> LSL-301 -> JB-302`.
- Metering branches: `FLT-301 -> P-301A -> PD-301A -> CV-301A -> 1/2" CHEMICAL DOSING HEADER`; `FLT-301 -> P-301B -> PD-301B -> CV-301B -> FV-301 -> MIX-301 -> 1/2" CHEMICAL DOSING HEADER`.
- Solenoid/analyzer/control: `JB-302 -> SV-301A -> P-301A`, `JB-302 -> SV-301B -> P-301B`, `AIT-301 -> AIC-301 -> 1/2" CHEMICAL DOSING HEADER`, plus `AIC-301 -> JB-101` and `JB-302 -> JB-101`.

### Sample/analyzer and control/IA bay
- Sample panel tap: `8" SERVICE WATER RETURN HEADER -> SAMPLE / ANALYZER PANEL`; sample routes through `SV-501/SV-502/SV-503`, `SC-501`, `SP-501`, `RV-501`, `DV-501`, `AV-501`, `AIT-501`, `AI-501`, `AAL-501`, `JB-501`.
- IA/control: `OPC-IA-IN -> 1" IA HEADER - 80 PSIG`, with drops to `AFR-201`, `AFR-230`, `AFR-301`, `AFR-401`; AFRs are connected to nearby pneumatic control valves where routing is visually aligned.
- Data/control marshalling: `JB-201 -> JB-202 -> DCS / PLC DATA BUS`, `JB-12A/B -> JB-202`, `JB-301 -> JB-402`, `JB-101/JB-302/JB-501 -> DCS / PLC DATA BUS`, `JB-402 -> CP-101 -> PLC-101 -> DCS / PLC DATA BUS`, and `CONTROL ROOM LINK -> DCS-001` plus bus ties.

## Ambiguous or uncertain cases

- `MOV-102/HV-103/TK-101` and `HV-104/TK-101/TK-102` are plausible from the local geometry, but the exact top-nozzle/header segmentation is dense; I modeled the visually continuous named chain rather than anonymous elbows.
- `XV-22A/B`, `HV-31A/B`, `HV-32A/B`, `HS-13A/B`, `PT-202`, `PY-202`, `PDT-201`, `PD-301A/B`, `SV-301A/B`, `AIT-301`, `AIC-301`, `CAL-301`, `FV-301`, and `AFR-230` are visible named endpoints but not in the 147-row inventory. I included them because high recall was requested and they have visible connectivity.
- Lower CCW bypass/recirc routing around `FCV-401/HV-402/CV-402/HV-403/MOV-404/HV-405` spans several crops and has crossings/continuations; I included the plausible named chain but did not create anonymous intermediate line nodes.
- AFR-to-control-valve edges are pneumatic/control-air interpretations from visible IA drops and nearby dashed routes; they should be reviewed if only hard-wired signal links are desired.

## Labels not included

- WN ids from `wire_nodes.csv`, anonymous endpoints, unlabeled junctions, bend points, and simple continuation ticks were excluded.
- Pure line-number labels such as `4"-CCW-12A`, `6"-CCW-301-A`, `3"-CCW-505-A`, `1"-VT-SW`, and similar were not included as nodes unless they were elevated to a visible named header/manifold/off-page endpoint.
- Border/grid/title-block text, legends, general notes, and revision-table text were not included.

## Basic validation

- Node count: 193
- Edge count: 236
- Diagonal check: pass
- Symmetry check: pass

## Node order

OPC-CCW-R01, 6" CCW RETURN HEADER, 6" PUMP SUCTION HEADER, RECIRC TO SURGE TANK, 6" PUMP DISCHARGE HEADER, 4" FILTER INLET MANIFOLD, 4" FILTER OUTLET MANIFOLD, 4" HX INLET MANIFOLD, 4" HX OUTLET MANIFOLD, 6" CCW SUPPLY HEADER, OPC-CCW-S01, OPC-SW-IN, 8" SERVICE WATER SUPPLY HEADER, 8" SERVICE WATER RETURN HEADER, OPC-SW-OUT, 1/2" CHEMICAL DOSING HEADER, SAMPLE / ANALYZER PANEL, 3" FLOOR DRAIN / RADWASTE RETURN HEADER, OPC-IA-IN, 1" IA HEADER - 80 PSIG, DCS / PLC DATA BUS, CONTROL ROOM LINK, DCS-001, HS-13A, HS-13B, PT-202, PY-202, PDT-201, QI-301, XV-22A, XV-22B, HV-31A, HV-32A, HV-31B, HV-32B, PD-301A, PD-301B, SV-301A, SV-301B, AIT-301, AIC-301, CAL-301, FV-301, AFR-230, HV-101, FE-101, FT-101, FI-101, TT-101, TY-101, MOV-102, HV-103, TK-101, PSV-101, HV-105, SV-101, TK-102, HV-104, LV-105, LT-101, LIC-101, LSHH-101, LSL-101, JB-101, DV-101, HV-106, HV-107, DV-102, HV-405, MOV-404, HV-12A, STR-12A, P-12A, CV-12A, HV-13A, MOV-13A, VV-12A, DV-12A, PY-12A, PT-13A, JB-12A, HV-12B, STR-12B, P-12B, CV-12B, HV-13B, MOV-13B, VV-12B, DV-12B, PY-12B, PT-13B, JB-12B, FE-201, FCV-201, HV-201, FT-201, FIC-201, HV-21A, FLT-201A, HV-22A, VV-21A, DV-21A, DPI-21A, DPT-21A, PDI-201, JB-201, HV-21B, FLT-201B, HV-22B, VV-21B, DV-21B, DPI-21B, DPT-21B, HV-230, FCV-230, HV-231, PSV-201, RD-201, VV-202, SW-HV-301, SW-FE-301, SW-FCV-301, FT-301, FIC-301, SW-VV-301, HX-31A, HX-31B, MOV-301, VV-31A, PSV-31A, DV-31A, TT-31A, TY-31A, VV-31B, PSV-31B, DV-31B, TT-31B, TY-31B, TCV-301, PCV-302, HV-303, HV-401, TE-301, TIC-301, PT-302, PIC-302, TAH-301, PAL-302, JB-301, FE-401, PY-401, PT-401, FT-401, FIC-401, FCV-401, HV-402, CV-402, HV-403, SW-DV-301, SW-HV-302, SW-CV-302, TK-301, VV-301, DV-301, LT-301, LSL-301, JB-302, HV-301, FLT-301, P-301A, P-301B, CV-301A, CV-301B, MIX-301, SV-501, SC-501, SP-501, SV-502, SV-503, RV-501, DV-501, AV-501, AIT-501, AI-501, AAL-501, JB-501, JB-402, AFR-201, AFR-301, AFR-401, JB-202, CP-101, PLC-101
