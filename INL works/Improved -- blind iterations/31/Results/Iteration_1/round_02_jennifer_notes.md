# Round 02 Jennifer Final Confirmation Notes

Scope: I used only doc31 local resources and round files in `Results\Iteration_1`. No ground truth, evaluator output, prior score feedback, or outside files were used.

## Decision

Agreement and saturation were reached. `round_02_diego_matrix.csv` is byte-identical to `round_01_jennifer_matrix.csv` and Jennifer's final `round_02_jennifer_matrix.csv` is an exact copy of Diego Round 02.

- Matrix SHA-256: `201466c4b5f8ce57e7dc908cc4e7116b049eba8e787a5ff5e3dfdfcf370fe77a`
- Round 02 action: no additional nodes, removals, additions, or renames.
- Saturation result: no remaining precision issue found in the quick review of the disputed local regions.

## Quick Saturation Check

I rechecked the same high-risk regions that drove the Round 01 refinement:

- Service-water branches around `SWS-501`, `SWR-501`, `HX-301A`, and `HX-301B`: the accepted Round 01 local endpoints still fit the raw crops. `FT-511A -- HV-511A`, `FCV-511A -- HX-301A`, `FCV-511B -- HX-301A`, and `FCV-511B -- HX-301B` avoid jumping across nearer named components.
- `FH-301` / `FT-203` / `HV-203`: `FT-203` remains the nearer named endpoint on the vertical segment before the lower branch, so `FH-301 -- FT-203 -- HV-203` remains the precision representation.
- `TIC-310` near `HV-512B`: the dot-dashed path remains crowded and does not clearly terminate on `HV-512B`; the accepted direct TIC endpoints remain the safer choice.
- Return strainer, V-401 controls, TK-601 dosing, and the MCC/PLC/DCS bay: no new direct endpoint connection was visible enough to add, and no retained local edge was unsupported enough to remove.

## Accepted Final Node Policy

The final matrix retains all 169 inventory components and the same 20 visible non-inventory endpoints/components retained in Round 01: `OPC-101`, `HV-101`, `SUH-201`, `QH-203`, `LV-401`, `SP-401`, `OPC-905`, `OPC-90_AUX_VENT`, `OPC-50_SW_SUPPLY`, `OPC-50_SW_RETURN`, `OPC-40_SUPPLY_HDR`, `OPC-40_CCW_RETURN`, `OPC-90_INST_AIR`, `OPC-90_DCS_LINK`, `OPC-90_DRAIN_SUMP`, `MOV-401`, `PCV-401`, `LSH-401`, `LSL-401`, and `MOV-402`.

No anonymous intermediate nodes, WN ids, junction ids, bends, t-sections, crossing points, or line-number-only labels were added.

## Removed / Rejected Candidates

| node_a | node_b | reason |
|---|---|---|
| FT-511A | FCV-511A | Rejected from Diego R01 and still rejected in final saturation. `FT-511A` is on the supply branch/header side; the nearer visible branch valve is `HV-511A`, while `FIC-511A -- FCV-511A` captures the direct control signal. |
| HV-511A | HX-301A | Rejected from Diego R01 and still rejected. The FCV-side branch is the nearer named endpoint to `HX-301A`; retaining `HV-511A -- HX-301A` skipped over `FCV-511A`. |
| HV-511B | HX-301A | Rejected from Diego R01 and still rejected. The branch passes through the `FT-511B`/`FCV-511B` area before the cooler connection, so this remains overconnected. |
| HV-511B | HX-301B | Rejected from Diego R01 and still rejected. Same service-water branch overconnection; `FCV-511B -- HX-301B` remains as the nearer accepted edge. |
| FH-301 | HV-203 | Rejected from Diego R01 and still rejected. The line from `FH-301` to the lower branch has `FT-203` as the nearer named endpoint, so the accepted local path is `FH-301 -- FT-203 -- HV-203`. |
| TIC-310 | HV-512B | Rejected from Diego R01 and still rejected. The crowded dot-dashed path does not clearly terminate on `HV-512B`; accepted TIC endpoints are the clearer temperature-controller links. |

## Uncertain / Plausible But Not Accepted

| node_a | node_b | reason |
|---|---|---|
| FT-203 | FCV-203 | Plausible through the same lower branch, but `FT-203 -- HV-203 -- FCV-203` is the more local accepted path without adding a second junction-spanning edge. |
| SWS-501 | HV-511A | Plausible branch continuation, but `SWS-501 -- FT-511A -- HV-511A` preserves the visible named FT endpoint on that header segment. |
| RD-601 | FI-601 | The RD/FI area has close parallel chemical-injection and CCW lines; the final matrix leaves the existing chemical path intact rather than merging nearby lines. |
| LV-401 | MOV-402 | The LV outlet appears to enter the return-strainer inlet area, but the accepted endpoint is `LV-401 -- STR-402`; a separate LV-to-MOV edge would overstate the inlet tee. |
| TIC-310 | FCV-310 | The control around TIC/FIC-310 is visually plausible but not direct enough; retained control edge is `FIC-310 -- FCV-310`. |
| COH-301 | RTH-401 | Retained in the final matrix because the vertical header segment is visibly continuous between named header boxes; nevertheless it remains a long-header adjacency and should not be expanded into additional cliques. |

## Basic Validation

- Node count: 189
- Edge count: 212
- Shape/header check: pass
- Symmetry: pass
- Diagonal: pass
- Isolated nodes: 0
- Matrix provenance: exact copy of `round_02_diego_matrix.csv`; also byte-identical to `round_01_jennifer_matrix.csv`
