# Round 01 Jennifer Precision-Refined Connectivity Notes

Scope: reviewed only the doc33 raw schematic, doc33 component inventory/crops/artifacts, and Diego round 01 matrix/notes in the paths specified by the prompt. No ground truth, evaluator output, prior feedback, validation metrics, or outside files were used.

## Summary of Changes from Diego

- Nodes removed: 0. All 193 Diego nodes were retained because each inventory component remained in scope and the added non-inventory nodes used here are visible named headers, manifolds, off-page connectors, control/data boxes, or visible named instruments/valves/equipment.
- Nodes added: 0.
- Renamed nodes: none.
- Edges removed: 20.
- Edges added: 6.
- Net effect: the graph is stricter around the DCS/data bus, junction boxes, AFR pneumatic routes, DP filter instruments, CAL-301, and the TK-101/TK-102 makeup path.

## Accepted Final Node Policy

- Retained all 147 inventory components from `component_labels_list.csv`.
- Retained Diego-visible non-inventory nodes only where they are named endpoints in the raw drawing: named headers/manifolds, off-page connectors, the data/control bus, control-room/control-panel/PLC/DCS boxes, visible hand-switch/control boxes, and visible named omitted instruments/valves/equipment.
- Did not add anonymous wire nodes, WN ids, junction ids, elbows, bends, continuation ticks, or line-number-only labels.
- For long headers/buses with intervening named components, local named adjacency is preferred over skip edges.
- Crossings without filled dots were not treated as connections.

## Edge Evidence by Region

### Return / Surge / Makeup

- Kept the return inlet sequence `OPC-CCW-R01 -> HV-101 -> FE-101 -> 6" CCW RETURN HEADER`, plus the local instrument pair `FE-101 -> FT-101 -> FI-101` and `TT-101 -> TY-101`.
- Kept the visible tank and suction piping around `MOV-102`, `HV-103`, `TK-101`, `PSV-101`, `HV-105`, `HV-104`, `TK-102`, `DV-101`, `HV-106`, `HV-107`, and `DV-102`.
- Replaced the Diego shortcut `SV-101 -> TK-102` with `SV-101 -> HV-104`, because the local linework routes toward the HV-104 makeup path before TK-102.
- Kept `LT-101 -> LIC-101 -> LV-105` and the visible `LIC-101 -> SV-101` signal/control path.

### Pump Trains

- Kept the solid A/B train sequences through suction header, `HV-12A/B`, `STR-12A/B`, `P-12A/B`, `CV-12A/B`, `HV-13A/B`, `MOV-13A/B`, and the pump discharge header.
- Kept local pump accessories `STR-12A/B -> VV-12A/B`, `P-12A/B -> DV-12A/B`, and `P-12A/B -> PY-12A/B`.
- Kept `PT-13A/B -> HS-13A/B -> JB-12A/B` and `HS-13A/B -> MOV-13A/B`; these dashed paths terminate locally on the shown hand-switch/JB/control endpoints.

### Filters / Bypass / Relief

- Kept `6" PUMP DISCHARGE HEADER -> FE-201 -> FCV-201 -> HV-201 -> 4" FILTER INLET MANIFOLD`, with `FT-201 -> FIC-201 -> FCV-201` as the flow-control signal path.
- Added `PT-202 -> 4" FILTER INLET MANIFOLD`; the raw crop shows PT-202 with its own visible tap at the inlet manifold, not only through `PY-202`.
- Converted the DP indicator area from `DPI -> DPT -> filter` to local visible taps: added `DPI-21A -> FLT-201A` and `DPI-21B -> FLT-201B`, while keeping `DPT-21A -> PDI-201 -> PDT-201 -> JB-201` and `DPT-21B -> JB-201`.
- Kept the A/B filter process paths through `HV-21A/B`, `FLT-201A/B`, `HV-22A/B`, `XV-22A/B`, and the outlet manifold.
- Kept bypass/relief solid paths `HV-230 -> FCV-230 -> HV-231`, and `PSV-201 -> RD-201 -> VV-202`.
- Removed `AFR-201 -> FCV-230`; FCV-230 has the aligned AFR-230 drop, while AFR-201 is retained for FCV-201.

### Heat Exchangers / Service Water / Right Controls

