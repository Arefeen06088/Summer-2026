# Round 01 Jennifer Precision-Refined Connectivity Notes

## Summary Of Changes From Diego

- Removed nodes: none.
- Added nodes: none.
- Renamed nodes: none.
- Removed edges: 13.
- Added edges: 5.

- Removed `OPC-CHM-501` -- `LIC-501`: OPC-CHM-501 is a corrosion-inhibitor off-page/tag box with a solid drop to the tank-side chemical line; the nearby LIC circle is annotation/control context, not a line endpoint.
- Removed `HV-503` -- `OPC-VENT-501`: HV-503 vents into the local 2-inch VENT-501-B1 branch/header, but the far off-page OPC-VENT endpoint is not the direct local endpoint.
- Removed `PSV-501` -- `TK-501`: The PSV-501 lower relief leg is a dashed/relief continuation; no filled dot ties it into the tank inlet/process line.
- Removed `PSV-501` -- `HDR-VENT-501`: PSV-501 is on the 2-inch RV relief leg, not directly on the visible HDR-VENT-501 endpoint/header label.
- Removed `PSV-550` -- `HDR-VENT-501`: PSV-550 is on the service-water/relief vertical leg; the horizontal vent header crossing lacks a filled junction.
- Removed `HDR-RET-501` -- `HDR-DRN-501`: The return and drain headers are separate named horizontal runs in the bottom region; the labels are adjacent but not directly tied.
- Removed `HV-580` -- `OPC-DRN-501`: HV-580 is on the CCW return line upstream of HDR-RET-501; OPC-DRN-501 belongs to the lower drain endpoint.
- Removed `HDR-RET-501` -- `CV-580`: CV-580 is followed locally by HV-580 before the named return-header segment, so the direct return-header adjacency is through HV-580.
- Removed `HDR-DRN-501` -- `TT-590`: TT-590 taps the CCW return line above the drain label, not the separate drain header.
- Removed `HDR-DRN-501` -- `PT-590`: PT-590 taps the CCW return line above the drain label, not the separate drain header.
- Removed `TK-501` -- `V-501`: PI-501 is visibly on the tank-to-air-separator connection; the local path is TK-501 -- PI-501 -- V-501.
- Removed `TCV-560A` -- `HV-561A`: The solid A-side service-water outlet from TCV-560A drops through the PI-550 leg; the line toward HV-561A is crossed by the control/signal run and is not the direct process adjacency.
- Removed `ORF-520` -- `HDR-SUC-501`: ORF-520 is on the recycle/return leg between V-501 and PCV-520/HV-520; no direct tie to the suction-header label is visible.

- Added `OPC-VENT-501` -- `HDR-VENT-501`: The far-right OPC-VENT-501 endpoint and the visible HDR-VENT-501 label identify the same long vent header run.
- Added `HV-580` -- `HDR-RET-501`: HV-580 is the immediate valve upstream of the named HDR-RET-501 return-header segment.
- Added `HDR-RET-501` -- `TT-590`: TT-590 has a dashed tap to the CCW return header near the HDR-RET-501 label.
- Added `HDR-RET-501` -- `PT-590`: PT-590 has a dashed tap to the CCW return header near the HDR-RET-501 label.
- Added `TCV-560A` -- `PI-550`: The A-side service-water outlet from TCV-560A drops on the solid leg carrying PI-550 before entering HX-501A.

## Accepted Final Node Policy

The final matrix keeps Diego's 184-node set: all 166 inventory components plus the 18 visible named non-inventory endpoints/header/control boxes. I retained visible named OPC/HDR/DCS endpoints when the raw drawing shows them as named off-page/header/control endpoints. I did not add anonymous junctions, wire-node IDs, elbows, bends, line-number-only labels, continuation arrows, section titles, or unlabeled crossing points. Crossings without filled dots were not treated as connections.

## Edge Evidence By Region

### Top And Named Header Endpoints

`OPC-IA-501` remains connected to `HDR-IA-501` on the top instrument-air line. `OPC-VENT-501` was connected directly to `HDR-VENT-501` because the far-right vent off-page connector and the visible vent header label identify the same long vent header run. I kept `HV-503` tied to `HDR-VENT-501` as the local 2-inch vent branch, but rejected the far-end `HV-503` to `OPC-VENT-501` shortcut.

### Left Tank, Makeup, Chemical, And Sample Area

The makeup train remains local through `OPC-DMW-501` -- `HV-501` -- `PRV-501` -- `LCV-501` -- `CV-501` -- `TK-501`. The corrosion-inhibitor off-page connector remains tied to `TK-501`; the adjacent `LIC-501` contact was treated as annotation/control proximity and removed. The tank-to-air-separator process path is represented as `TK-501` -- `PI-501` -- `V-501`, so the skip edge `TK-501` -- `V-501` was removed. `V-501` -- `ORF-520` remains accepted as the visible return/recycle leg, but `ORF-520` was not tied directly to `HDR-SUC-501`.

The `PSV-501` relief branch was tightened: its top branch remains local to the makeup segment, but the lower relief continuation does not visibly tie to `TK-501` or to the named vent header endpoint. The `P-503` chemical recirculation path remains `TK-501` -- `HV-506` -- `P-503` -- `CV-503` -- `TK-501`, and the sample path remains `V-501`/`SV-501`/`SP-501` to `OPC-SMP-501` where the dashed sample line terminates.

### Pump Trains And Recycle

The A/B pump train sequencing remains local: `HDR-SUC-501` feeds `HV-510A/B`, strainers, pumps, check/control valves, and then `HDR-DIS-501`. The recycle path remains `HDR-DIS-501` -- `HV-520` -- `PCV-520` -- `ORF-520`, with `PIC-520`/`PT-520` retained as signal/header taps. The rejected `ORF-520` -- `HDR-SUC-501` edge was a long inferred return-to-suction shortcut rather than a visible direct endpoint.

