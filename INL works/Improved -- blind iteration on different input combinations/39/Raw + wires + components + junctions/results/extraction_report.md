# Document 39 Extraction Report

Blind visual extraction used only the raw schematic and derived component/wire visual aids in the resource folder. No GT/GT-derived feedback and no off-the-shelf OCR were used.

## Final Result

- Nodes: 53
- Edges: 55
- Symmetric matrix: True
- Diagonal zero: True
- Unknown edge endpoints: 0
- Duplicate undirected edges: 0

## Saturated Decisions

- `CB-TIE-AB` is retained as a breaker node; no direct `BUS-4160-A-BUS-4160-B` edge is added.
- `GND-PLANT` is excluded as a reference symbol.
- `ANN-CR01-REC-SOE01` is included as a visible dashed endpoint-to-endpoint connection.
- `JB-A101-ANN-CR01` and `REC-SOE01-JB-B101` remain excluded because endpoints are not visually supported.
