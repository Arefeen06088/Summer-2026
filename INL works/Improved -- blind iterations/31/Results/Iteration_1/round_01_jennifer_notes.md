# Round 01 Jennifer Precision-Refined Connectivity Notes

Scope: Jennifer reviewed only the doc31 raw schematic, doc31 component inventory/crops, and Diego's round 01 files in `Results\Iteration_1`. The raw image was treated as authoritative. Solid lines were treated as process/utility piping; dashed and dot-dashed lines were included only where both visible endpoints were supported. Crossings without a filled tee dot were not promoted to junctions.

## Summary of Changes From Diego

- Removed nodes: none.
- Added nodes: none beyond Diego's node set.
- Renamed nodes: none.
- Removed edges: 6.
  - `FT-511A` -- `FCV-511A`
  - `HV-511A` -- `HX-301A`
  - `HV-511B` -- `HX-301A`
  - `HV-511B` -- `HX-301B`
  - `FH-301` -- `HV-203`
  - `TIC-310` -- `HV-512B`
- Added edges: 4.
  - `FT-511A` -- `HV-511A`
  - `FCV-511A` -- `HX-301A`
  - `FCV-511B` -- `HX-301A`
  - `FT-203` -- `HV-203`

## Accepted Final Node Policy

The final matrix retains all 169 inventory components and all 20 Diego-added visible non-inventory endpoints/components: `OPC-101`, `HV-101`, `SUH-201`, `QH-203`, `LV-401`, `SP-401`, `OPC-905`, `OPC-90_AUX_VENT`, `OPC-50_SW_SUPPLY`, `OPC-50_SW_RETURN`, `OPC-40_SUPPLY_HDR`, `OPC-40_CCW_RETURN`, `OPC-90_INST_AIR`, `OPC-90_DCS_LINK`, `OPC-90_DRAIN_SUMP`, `MOV-401`, `PCV-401`, `LSH-401`, `LSL-401`, and `MOV-402`.

No anonymous wire nodes, WN ids, unnamed elbows, bends, tee points, or line-number-only labels were admitted as nodes. Repeated `OPC-*` labels remain service-qualified because the raw drawing shows distinct off-page endpoints.

## Edge Evidence by Region

### TK-101 Makeup, Tank Instruments, and Relief/Vent

Diego's local TK-101 edges were retained. `OPC-101 -> HV-101 -> STR-101 -> FCV-101 -> TK-101` is visibly continuous. `FT-101`, `FIC-101`, `LIC-101`, `LT-101`, `LSHH-101`, `LSLL-101`, `LG-101`, and `PI-101` are kept as direct local instrument/control endpoints where the dashed lines visibly land. The top tank paths remain separated as `TK-101 -- VT-101` and `TK-101 -- PSV-101 -- HV-103`; no extra tie was added between the vent and relief branches.

### P-201A/B Trains and Recirc Tie

The pump train chains remain local: suction header to train suction valves/strainers/pumps, then check valves and MOVs into `DIH-201`. `SUH-201` and `QH-203` are kept because both are visibly named, and `QH-203` sits at the filled-dot recirc return tie. `QH-203 -- HV-203` is retained as the named recirc return path; it is a long line, but it is visually continuous and specifically labeled as the recirc return tie.

### FH-301, FT-203, and HV-203 Junction

Diego's `FH-301 -- HV-203` was replaced with `FT-203 -- HV-203`. The raw/crop view shows `FT-203` as the named endpoint on the vertical filter-inlet segment before the lower branch toward `HV-203`/`FCV-203`; keeping `FH-301 -- HV-203` skipped over that named local endpoint. `FH-301 -- FT-203`, `HV-203 -- FCV-203`, and `FT-203 -- FIC-203 -- FCV-203` remain.

### Filter/Cooler A/B Process Side

The A/B filter and cooler process chains remain linear: `FH-301` to the A/B inlet valves, filters, outlet valves, heat exchangers, and outlet valves toward `COH-301`. Instrument taps on `FLT-301A/B` and `HX-301A/B` were kept only where the dashed/tap line terminates locally on the equipment or adjacent branch.

### Service-Water Branches Around HX-301A/B

This is the densest region and received the main precision edits. `FT-511A -- FCV-511A` was replaced by `FT-511A -- HV-511A` because `FT-511A` lies on the supply branch/header side and the immediate local valve on that branch is `HV-511A`; the `FIC-511A -- FCV-511A` dashed control edge already captures the controller-to-valve signal. `HV-511A -- HX-301A` was replaced by `FCV-511A -- HX-301A`, and `HV-511B -- HX-301A` / `HV-511B -- HX-301B` were removed in favor of the nearer FCV-side cooler adjacency. `FCV-511B -- HX-301A` was added while Diego's `FCV-511B -- HX-301B` was retained.