### Filter, Heat Exchanger, And Service Water Area

The filter/HX trains remain local through `HDR-DIS-501` -- `HV-530A/B` -- `FLT-501A/B` -- `HV-531A/B` -- `HX-501A/B` -- `MOV-532A/B` -- `HDR-SUP-501`. Local vent/drain valves on filters and heat exchangers remain connected only to their adjacent equipment, not to a global drain/vent header.

The A-side service-water leg was corrected to `HV-560A` -- `TCV-560A` -- `PI-550` -- `HX-501A`; Diego's `TCV-560A` -- `HV-561A` edge followed a visually nearby dashed control/signal run rather than the solid process leg. The `HX-501A` -- `HV-561A` and B-side `HV-560B` -- `TCV-560B` -- `HV-561B` -- `HX-501B` adjacencies remain. `TT-540` remains tied to `TIC-540` and `HDR-SUP-501`, while `PSV-550` remains locally adjacent to `TT-540`; the unsupported `PSV-550` -- `HDR-VENT-501` header shortcut was removed.

### Right Distribution Branches 601-607

Diego's per-column branch pattern was retained without cross-column additions: each branch runs from `HDR-SUP-501` through `HV-60xA`, `FT-60x`, `FCV-60x`, `HX-60x`, `CV-60x`, `HV-60xB`, and back to `HDR-RET-501`. Each `FT-60x` remains signal-linked to `FIC-60x`, each `FIC-60x` to `FCV-60x`, and each exchanger keeps its local `PI`, `VV`, and `DV` taps. `TI-607` remains local to `HX-607` only.

### Bottom Return, Drain, And Control Bay

The bottom return sequence was corrected to `CV-580` -- `HV-580` -- `HDR-RET-501`. `TT-590` and `PT-590` were moved from `HDR-DRN-501` to `HDR-RET-501` because their dashed taps land on the CCW return line. `HDR-DRN-501` remains a separate named drain header endpoint connected to `OPC-DRN-501` and local drain valves; it is not merged with `HDR-RET-501`. The control bay remains sparse as `CP-501` -- `JB-501` -- `JB-502` -- `DCS-501`.

## Removed / Rejected Candidates

| node_a | node_b | reason |
|---|---|---|
| `OPC-CHM-501` | `LIC-501` | OPC-CHM-501 is a corrosion-inhibitor off-page/tag box with a solid drop to the tank-side chemical line; the nearby LIC circle is annotation/control context, not a line endpoint. |
| `HV-503` | `OPC-VENT-501` | HV-503 vents into the local 2-inch VENT-501-B1 branch/header, but the far off-page OPC-VENT endpoint is not the direct local endpoint. |
| `PSV-501` | `TK-501` | The PSV-501 lower relief leg is a dashed/relief continuation; no filled dot ties it into the tank inlet/process line. |
| `PSV-501` | `HDR-VENT-501` | PSV-501 is on the 2-inch RV relief leg, not directly on the visible HDR-VENT-501 endpoint/header label. |
| `PSV-550` | `HDR-VENT-501` | PSV-550 is on the service-water/relief vertical leg; the horizontal vent header crossing lacks a filled junction. |
| `HDR-RET-501` | `HDR-DRN-501` | The return and drain headers are separate named horizontal runs in the bottom region; the labels are adjacent but not directly tied. |
| `HV-580` | `OPC-DRN-501` | HV-580 is on the CCW return line upstream of HDR-RET-501; OPC-DRN-501 belongs to the lower drain endpoint. |
| `HDR-RET-501` | `CV-580` | CV-580 is followed locally by HV-580 before the named return-header segment, so the direct return-header adjacency is through HV-580. |
| `HDR-DRN-501` | `TT-590` | TT-590 taps the CCW return line above the drain label, not the separate drain header. |
| `HDR-DRN-501` | `PT-590` | PT-590 taps the CCW return line above the drain label, not the separate drain header. |
| `TK-501` | `V-501` | PI-501 is visibly on the tank-to-air-separator connection; the local path is TK-501 -- PI-501 -- V-501. |
| `TCV-560A` | `HV-561A` | The solid A-side service-water outlet from TCV-560A drops through the PI-550 leg; the line toward HV-561A is crossed by the control/signal run and is not the direct process adjacency. |
| `ORF-520` | `HDR-SUC-501` | ORF-520 is on the recycle/return leg between V-501 and PCV-520/HV-520; no direct tie to the suction-header label is visible. |

## Uncertain / Plausible But Not Accepted

| node_a | node_b | reason |
|---|---|---|
| `HV-503` | `OPC-VENT-501` | Same vent service family, but the direct visible endpoint is the local vent header label, not the far off-page connector. |
| `PSV-501` | `TK-501` | Relief leg passes near the tank inlet line; no filled dot or direct endpoint tie is visible. |
| `PSV-550` | `HDR-VENT-501` | The vent header crosses the area, but the PSV leg has no filled junction into that header. |
| `HDR-RET-501` | `HDR-DRN-501` | Both labels are visible in the bottom region, but they name separate parallel runs. |
| `ORF-520` | `HDR-SUC-501` | The recycle line returns toward the left-side equipment, but the visible ORF-520 endpoints are V-501 and PCV-520. |
| `TCV-560A` | `HV-561A` | A dashed control/signal line makes the two valves look aligned; the solid process route from TCV-560A drops to PI-550. |

## Basic Validation

- Node count: 184
- Edge count: 208
- Symmetry: pass
- Diagonal: pass
- Isolated nodes: 0