- Kept service-water inlet sequence `OPC-SW-IN -> SW-HV-301 -> SW-FE-301 -> SW-FCV-301 -> 8" SERVICE WATER SUPPLY HEADER`, with `SW-FE-301 -> FT-301 -> FIC-301 -> SW-FCV-301`.
- Kept the supply/return header connections to `HX-31A/B` and the CCW-side paths `4" HX INLET MANIFOLD -> HV-31A/B -> HX-31A/B -> HV-32A/B -> 4" HX OUTLET MANIFOLD`.
- Removed `TY-31A -> VV-31A` and `TY-31B -> VV-31B`; these are crossing/nearby signal and vent-valve centerlines without accepted endpoint dots.
- Kept `TT-31A/B -> TY-31A/B`, `HX-31A/B -> VV-31A/B`, and the `HX-31A/B -> PSV-31A/B -> DV-31A/B` relief/drain branches.
- Kept outlet/supply chain `4" HX OUTLET MANIFOLD -> TCV-301 -> PCV-302 -> HV-303 -> 6" CCW SUPPLY HEADER -> HV-401 -> OPC-CCW-S01`, plus `TE-301 -> TIC-301 -> TCV-301` and `PT-302 -> PIC-302 -> PCV-302`.
- Kept `TAH-301 -> PAL-302 -> JB-301` and right-side marshalling through `JB-301 -> JB-402 -> CP-101 -> PLC-101`.
- Kept `6" CCW SUPPLY HEADER -> FE-401`, `PY-401 -> FE-401`, `PT-401 -> FE-401`, `FT-401 -> FIC-401 -> FCV-401`, and the lower process chain through `FCV-401`, `HV-402`, `CV-402`, `HV-403`, and `MOV-404`.
- Removed `AFR-301 -> TCV-301`, `AFR-301 -> PCV-302`, and `AFR-401 -> FCV-401`; the visible lines there are controller-to-valve signals or process lines, not clear AFR terminal routes.

### Chemical Dosing

- Kept the tank/filter/metering process path `TK-301 -> HV-301 -> FLT-301`, with `FLT-301 -> P-301A/B`, `P-301A -> PD-301A -> CV-301A -> 1/2" CHEMICAL DOSING HEADER`, and `P-301B -> PD-301B -> CV-301B -> FV-301 -> MIX-301 -> 1/2" CHEMICAL DOSING HEADER`.
- Kept `TK-301 -> VV-301`, `TK-301 -> DV-301`, and the local level wiring among `LT-301`, `LSL-301`, and `JB-302`.
- Removed `CAL-301 -> TK-301` and `CAL-301 -> JB-302`; the visible CAL-301 line is process-side, not a tank or JB termination. Added `CAL-301 -> P-301A` as the closest visible named endpoint on the metering suction side.
- Replaced `AIC-301 -> 1/2" CHEMICAL DOSING HEADER` with `AIC-301 -> FV-301`; AIT/AIC are shown as a dashed analyzer/control path, and the visible final-control endpoint is FV-301 rather than the process header.
- Kept `AIT-301 -> AIC-301`, `AIC-301 -> JB-101`, `JB-302 -> SV-301A/B`, `SV-301A/B -> P-301A/B`, and `JB-302 -> JB-101` where the dashed endpoints visibly land.

### Sample / Analyzer / Drains

- Kept `8" SERVICE WATER RETURN HEADER -> SAMPLE / ANALYZER PANEL` and local panel entries through `SV-501`, `SV-502`, and `SV-503`.
- Kept `SV-501/SV-502 -> SC-501 -> SP-501`, `SV-503 -> SP-501`, `SP-501 -> RV-501`, `SP-501 -> DV-501`, and `DV-501 -> 3" FLOOR DRAIN / RADWASTE RETURN HEADER`.
- Kept analyzer path `SP-501 -> AV-501 -> AIT-501 -> AI-501 -> AAL-501 -> JB-501`. Removed `AFR-401 -> AV-501` because the raw linework does not clearly terminate the AFR route on AV-501.

### Control / IA / Data Bus

