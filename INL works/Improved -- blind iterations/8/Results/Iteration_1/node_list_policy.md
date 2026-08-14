# Document 8 Iteration 1 - Node List Policy

Scope: extracted only from `Input resources` for document 8 plus inspection crops generated from the raw image into the provided `Codes and artifacts` folder. No ground truth, evaluator output, validation metrics, or external resources were used.

Accepted component nodes:
- Physical components visibly labeled in `component_visual_ocr_labels.csv`.
- Additional visibly labeled components missed by OCR but clear in the raw schematic: `MCC-2A1`, `MCC-2A2`, `MCC-2B1`, `MCC-2B2`, `MCC-2C`, `MCC-2D`, `PN-125B`, `CB-52B`, `PUMP-AF-2B`.
- Visual ground label `GND-A` is used; the OCR row `GND-AJ` appears to be the same symbol/label area.

Accepted logical electrical nodes:
- Named buses only: `BUS-4160-N2A`, `BUS-4160-N2B`, `BUS-4160-S2A`, `BUS-4160-S2B`, `BUS-480-E2A`, `BUS-480-E2B`, `BUS-480-N2A`, `BUS-480-N2B`, `BUS-125DC-A`, `BUS-125DC-B`, `BUS-120AC-A`, `BUS-120AC-B`.
- Named source/intermediate line `2E-100` is kept as a logical node because it is visibly labeled on the generator/UAT source run.
- Grounds `GND-A` and `GND-B` are kept as logical ground nodes.

Excluded as nodes:
- Wire corners, filled dots, unlabeled taps, crossings, and wire-node CSV IDs.
- Container headings, dashed cabinet/raceway boundaries, section titles, terminal block labels, cable numbers, and phase letters.
- Cable/reference IDs such as `2E-110`, `2E-140`, `2E-180`, `2E-190`, `2E-200`, `2C-254`, and `2C-263` are used only as evidence notes, not as graph nodes.

Edge policy:
- Edges are undirected.
- High-confidence edges use solid power geometry or clear named bus/component terminals.
- Dashed CT/PT/control/protective relay links are included only when visually plausible and are mostly separated into lower-confidence edges.
- Normally open switches/breakers are still included as connectivity-through-device edges, with operating state captured in notes where visible.
