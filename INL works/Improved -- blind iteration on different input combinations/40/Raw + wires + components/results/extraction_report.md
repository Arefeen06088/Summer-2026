# Document 40 Extraction Report

Blind visual extraction used only the raw schematic and the provided derived component/wire visual aids. No GT/GT-derived feedback and no off-the-shelf OCR were used.

## Final Result

- Nodes: 55
- Edges: 56
- Symmetric matrix: True
- Diagonal zero: True
- Unknown edge endpoints: 0
- Duplicate undirected edges: 0

## Saturation

Diego R1 produced a high-recall graph. Jennifer R2 removed label-only nodes and unsupported MCC-to-CT/VT source associations. Diego R3 agreed with Jennifer's graph unchanged. Jennifer R4 confirmed saturation; final counts here are validated from the approved edge CSV.

## Key Precision Decisions

- `TIE-BKR-21AB` is retained as the only A/B 4160 V bus tie node; no direct `SWGR-21A--SWGR-21B` edge is added.
- `Voltage-Sig-A/B` and `Trip-MPA1/MPB1` are labels on signal/trip lines, not final matrix nodes.
- `CT-21A/B` and `VT-21A/B` remain as instrument-signal nodes connected to their RPS panels; inferred MCC source edges are excluded.
- Cable IDs, voltage ratings, channel headings, and control-lane labels are excluded as non-component text.