- Kept `OPC-IA-IN -> 1" IA HEADER - 80 PSIG`, with visible drops to `AFR-201`, `AFR-230`, `AFR-301`, and `AFR-401`.
- Kept only the AFR-to-valve endpoints with clear aligned visible routing: `AFR-201 -> FCV-201`, `AFR-230 -> FCV-230`, and `AFR-301 -> SW-FCV-301`.
- Kept the directly supported data-bus landings `JB-202 -> DCS / PLC DATA BUS`, `PLC-101 -> DCS / PLC DATA BUS`, and `CONTROL ROOM LINK -> DCS / PLC DATA BUS`.
- Kept `CONTROL ROOM LINK -> DCS-001`; removed direct `DCS-001 -> DCS / PLC DATA BUS` because that skip bypasses the visible named link.
- Removed direct data-bus shortcuts from `JB-101`, `JB-302`, `JB-301`, and `JB-501`; their visible routes go through local marshalling/JB/control paths.

## Removed / Rejected Candidates

| node_a | node_b | reason |
|---|---|---|
| `DCS / PLC DATA BUS` | `JB-101` | No visible direct landing from JB-101 onto the data bus; the local chemical/left control wiring routes through JB-302/field instruments. |
| `DCS / PLC DATA BUS` | `JB-302` | JB-302 terminates local chemical skid wiring and the JB-101 route; no direct raw-image endpoint on the data bus was visible. |
| `DCS / PLC DATA BUS` | `JB-301` | JB-301 routes through the local right-side marshalling path toward JB-402 rather than landing directly on the bus. |
| `DCS / PLC DATA BUS` | `JB-501` | JB-501 is visibly tied to the sample/analyzer signal chain and JB-402 route, not directly to the bus. |
| `DCS / PLC DATA BUS` | `DCS-001` | DCS-001 connects via CONTROL ROOM LINK; direct bus-to-DCS shortcut skips the visible named link. |
| `AFR-201` | `FCV-230` | FCV-230 has its own aligned AFR-230 drop; no direct AFR-201 route to FCV-230 was accepted. |
| `AFR-301` | `TCV-301` | Only controller/valve dashed signal is visible; no clear IA/AFR route terminating on TCV-301. |
| `AFR-301` | `PCV-302` | Only PIC/PCV dashed control signal is visible; no clear AFR-301 pneumatic endpoint at PCV-302. |
| `AFR-401` | `FCV-401` | FIC-401 to FCV-401 signal is visible, but the AFR-401-to-FCV-401 pneumatic route does not visibly terminate. |
| `AFR-401` | `AV-501` | AV-501 is on the sample panel process/analyzer path; no visible AFR-401 pneumatic termination was accepted. |
| `DPI-21A` | `DPT-21A` | DPI-21A has a local tap to the filter assembly; it is not visibly chained directly to DPT-21A. |
| `DPT-21A` | `FLT-201A` | DPT-21A is on the dashed signal run to PDI/PDT; no direct visible process/tap endpoint at FLT-201A. |
| `DPI-21B` | `DPT-21B` | DPI-21B has a local tap to the filter assembly; it is not visibly chained directly to DPT-21B. |
| `DPT-21B` | `FLT-201B` | DPT-21B signal continues toward JB-201; no direct visible process/tap endpoint at FLT-201B. |
| `TY-31A` | `VV-31A` | The TT/TY signal line crosses near the vent-valve centerline without a supported endpoint connection. |
| `TY-31B` | `VV-31B` | The TT/TY signal line crosses near the vent-valve centerline without a supported endpoint connection. |
| `CAL-301` | `TK-301` | CAL-301 is not visibly piped directly to TK-301; its visible line tees into the metering-pump suction side. |
| `CAL-301` | `JB-302` | The nearby dashed JB-302 run passes by the calibration column without a clear termination on CAL-301. |
| `AIC-301` | `1/2" CHEMICAL DOSING HEADER` | AIC-301 is on the analyzer/control signal path; the accepted visible endpoint is the final valve signal, not the process header itself. |
| `SV-101` | `TK-102` | SV-101 does not visibly land directly on TK-102; the nearby makeup route is represented locally through HV-104/TK-102. |

## Uncertain / Plausible But Not Accepted

