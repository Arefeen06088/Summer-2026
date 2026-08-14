# Document 21 Extraction Notes

Ground truth used: no. OCR used: no. Source scope was limited to the `Raw + wires` folder.

## Rounds

- Round 1 Diego: high-recall graph with 200 nodes. Included the visible but unreadable EDG-2A breaker as `UCB-202A-EDG2A`, plus candidate UVLS serial edges and candidate EDG battery/control edges.
- Round 1 Jennifer: kept all nodes; retained `UCB-202A-EDG2A`; corrected `DS-302B--CB-502B--TR-NB--BUS-302B`; added `BUS-501A--BUS-501B` N.O. tie; changed UVLS to branch taps from `K101`; removed unsupported `BAT-EDG-A/B` to `CP-EDG-A/B` edges.
- Round 2 Diego: saturation check against Jennifer's corrections.
- Round 2 Jennifer: final confirmation. Graph saturated and unchanged from round 1 Jennifer.

## Final Ambiguity Handling

- `BAT-EDG-A` and `BAT-EDG-B` remain visible isolated component nodes because their dashed lead destinations are not visually supported enough for a direct edge.
- `CB-204A` is retained on the `BUS-201B--CB-204A--DS-201B--CB-106--EDG-1B` path with low-confidence tag readability.
- `UCB-202A-EDG2A` is a visible circuit-breaker symbol on the EDG-2A feeder with no readable external tag; it is retained as an unlabeled logical breaker placeholder rather than collapsed.

## Matrix Checks

- Final nodes: 200
- Final undirected edges: 204
- Final nonzero matrix entries: 408
- Symmetric matrix: yes
- Diagonal zeros: yes
