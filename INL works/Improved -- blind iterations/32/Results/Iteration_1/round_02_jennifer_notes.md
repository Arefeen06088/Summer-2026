# Round 02 Jennifer Final Confirmation Notes

## Saturation And Agreement

Saturation/agreement reached: yes. I compared `round_02_diego_matrix.csv` against `round_01_jennifer_matrix.csv`; they are semantically identical, and the copied Jennifer Round 02 matrix has SHA-256 `11E3A286D7C37ADA57D676648CCCD06F9ACB60485540EA7A1B745EA4749E58F1`. After a quick saturation check of the disputed left tank/makeup, vent/relief, service-water, recycle, distribution, bottom return/drain, and control-bay regions, I found no remaining precision issue.

I therefore used Diego Round 02 exactly as `round_02_jennifer_matrix.csv`. No nodes, edges, or names were changed in Jennifer Round 02.

## Confirmation Checks

- Diego Round 02 equals Jennifer Round 01: pass
- Jennifer Round 02 equals Diego Round 02: pass
- Node count: 184
- Edge count: 208
- Symmetry: pass
- Diagonal: pass
- Valid values: pass
- Isolated nodes: 0

## Saturation Evidence

- `TK-501 -- PI-501 -- V-501` remains the supported tank-to-air-separator path; the direct `TK-501 -- V-501` skip edge remains rejected.
- `OPC-CHM-501 -- TK-501` remains supported, while `OPC-CHM-501 -- LIC-501` remains rejected as label/control proximity rather than a direct endpoint.
- `OPC-VENT-501 -- HDR-VENT-501` remains accepted as the named vent header/off-page endpoint; relief and vent valves are not expanded into unsupported far-end shortcuts.
- `TCV-560A -- PI-550` remains the supported A-side service-water process path; `TCV-560A -- HV-561A` remains rejected.
- The bottom return sequence remains `CV-580 -- HV-580 -- HDR-RET-501`, with `TT-590` and `PT-590` on `HDR-RET-501`; `HDR-DRN-501` remains separate and tied to `OPC-DRN-501`.
- The 601-607 distribution branches remain per-column only, with no cross-column edges added.
- The control bay remains sparse: `CP-501 -- JB-501 -- JB-502 -- DCS-501`.

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
- Valid values: pass
- Isolated nodes: 0
