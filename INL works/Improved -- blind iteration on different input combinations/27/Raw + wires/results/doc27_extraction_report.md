# Document 27 Connectivity Extraction Report

## Source Discipline

- Used only `Raw + wires` resources.
- Did not use GT or GT-derived feedback.
- Did not use off-the-shelf OCR; labels were read visually.

## Rounds

| Round | Agent | Nodes | Accepted edges | Outcome |
|---|---:|---:|---:|---|
| Diego R1 | high-recall extraction | 200 | 199 | Main graph proposed; A10/B01 charger and battery region over-included. |
| Jennifer R1 | precision review | 200 | 200 | Promoted `CHGR-125A/B`; removed unsupported `JB-A10` to DC bus and B battery ties. |
| Diego R2 | saturation check | 200 | 200 | Rechecked Jennifer corrections against focused crops. |
| Jennifer R2 final | precision review | 200 | 200 | Confirmed saturated final matrix; no additions/removals. |

## Final Accepted Charger / DC / Ground Edges

- `BUS-480-A -- CHGR-125A`
- `CHGR-125A -- DC-BUS-125A`
- `BUS-480-B -- CHGR-125B`
- `CHGR-125B -- DC-BUS-125B`
- `DC-BUS-125A -- DC-BUS-125B`
- `DC-BUS-125A -- PANEL-CTRL-MAIN`
- `BUS-480-C -- GND-EQ-A`
- `BUS-480-D -- GND-EQ-B`

## Final Rejected / Uncertain

- `JB-A10 -- DC-BUS-125A`: `JB-A10` has a visible dotted signal drop to `LT-A10`, not a clear DC bus tie.
- `DS-B01 -- BAT-125B` and `BAT-125B -- DC-BUS-125B`: battery is visible, but no certain conductor/junction ties it into the B01 feeder or DC bus.
- `CHGR-125A/B -- BAT-125A/B` and `BAT-125A/B -- DC-BUS-125A/B`: charger/battery internals are not visually certain enough to count.
- `PANEL-CTRL-MAIN -- DC-BUS-125B`: the panel tap is represented once as `DC-BUS-125A -- PANEL-CTRL-MAIN` on the continuous central DC bus.

## Final Files

- `final_connectivity_matrix.csv`
- `final_edgelist.csv`
- `final_nodes.csv`
- `doc27_round_metadata.json`
- `doc27_token_usage_estimate.csv`
- `doc27_token_usage_estimate.json`
