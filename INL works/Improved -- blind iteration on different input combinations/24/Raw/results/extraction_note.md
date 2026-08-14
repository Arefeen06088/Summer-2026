# Case 24 Extraction Note

Generated: 2026-07-14T09:55:53

Allowed evidence used: the raw schematic PNG and raw-derived crops in `codes/crops` only. No GT or GT-derived feedback was used.

## Rounds

- Round 1 Diego: high-recall proposal with all main AC, feeder, DC/RPS, and common load-shed routes. Included two tentative `TRIP-MOD-* -- LOAD-SHED-CAB` candidates.
- Round 2 Jennifer: precision refinement. Removed unsupported direct trip-module/load-shed candidates; rejected relay-to-relay feeder chains, B-side meter, ground merges, direct load-shed-to-sequence-recorder, annunciator-to-lamp, and lamp-to-lamp edges.
- Round 3 Diego: agreed with Jennifer; confirmed `SYNC-CAB` is visibly labeled and connected to `CB-TIE-1` by dashed control/trip route.

## Final Decisions

- Final node count: 200
- Final edge count: 200
- Ground symbols are separate labeled terminal nodes; they are not merged together.
- `METER-V1` is included only on `DC-BUS-125A`; no B-side meter label was visible.
- Feeder control uses local `HS-2* -- RELAY-K2* -- MCC-2*` edges only; no cross-feeder control-chain edges are included.
- `TRIP-MOD-A -- LOAD-SHED-CAB` and `TRIP-MOD-B -- LOAD-SHED-CAB` remain uncertain/rejected for the final matrix.

## Files

- `final_connectivity_matrix.csv`: final saturated matrix.
- `final_edges.csv`: final saturated edge list.
- `round_01_diego_high_recall_matrix.csv`, `round_02_jennifer_precision_matrix.csv`, `round_03_diego_saturation_matrix.csv`: round matrices.
