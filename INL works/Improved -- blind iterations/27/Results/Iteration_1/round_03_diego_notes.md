# Diego Focused QA Notes - Doc 27 / Iteration 1 / Round 03

## Scope Statement
Used only allowed Doc 27 resources: raw/crop/overlay artifacts under `Codes and artifacts`, Doc 27 input resources as needed, and saved round outputs in `Results/Iteration_1`, starting from `round_02_jennifer_matrix.csv` and `round_02_jennifer_notes.md`. No ground truth, GT-derived evaluator output, score feedback, or other documents/iterations were used.

## Round-03 Decision Summary
Changed the agreed round-02 matrix in one place to resolve the visually supported isolated DC bus node:

| Action | Edge/node | Round-03 decision | Raw basis |
|---|---|---|---|
| Added | `DC-BUS-125A -- DC-BUS-125B` | Accepted | `09_dc_center_raw.png`, `09_dc_center_wire_nodes_overlay.png`, and `jennifer_zoom_dc_bus_panel_raw.png` show the heavy horizontal DC conductor continuing through both labeled bus drops, with junction dots at the A and B bus label locations and no visible break between them. |
| Kept isolated | `BAT-125A` node | No edge added | The raw battery symbol is visible, but it is offset from the solid `DS-A10`/`JB-A10` vertical conductor. The nearby dot-dash enclosure/control boundary is not connectivity. No direct conductor to `DS-A10`, `JB-A10`, or `DC-BUS-125A` is raw-supported. |
| Kept isolated | `BAT-125B` node | No edge added | The raw battery symbol is visible near the B charger/disconnect area, but there is no clear conductor from the battery symbol to `DS-B01`, `DC-BUS-125B`, or `CHGR-125B`. The adjacent dot-dash enclosure/control geometry was not promoted to connectivity. |
| Kept excluded | `TE-41` node | No node added | Re-check found no distinct raw-visible instrument/termination separate from `CB-TIE-41`; the prior visual rejection still stands. |

## Candidate Edge Review
- `BAT-125A -- DS-A10`: omitted. The solid vertical conductor through `DS-A10` continues to the lower `JB-A10` object; it does not visibly terminate on the `BAT-125A` battery plates/symbol.
- `BAT-125A -- JB-A10`: omitted. The `JB-A10` dashed/vertical route is separate from the battery symbol; no raw conductor tie is visible.
- `BAT-125A -- DC-BUS-125A`: omitted. No direct battery-to-bus conductor is visible.
- `BAT-125B -- DS-B01`: omitted. The `DS-B01` vertical route goes to the `PMP-B01` branch; it does not visibly terminate on the `BAT-125B` battery symbol.
- `BAT-125B -- DC-BUS-125B`: omitted. No direct battery-to-bus conductor is visible.
- `DC-BUS-125B -- CHGR-125B`: omitted. The charger area is bounded by dot-dash enclosure/control geometry, not a raw solid conductor to the DC bus.
- `DC-BUS-125B -- PANEL-CTRL-MAIN`: omitted as a direct edge. Since the continuous heavy conductor is now represented by `DC-BUS-125A -- DC-BUS-125B`, the existing `DC-BUS-125A -- PANEL-CTRL-MAIN` edge is sufficient to connect the panel to the same raw bus without adding a duplicate B-side panel edge.
- `DC-BUS-125A -- DC-BUS-125B`: added as the least-wrong representation of the continuous heavy horizontal conductor shared by the two printed DC bus labels.

## Isolated Node Rationale
After round 03, `DC-BUS-125B` is no longer isolated because the raw conductor geometry supports a direct edge to `DC-BUS-125A`.

`BAT-125A` and `BAT-125B` remain isolated intentionally. They are retained as raw-visible named component nodes from the existing matrix/inventory, but no candidate edge met the visual standard for a direct conductor connection. I did not add functional battery/DC relationships without raw conductor support.

## Dotted Line Policy
No broad dotted enclosure/control edges were added. Dot-dash boundaries around the DC charger/battery area were treated as non-conductive enclosure/control geometry unless a distinct endpoint and conductor termination were visible.

## Output Summary
- Matrix file: `round_03_diego_matrix.csv`
- Notes file: `round_03_diego_notes.md`
- Basis matrix: `round_02_jennifer_matrix.csv`
- Matrix change count: one unique undirected edge added, zero nodes added, zero nodes removed
