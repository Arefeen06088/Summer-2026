# Document 26 Connectivity Extraction Report

## Source Discipline

- Used only `Raw + wires` resources.
- Did not use GT or GT-derived feedback.
- Did not use off-the-shelf OCR; labels were read visually.

## Rounds

| Round | Agent | Nodes | Accepted edges | Outcome |
|---|---:|---:|---:|---|
| Diego R1 | high-recall extraction | 200 | 203 | Main graph proposed; dashed RCP/MOV controls left unresolved. |
| Jennifer R1 | precision review | 200 | 203 | Corrected inverter chain; kept ambiguous dashed endpoints uncertain. |
| Diego R2 | dashed-control revisit | 200 | 205 | Added only `STR-A3-3 -- BUS-120N-A` and `STR-B3-3 -- BUS-120N-B`; rejected/uncertain RCP dashed lower endpoints. |
| Jennifer R2 final | precision review | 200 | 205 | Accepted Diego R2's two dashed/protection additions; no further additions. |

## Final Accepted Additions After R1

- `STR-A3-3 -- BUS-120N-A`: dashed/protection path exits `STR-A3-3` near `MOV-SI-902A` and reaches the `BUS-120N-A` tap area.
- `STR-B3-3 -- BUS-120N-B`: mirrored dashed/protection path exits `STR-B3-3` near `MOV-SI-902B` and reaches the `BUS-120N-B` tap area.

## Final Rejected / Uncertain

- RCP dashed contacts at `CB-4A03` and `CB-4B03`: breaker-side contact is visible, but no labeled lower endpoint is supported strongly enough for a matrix edge.
- `CB-4A03 -- GND-RCP-A` and `CB-4B03 -- GND-RCP-B`: dashed line crosses near ground geometry without a clear junction dot/terminal.
- Extra dashed crossings through DC/UPS buses: not counted unless both endpoints and connection/junction evidence are visible.

## Final Files

- `final_connectivity_matrix.csv`
- `final_edgelist.csv`
- `final_nodes.csv`
- `doc26_round_metadata.json`
- `doc26_token_usage_estimate.csv`
- `doc26_token_usage_estimate.json`
