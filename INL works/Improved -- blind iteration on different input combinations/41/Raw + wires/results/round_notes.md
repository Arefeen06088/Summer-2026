# Document 41 Connectivity Extraction Notes

Only files under `Raw + wires` were used. No Ground Truth or GT-derived feedback was used. No off-the-shelf OCR was used.

## Saturated Result

- Nodes: 58
- Edges: 60
- Symmetric matrix: True
- Diagonal zero: True

## Precision Decisions

- Removed/not modeled `BUS_480E1A--CHGR_125A`: No terminal dot or termination at BUS-480E1A; charger route is from BUS-480A.
- Removed/not modeled `BUS_480E1B--CHGR_125B`: Route passes near ESS-B without terminal dot; upstream kept as BUS-480B.
- Removed/not modeled `UPS_BUS_B--INST_RACK_1`: Only A-side UPS feed visibly drops into INST-RACK-1.
- Removed/not modeled `LOAD_TO_RPS_CROSSINGS--RPS_CONTROL`: Crossings near loads have no terminal dots; not modeled as edges.
- Removed/not modeled `PT_UV_SEQ--INST_RACK_1`: PT/UV/SEQ are internal rack markings, not independently externally wired nodes.
- Removed/not modeled `CTRL_86A_OR_B--ANY`: CTRL labels are route labels, not component/node names.

## Round Progress

- Diego R1 proposed the full 58-node graph; the saved unique undirected edge list validates to 60 edges.
- Jennifer R1 kept the graph and rejected unsupported overconnections.
- Diego R2 and Jennifer R2 are saturation confirmations; their matrix files preserve the agreed graph unless manually revised after review.

## Token Estimate Summary

- Total expected tokens estimated: 61497 (low 51197, high 77397).
