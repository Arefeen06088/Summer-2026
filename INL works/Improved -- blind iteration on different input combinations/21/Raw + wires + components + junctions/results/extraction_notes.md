# Document 21 Connectivity Extraction

Generated: 2026-07-16T10:11:58

Allowed resource folder: `C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\21\Raw + wires + components + junctions`

No GT or GT-derived files were used. No off-the-shelf OCR was used; labels and topology were read visually from the raw schematic plus deterministic crops/overlays.

## Multi-Agent Rounds

- Round 01 Diego: high-recall extraction. Included plausible but later rejected bus ties, an overcalled BUS-202A breaker label, and uncertain lower control/EDG continuation edges.
- Round 02 Jennifer: precision review. Corrected MCC source buses, rejected 480 V direct tie edges, corrected `CB-204A`, and represented unresolved drawing continuations only as conditional synthetic nodes.
- Round 03 Diego: saturation pass. Accepted Jennifer's topology, while still carrying synthetic continuation placeholders for unresolved drawing continuations.
- Round 04 Jennifer: final scoring-oriented pass. Removed synthetic scored nodes and kept continuations as notes only.

## Final Graph Policy

- Final matrix uses named nodes from the schematic only.
- The unlabeled breaker on the `BUS-202A` to `DS-202A` EDG feeder is visually real but not named; it is collapsed as `BUS-202A -- DS-202A` instead of inventing a component label.
- `RECT-24C`, `BAT-EDG-A/B`, `CP-CRD`, and the vertical dashed control rail are documented as visible continuation/interlock evidence where applicable, but unsupported synthetic continuation nodes are not included in the final scored matrix.
- Direct `BUS-301A -- BUS-302A` and `BUS-301B -- BUS-302B` ties are rejected.
- The final graph is undirected, symmetric, and has a zero diagonal.

## Final Counts

- Nodes: 193
- Undirected edges: 187
- Validation: {"diagonal_zero": true, "duplicate_edges": [], "missing_nodes": [], "valid": true}
