# Doc 30 / Iteration 1 Diego Round 02 Convergence Notes

## Source Boundary

Used only doc 30 input resources, doc 30 prepared crops/artifacts, Diego round 01, and Jennifer round 01. Raw schematic evidence remained primary. OCR/component overlays, wire-node overlays, Diego custom crops, and Jennifer review crops were used only as doc-30-derived visual aids. No ground truth, evaluator output, score feedback, or other document/iteration resources were used.

## Convergence Decision

Diego agrees with Jennifer round 01. `round_02_diego_matrix.csv` is intentionally identical to `round_01_jennifer_matrix.csv`.

## Verified Jennifer Changes

### `CAP-101` Removal

Accepted Jennifer's removal of `CAP-101` as a matrix node. The `cap_opc109_zoom.png` raw-derived crop shows `CAP-101` as text near a small tick/annotation on the spare branch, not as a distinct inline component symbol with its own two-terminal connectivity. This preserves the no-anonymous/no-annotation-node policy.

Removed/accepted absent:
- `CAP-101`
- `CAP-101 -- MOV-141`
- `CAP-101 -- OPC-109`

### Spare Branch Representation

Accepted Jennifer's direct `MOV-141 -- OPC-109` edge. The raw crop shows the spare off-page branch leaving the MOV-141 vertical run and terminating at the `OPC-109` off-page connector. With `CAP-101` treated as annotation text, direct adjacency is the cleanest high-recall representation.

Added/accepted present:
- `MOV-141 -- OPC-109`

### `JB-101` To `PIC-101` / `TIC-101`

Accepted Jennifer's removal of:
- `JB-101 -- PIC-101`
- `JB-101 -- TIC-101`

The `tic_pic_jb_zoom.png` and wire-node zoom show the `TIC-101` and `PIC-101` dashed signal routing as local loop/trunk geometry near the instruments. They do not visibly terminate directly on `JB-101`. `JB-101` retains its direct visible control/JB/DCS trunk relationships where supported.

## Brief Review Of Retained Ambiguous Choices

- `H-103 -- H-105`: retained. Raw and wire-node crops still support a plausible downcomer/intersection between the cooler discharge/header area and clean CCW supply header.
- `VV-111 -- H-101`: retained. The V-101/VV-111 raw crop still shows a plausible tie into the adjacent suction header geometry.
- `FCV-171 -- IAH-100`: retained as a visible pneumatic/instrument-air association at the actuator/header area, not as a process-pipe edge.
- `LSHH-101 -- VV-107` and `LSHH-101 -- PSV-108`: retained. The dashed high-level relation is visible in the TK-101 relief/vent crop.
- Bottom row-G chain/taps: retained. Raw crops show the unlabeled horizontal run and vertical taps; Jennifer's adjacent-chain model avoids adding anonymous header/junction nodes.
- `PT-201 -- H-107`: retained. The pressure signal is visibly associated with the chemical injection header/riser area; `H-107` remains the best named endpoint.

## Preserved Node Policy

- All 150 inventory components retained.
- Accepted non-inventory nodes: `DH-100`, `FLG-101`, `H-101`, `H-102`, `H-103`, `H-104`, `H-105`, `H-106`, `H-107`, `IAH-100`, `OPC-101`, `OPC-102`, `OPC-103`, `OPC-104`, `OPC-105`, `OPC-106`, `OPC-107`, `OPC-108`, `OPC-109`, `RH-100`, `SH-100`, `VH-100`.
- Rejected non-inventory annotation node: `CAP-101`.
- Continued to exclude `WN-*`, `BR-*`, line-number-only labels, unlabeled elbows/crossings/t-sections, and clique-expanded long headers.

## Final Validation Counts

- Nodes: 172
- Inventory component nodes retained: 150
- Accepted non-inventory nodes: 22
- Undirected edges: 208
- Blank top-left cell: True
- Row/column labels identical: True
- Duplicate node labels: 0
- Values only 0/1: True
- Matrix symmetric: True
- Diagonal zero: True
- Isolated nodes: none