| node_a | node_b | reason |
|---|---|---|
| `CAL-301` | `P-301B` | The calibration-column line tees into the metering suction manifold, but the clearest immediate named branch is P-301A; B-side reach was not accepted. |
| `AFR-301` | `TCV-301 / PCV-302` | Pneumatic service is plausible by loop grouping, but the visible routes are controller-to-valve signals rather than clear AFR terminations. |
| `AFR-401` | `FCV-401 / AV-501` | Pneumatic service is plausible locally, but visible endpoint evidence is insufficient under the strict AFR rule. |
| `JB-301` | `DCS / PLC DATA BUS` | A broader marshalling path exists through JB-402/CP-101/PLC-101, but no direct bus landing was accepted. |
| `JB-501` | `DCS / PLC DATA BUS` | Sample/analyzer signals plausibly reach DCS through marshalling, but the direct bus shortcut is not visible. |
| `TK-301` | `LT-301` | Tank level association is visually plausible; retained from Diego, though the linework is weaker than the solid tank piping. |
| `RECIRC TO SURGE TANK` | `6" CCW RETURN HEADER` | The long recirc/return geometry crosses dense lower-left routing; retained as Diego modeled because the raw line remains visibly continuous enough. |
| `SWBV-31A/B/32A/B` | `HX service-water paths` | The SWBV labels are visible but were not promoted to matrix nodes because the accepted node policy avoids extra non-inventory valve labels without clear component inventory support. |

## Basic Validation

- Node count: 193
- Edge count: 222
- Symmetry: pass
- Diagonal: pass
- Isolated nodes: 0

## Node Order

OPC-CCW-R01, 6" CCW RETURN HEADER, 6" PUMP SUCTION HEADER, RECIRC TO SURGE TANK, 6" PUMP DISCHARGE HEADER, 4" FILTER INLET MANIFOLD, 4" FILTER OUTLET MANIFOLD, 4" HX INLET MANIFOLD, 4" HX OUTLET MANIFOLD, 6" CCW SUPPLY HEADER, OPC-CCW-S01, OPC-SW-IN, 8" SERVICE WATER SUPPLY HEADER, 8" SERVICE WATER RETURN HEADER, OPC-SW-OUT, 1/2" CHEMICAL DOSING HEADER, SAMPLE / ANALYZER PANEL, 3" FLOOR DRAIN / RADWASTE RETURN HEADER, OPC-IA-IN, 1" IA HEADER - 80 PSIG, DCS / PLC DATA BUS, CONTROL ROOM LINK, DCS-001, HS-13A, HS-13B, PT-202, PY-202, PDT-201, QI-301, XV-22A, XV-22B, HV-31A, HV-32A, HV-31B, HV-32B, PD-301A, PD-301B, SV-301A, SV-301B, AIT-301, AIC-301, CAL-301, FV-301, AFR-230, HV-101, FE-101, FT-101, FI-101, TT-101, TY-101, MOV-102, HV-103, TK-101, PSV-101, HV-105, SV-101, TK-102, HV-104, LV-105, LT-101, LIC-101, LSHH-101, LSL-101, JB-101, DV-101, HV-106, HV-107, DV-102, HV-405, MOV-404, HV-12A, STR-12A, P-12A, CV-12A, HV-13A, MOV-13A, VV-12A, DV-12A, PY-12A, PT-13A, JB-12A, HV-12B, STR-12B, P-12B, CV-12B, HV-13B, MOV-13B, VV-12B, DV-12B, PY-12B, PT-13B, JB-12B, FE-201, FCV-201, HV-201, FT-201, FIC-201, HV-21A, FLT-201A, HV-22A, VV-21A, DV-21A, DPI-21A, DPT-21A, PDI-201, JB-201, HV-21B, FLT-201B, HV-22B, VV-21B, DV-21B, DPI-21B, DPT-21B, HV-230, FCV-230, HV-231, PSV-201, RD-201, VV-202, SW-HV-301, SW-FE-301, SW-FCV-301, FT-301, FIC-301, SW-VV-301, HX-31A, HX-31B, MOV-301, VV-31A, PSV-31A, DV-31A, TT-31A, TY-31A, VV-31B, PSV-31B, DV-31B, TT-31B, TY-31B, TCV-301, PCV-302, HV-303, HV-401, TE-301, TIC-301, PT-302, PIC-302, TAH-301, PAL-302, JB-301, FE-401, PY-401, PT-401, FT-401, FIC-401, FCV-401, HV-402, CV-402, HV-403, SW-DV-301, SW-HV-302, SW-CV-302, TK-301, VV-301, DV-301, LT-301, LSL-301, JB-302, HV-301, FLT-301, P-301A, P-301B, CV-301A, CV-301B, MIX-301, SV-501, SC-501, SP-501, SV-502, SV-503, RV-501, DV-501, AV-501, AIT-501, AI-501, AAL-501, JB-501, JB-402, AFR-201, AFR-301, AFR-401, JB-202, CP-101, PLC-101
