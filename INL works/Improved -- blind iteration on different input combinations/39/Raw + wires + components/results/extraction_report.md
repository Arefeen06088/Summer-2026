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

- `CB_TIE_AB` is retained as a breaker node; no direct `BUS_4160_A-BUS_4160_B` edge is added.
- `GND_PLANT` is excluded as a reference symbol.
- `ANN_CR01-REC_SOE01` is included as a visible dashed endpoint-to-endpoint connection.
- `JB_A101-ANN_CR01` and `REC_SOE01-JB_B101` remain excluded because endpoints are not visually supported.
