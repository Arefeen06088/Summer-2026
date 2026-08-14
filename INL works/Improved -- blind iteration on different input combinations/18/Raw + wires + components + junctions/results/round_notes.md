# Document 18 Connectivity Extraction Notes

Allowed resource folder only:
`C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\18\Raw + wires + components + junctions`

No GT or GT-derived feedback was used. No off-the-shelf OCR was used; labels and topology were read visually from the raw image and allowed derived overlays/crops.

## Rounds

1. Diego high-recall extraction: broad primary/4160/480/control topology, all 480 feeder chains, lower Train A/B control power, and plausible PLC-to-relay/JB dashed branches.
2. Jennifer precision review: retained power topology, pruned relay fanout as uncertain, and removed unsupported UAT-to-4160 downstream edges.
3. Diego second extraction: agreed on power topology and reintroduced visible PLC-to-relay/JB dashed branches as visually supported.
4. Jennifer final correction: accepted all PLC-to-relay/JB dashed branches, kept K102/K202 annunciator branches, and corrected the A-side supply path to `BUS-4160A -> TB-RPS-A -> TR-480-A1`.

## Final Matrix Policy

- `1` means a visually supported undirected connection.
- Solid power, dashed control/signal, and normally-open physical ties are all represented as `1` in the matrix.
- Edge type/status is preserved in `final_edge_list.csv`.
- The normally-open `CB-4160 TIE` is kept as a physical edge but `BUS-4160A` and `BUS-4160B` are not collapsed into one node.

## Final Size

- Nodes: 200
- Edges: 201
