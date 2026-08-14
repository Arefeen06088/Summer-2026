# Document 20 Connectivity Extraction

Generated: 2026-07-16T09:37:03

Allowed resource folder: `C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\20\Raw + wires + components + junctions`

No GT or GT-derived files were used. No off-the-shelf OCR was used; labels and topology were read visually from the raw image and deterministic crops/overlays.

## Rounds

- Round 01 Diego: high-recall graph. Diego represented the A/B ESF interlock as a synthetic node.
- Round 02 Jennifer: precision correction. Jennifer removed the synthetic interlock node and used a direct `RELAY-K106 -- RELAY-K108` edge.
- Round 03 Diego: agreed with Jennifer's correction; graph saturated.
- Round 04 Jennifer: final confirmation; graph saturated.

## Final Graph Policy

- Named buses, breakers, disconnects, transformers, MCCs, JBs, relays, switches, instruments, batteries, chargers, rectifiers, inverters, and loads are nodes.
- Unlabeled connector squares, black bus dots, tick marks, and ordinary wire junction geometry are not semantic nodes.
- Tie breakers are included as topological connectivity nodes. `CB-TIE-416` is marked normally open in the edge table where visible.
- The A/B ESF interlock is represented as direct edge `RELAY-K106 -- RELAY-K108` with evidence `A/B ESF interlock dashed conductor between relay branches`.

## Final Counts

- Nodes: 200
- Undirected edges: 202
- Matrix diagonal: zero
- Matrix symmetry: enforced by generator
