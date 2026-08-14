# Round 3 Saturation Notes

Scope: re-inspected only allowed document-12 resources inside the Raw + wires + junctions + OCR folder: raw/crop images, overlays, component_visual_ocr_labels.csv, wire_nodes.csv, and the previously saved Diego proposal in results.

Decision: agree with the 149-edge precision set. I found no strong visual evidence requiring restoration of rejected abstract logical nodes or their edges.

Accepted final added nodes are the nine named buses visible on the drawing: BUS-4KV-A, BUS-4KV-B, BUS-480-A, BUS-480-B, BUS-480-C, BUS-480-D, DC-BUS-A, DC-BUS-B, BUS-120VAC-ESF.

Rejected final nodes remain rejected: TRAIN-A-INTERLOCK-NET, TRAIN-B-INTERLOCK-NET, RPS-A-CONTROL-NET, RPS-B-CONTROL-NET, RPS-A-SIGNAL-NET, RPS-B-SIGNAL-NET, RPS-A-INTERLOCK-NET, RPS-B-INTERLOCK-NET. The bottom and upper crops show real dashed/dotted/dash-dot bundles, but not a strong named-terminal basis for representing these as final nodes.

Label correction decision: keep DS-F23 literally. The right MCC-1B crop shows CB-F023 feeding a disconnect labeled DS-F23; normalizing to DS-F023 was plausible pattern completion, not strong visual evidence.

Final edge selection: kept Diego edge indices 1-142, 146-147, 192, and 214-217, with DS-F023 endpoint labels changed to DS-F23. Removed all abstract-net edges and the unsupported BUS-120VAC-ESF--SEQ-REC-1 / TB-ANN-1--SEQ-REC-1 proposals.

Ground handling: kept only PNL-RPS-A--GND-1 and PNL-RPS-B--GND-2. Grounds were not merged.
