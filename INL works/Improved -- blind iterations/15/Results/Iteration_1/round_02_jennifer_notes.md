# Round 02 Jennifer Final Saturation - Doc 15

## Scope

Used only doc 15 input resources/artifacts and the round files in this results folder. No ground truth, evaluator output, validation metrics, previous document outputs, or GT-derived feedback were used.

## Saturation Decision

Final saturation reached. Diego round 02 fully preserved Jennifer round 01's conservative node, accepted-edge, and uncertain-edge split. I independently rechecked the risky cases and found no last unsupported accepted edge and no missing clear direct solid edge.

The final Jennifer CSV files are direct copies of Diego round 02:

- `round_02_jennifer_nodes.csv` copied from `round_02_diego_nodes.csv`
- `round_02_jennifer_edges.csv` copied from `round_02_diego_edges.csv`
- `round_02_jennifer_uncertain.csv` copied from `round_02_diego_uncertain.csv`

## Final Policy Confirmation

- Node set remains stable at 183 nodes: all 163 detected component labels, visually named buses, MCC/GND component nodes, and the four visually drawn SEQ/RPS control blocks.
- No anonymous `WN-*` nodes are included.
- Accepted edges remain limited to visually supported direct solid power/bus/device connectivity.
- Normally-open ties remain represented only as device-segment paths: `BUS-416A` -> `CB-TIE-AB` -> `DS-TIE-AB` -> `BUS-416B` and `BUS-416C` -> `CB-TIE-CD` -> `DS-TIE-CD` -> `BUS-416D`. No direct bus-to-bus shortcut is present.
- Dashed control/trip/status paths, relay links, and DC row paths remain out of accepted edges and in uncertain candidates when visually plausible.

## Risky Area Audit

- `BUS-NSS-1` -> `DG-1A`: not accepted; retained as uncertain because the DG symbol visually touches/lies on the NSS bus but has no explicit junction dot.
- `BUS-NSS-1` -> `DG-1B`: not accepted and not uncertain; visual crops show a gap to the NSS bus, while `DG-1B` -> `CB-DG-B` is the clear solid connection.
- `BUS-NSS-2` -> `DG-1C`: not accepted; retained as uncertain for the same no-dot visual-contact reason as DG-1A.
- `BUS-NSS-2` -> `DG-1D`: not accepted and not uncertain; visual crops show a gap to the NSS bus, while `DG-1D` -> `CB-DG-D` is the clear solid connection.
- DC row BAT/CHG/BUS-DC/INV/CP/TB/JB/GND paths remain uncertain because the row is dashed/control-style wiring even where endpoints are visually direct.

## Counts

- Nodes: 183
- Accepted edges: 126
- Uncertain candidates: 70

## Endpoint Audit

Endpoint audit passed on the final Jennifer round 02 files: every accepted and uncertain edge endpoint exists in `round_02_jennifer_nodes.csv`.
