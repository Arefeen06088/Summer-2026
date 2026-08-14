# Jennifer Refinement Notes - Doc 27 / Iteration 1 / Round 01

## Scope Statement
Inspected only the allowed Doc 27 resources under `Input resources`, the derived/crop artifacts under `Codes and artifacts`, and Diego's round-01 outputs under `Results/Iteration_1`. The raw schematic was treated as the primary evidence, with crops/overlays used only as aids. No ground truth, GT-derived evaluator output, score feedback, or resources from any other document/iteration were used.

## Final Node Policy
- Final matrix keeps Diego's 200-node order and label set.
- `TE-41` remains excluded. In the raw top/tie region, the only distinct visible device is `CB-TIE-41`; `TE-41` is a partial/OCR split near that breaker label, not a separate instrument symbol or termination.
- Raw-visible electrical objects beyond the 190-item inventory are retained where clearly printed as bus/ground/panel connectivity objects: `BUS-13KV-N`, `BUS-4160-A`, `BUS-4160-B`, `BUS-480-A`, `BUS-480-B`, `BUS-480-C`, `BUS-480-D`, `DC-BUS-125A`, `DC-BUS-125B`, `PANEL-CTRL-MAIN`, and `GND-EQ-B`.
- Section titles and feeder-family captions remain notes-only. Intermediate wire-node IDs are not matrix nodes.
- Dotted enclosure boundaries in the DC center were not treated as electrical conductors.

## Edge Changes vs Diego
| Action | Edge | Rationale |
|---|---|---|
| Added | `BUS-480-A -- CHGR-125A` | Raw shows the A charger box fed by a solid vertical tap from `BUS-480-A`. |
| Added | `BUS-480-B -- CHGR-125B` | Raw shows the B charger box fed by a solid vertical tap from `BUS-480-B`. |
| Removed | `DS-A10 -- CHGR-125A` | The apparent crossing is a dotted enclosure boundary near the A10 branch, not a conductor from the disconnect to the charger. |
| Removed | `DS-B01 -- CHGR-125B` | The B charger is on its own bus tap; the nearby dotted enclosure line is not connectivity to `DS-B01`. |
| Removed | `CHGR-125A -- DC-BUS-125A` | No distinct drawn conductor from the A charger to the DC bus; dotted enclosure geometry was not promoted. |
| Removed | `CHGR-125B -- DC-BUS-125B` | No distinct drawn conductor from the B charger to the DC bus; dotted enclosure geometry was not promoted. |
| Removed | `BAT-125A -- DC-BUS-125A` | Battery symbol is visible, but no direct raw conductor termination to the DC bus is shown. |
| Removed | `BAT-125B -- DC-BUS-125B` | Battery symbol is visible, but no direct raw conductor termination to the DC bus is shown. |
| Removed | `JB-A10 -- DC-BUS-125A` | The `JB-A10` dashed drop continues toward `LT-A10`; it does not visibly terminate on the DC bus line. |
| Removed | `DC-BUS-125A -- DC-BUS-125B` | The line appears continuous, but separate `125A`/`125B` labels make a direct logical bus merge ambiguous. |
| Removed | `DC-BUS-125B -- PANEL-CTRL-MAIN` | Retained only one panel-to-DC-bus representative edge to avoid using the panel tap as a hidden A/B bus tie. |

## Accepted Edge Rationale by Region
### Top Sources and 13 kV Bus
Kept Diego's source chain: `GRID-345 -- DS-101 -- CB-101 -- BUS-13KV-N`, generator taps through `CB-G1`/`CB-G2`, and transformer feeds from `BUS-13KV-N` to `TR-1A`/`TR-1B` through the shown transformer/breaker paths. No `TE-41` node or edge was added.

### 4.16 kV Buses, Diesel Sources, and Tie
Kept the visible diesel source chains to `BUS-4160-A` and `BUS-4160-B`, plus the breaker-mediated tie `BUS-4160-A -- CB-TIE-41 -- BUS-4160-B`. No direct A/B 4160 bus shortcut was added.

### 480 V Transformers and Load-Center Buses
Kept the cross-panel transformer feeds confirmed in the full left/right crops: `BUS-4160-A` feeds `TR-480-A` and `TR-480-C`; `BUS-4160-B` feeds `TR-480-B` and `TR-480-D`. Kept each transformer through its incoming breaker to its own 480 V bus.

### A/B/C/D Feeder Branches
Kept Diego's repeated bus-to-breaker-to-device-to-load/end-device chains where each vertical branch is visibly drawn. Feeder family captions remain notes-only, and bus sections were not clique-expanded.

### DC Center
Kept `PANEL-CTRL-MAIN` as a raw-visible named component with a direct dashed vertical termination on the DC bus line, represented as `DC-BUS-125A -- PANEL-CTRL-MAIN`. Added charger input edges from the 480 V buses. Removed charger/battery/JB/DC-bus edges that depended on dotted enclosure boundaries or on inferred functional relationships rather than direct drawn conductors.

### Grounds
Kept `GND-EQ-A -- BUS-480-C` and `GND-EQ-B -- BUS-480-D`; the lower crops show the named ground symbols and dashed conductors terminating at the respective lower 480 V bus regions.

## Uncertain / Plausible Candidates
| Candidate | Status | Reason |
|---|---|---|
| `DC-BUS-125A -- DC-BUS-125B` | Omitted as uncertain | The heavy horizontal line appears continuous, but the raw prints two distinct DC bus labels; a direct edge could overmerge logical A/B buses. |
| `DC-BUS-125B -- PANEL-CTRL-MAIN` | Omitted as uncertain | The panel tap lands near the shared DC bus line; connecting it to both DC bus labels would create a hidden A/B tie. |
| `BAT-125A -- DC-BUS-125A` | Omitted as uncertain | The battery is visible, but no direct conductor to the DC bus is clearly drawn. |
| `BAT-125B -- DC-BUS-125B` | Omitted as uncertain | The battery is visible, but no direct conductor to the DC bus is clearly drawn. |
| `CHGR-125A -- DC-BUS-125A` | Omitted as uncertain | Functionally plausible charger/DC relation, but the visible geometry is enclosure/dotted boundary, not a clear conductor. |
| `CHGR-125B -- DC-BUS-125B` | Omitted as uncertain | Functionally plausible charger/DC relation, but the visible geometry is enclosure/dotted boundary, not a clear conductor. |
| `JB-A10 -- DC-BUS-125A` | Omitted as uncertain | The nearby dashed branch aligns with `LT-A10`; the DC bus touch is not visually definite. |

## Removed / Rejected Candidates
| Candidate | Decision | Reason |
|---|---|---|
| `TE-41` node | Rejected | False OCR split/partial label near `CB-TIE-41`; no separate instrument symbol/termination found. |
| `DS-A10 -- CHGR-125A` | Removed | Dotted enclosure crossing was not a conductor. |
| `DS-B01 -- CHGR-125B` | Removed | Dotted enclosure crossing was not a conductor. |
| Dotted DC enclosure boundaries as nodes/edges | Rejected | Boundaries frame the charger/battery area and are not electrical connectivity objects. |
| Section titles / feeder captions as nodes | Rejected | They describe regions/families, not conductor bus labels or components. |

## Output Summary
- Nodes: 200
- Unique undirected edges: 196
- Matrix remains symmetric with matching row/column labels and zero diagonal.