`TIC-310 -- HV-512B` was removed because the dot-dashed/dashed signal path in that crowded area does not clearly terminate on `HV-512B`. The supported direct temperature/control endpoints retained are `TI-512A -- TIC-310`, `TIC-310 -- TT-310`, and the existing local taps around `HV-512A/B` where visible.

### V-401, DH-401, PCV/MOV/LV, and Return Controls

The missed visible nodes `LSH-401`, `LSL-401`, `LV-401`, `MOV-401`, `MOV-402`, and `PCV-401` are retained. `V-401` keeps direct level and switch dashed edges and the visible valve branches to `HV-430`, `DV-401`, `LV-401`, and the service-water return/control path. `DH-401 -- MOV-401 -- OPC-40_SUPPLY_HDR` and `DH-401 -- PCV-401 -- RTH-401` remain supported by solid pipe branches. `FI-401 -- MOV-401` and `PIC-401 -- PCV-401` remain direct dashed endpoint signals.

### Return Strainer and Sample Path

`OPC-40_CCW_RETURN -- MOV-402 -- STR-402 -- HV-402 -- RTH-401` is retained. `PT-402` and `TI-402` remain local taps on the return-strainer line. The sample path is kept as `STR-402 -- SV-401 -- SP-401 -- SAM-101`; no anonymous sample junctions were added.

### TK-601 Chemical Dosing and SAM-101

The chemical dosing train is retained as local visible chains from `OPC-905` through `HV-610`/`FCV-610` into `TK-601`, from `TK-601` through the A/B metering pumps into `CHH-601`, and from `CHH-601` through `FCV-601`/`RD-601` toward `IQ-601`. The sample path remains separate as `CHH-601 -- SV-601 -- SP-601 -- SAM-101`, with `PH-601 -- SP-601` as a dashed analyzer/sample connection. I did not add extra merges between the chemical injection, CCW, sample, and drain lines where the nearby parallel lines are not unambiguous.

### MCC, CP, PLC, DCS, JB, and Instrument Air

The wiring/control bay remains sparse. Retained signal edges are `HS-201A -- MCC-201`, `HS-201B -- MCC-201`, `JB-101 -- CP-101`, `JB-102 -- PLC-101`, `PLC-101 -- DCS-001`, and `PLC-101 -- OPC-90_DCS_LINK`. Instrument air remains `REG-601 -- IAH-101 -- OPC-90_INST_AIR`. No bus-like cliques were added.

## Removed / Rejected Candidates

| node_a | node_b | reason |
|---|---|---|
| FT-511A | FCV-511A | Removed from Diego. `FT-511A` is on the supply branch/header side; the nearer visible branch valve is `HV-511A`, while `FIC-511A -- FCV-511A` captures the direct control signal. |
| HV-511A | HX-301A | Removed from Diego. The FCV-side branch is the nearer named endpoint to `HX-301A`; retaining `HV-511A -- HX-301A` skipped over `FCV-511A`. |
| HV-511B | HX-301A | Removed from Diego. The branch passes through the `FT-511B`/`FCV-511B` area before the cooler connection, so this was treated as overconnected. |
| HV-511B | HX-301B | Removed from Diego. Same service-water-branch overconnection; `FCV-511B -- HX-301B` remains as the nearer accepted edge. |
| FH-301 | HV-203 | Removed from Diego. The line from `FH-301` to the lower branch has `FT-203` as the nearer named endpoint, so the accepted local replacement is `FT-203 -- HV-203`. |
| TIC-310 | HV-512B | Removed from Diego. The crowded dot-dashed path does not clearly terminate on `HV-512B`; accepted TIC endpoints are the visible temperature-controller links. |

## Uncertain / Plausible But Not Accepted

| node_a | node_b | reason |
|---|---|---|
| FT-203 | FCV-203 | Plausible through the same lower branch, but `FT-203 -- HV-203 -- FCV-203` is the more local accepted path without adding a second junction-spanning edge. |
| SWS-501 | HV-511A | Plausible branch continuation, but `SWS-501 -- FT-511A -- HV-511A` preserves the visible named FT endpoint on that header segment. |
| RD-601 | FI-601 | The RD/FI area has close parallel chemical-injection and CCW lines; I left Diego's existing chemical path intact rather than merging the nearby lines. |
| LV-401 | MOV-402 | The LV outlet appears to enter the return-strainer inlet area, but the accepted endpoint is `LV-401 -- STR-402`; a separate LV-to-MOV edge would overstate the inlet tee. |
| TIC-310 | FCV-310 | The control around TIC/FIC-310 is visually plausible but not direct enough; retained control edge is `FIC-310 -- FCV-310`. |
| COH-301 | RTH-401 | Retained in the final matrix because the vertical header segment is visibly continuous between named header boxes; nevertheless it remains a long-header adjacency and should not be expanded into additional cliques. |

## Basic Validation

- Node count: 189
- Edge count: 212
- Symmetry: pass
- Diagonal: pass
- Isolated nodes: 0
