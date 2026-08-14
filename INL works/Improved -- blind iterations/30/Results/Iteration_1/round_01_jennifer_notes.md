# Doc 30 / Iteration 1 Jennifer Connectivity Notes

## Source Boundary

Reviewed only doc 30 input resources, doc 30 prepared crops/artifacts, and Diego's round-01 proposal. The raw schematic was the primary evidence. OCR, wire overlays, and the new `jennifer_review_crops` zoom crops were used only as aids cut from doc 30 resources.

## Change Log From Diego

- Rejected `CAP-101` as a matrix node. The raw spare-branch crop shows the text near a small tick/annotation on the `OPC-109` branch, but no distinct inline component symbol or endpoint requiring a separate node.
- Removed `MOV-141 -- CAP-101` and `CAP-101 -- OPC-109`.
- Added `MOV-141 -- OPC-109` to preserve the visually connected off-page spare branch without the unsupported cap node.
- Removed `TIC-101 -- JB-101` and `PIC-101 -- JB-101`. The zoomed raw control crop shows their dashed signal lines routing through local instrument/control loops, not terminating directly on `JB-101`.
- No other Diego edges were changed.

## Added Nodes

Accepted all 150 inventory physical-component labels.

Accepted non-inventory node `FLG-101`: raw-visible inline flange on the inlet chain between `HV-101` and `MOV-102`.

Accepted raw-visible off-page connectors: `OPC-101`, `OPC-102`, `OPC-103`, `OPC-104`, `OPC-105`, `OPC-106`, `OPC-107`, `OPC-108`, `OPC-109`.

Accepted named headers/logical nodes: `VH-100`, `RH-100`, `IAH-100`, `H-101`, `H-102`, `H-103`, `H-104`, `H-105`, `H-106`, `H-107`, `SH-100`, `DH-100`.

Rejected non-inventory node: `CAP-101`.

## Edge Decisions

Panel/control area:
- Kept `CP-101 -- PLC-101`, `JB-101 -- JB-102`, `JB-101 -- DCS-001`, `JB-102 -- DCS-001`, and `FIC-120 -- DCS-001` because the raw crop shows direct visible panel/JB/DCS trunks.
- Removed `TIC-101 -- JB-101` and `PIC-101 -- JB-101`; the raw dashed signals do not terminate directly on `JB-101`.

Headers and top process area:
- Kept `H-103 -- H-105`; the raw and wire-node crops show a real downcomer/intersection between the cooler discharge/supply header area and `H-105`.
- Kept `VV-111 -- H-101`; the raw crop shows the `VV-111`/`V-101` line tying into the `H-101` suction header.
- Kept `FCV-171 -- IAH-100` as a visible pneumatic/header association at the actuator/header area, but marked it ambiguous because it is not a solid process-pipe edge.
- Kept `LSHH-101 -- VV-107` and `LSHH-101 -- PSV-108` as visible dashed high-level/relief associations; semantics remain ambiguous.

Branch trains:
- Kept the repeated `H-105` to branch equipment to `H-106` chains for 201-208.
- Kept `FI-20x -- FE-20x` and `TI-20x -- equipment` associations; the dashed local instrument ties are visible for each train.

Chemical injection and dosing:
- Kept `PT-201 -- H-107`; the pressure signal is visibly tied to the local chemical injection header/feed near `H-107`, though the exact endpoint is close to the `HV-302`/`IQ-201` riser.
- Kept `MX-201 -- FCV-301 -- HV-302 -- IQ-201 -- H-107 -- HX-201` as a visually supported abstraction around the dosing tee and chemical injection header.
- Kept `FT-301 -- FIC-301`, `FIC-301 -- FCV-301`, and `FT-301 -- FCV-301`.

Bottom sample/drain area:
- Kept row-G chain `FCV-301 -- SV-201 -- DV-201 -- SV-203 -- DV-203 -- PCV-151 -- HV-150 -- H-106`. Raw and wire-node crops show real junctions along the horizontal run, but this remains a modeling abstraction because no named row-G header is present.
- Kept direct taps from `H-106` to `SV-201`, `DV-201`, `SV-203`, and `DV-203`; vertical drops from `H-106` into these valve runs are visible.
- Kept `SV-201 -- SH-100`, `SV-203 -- SH-100`, `DV-201 -- DH-100`, and `DV-203 -- DH-100`.
- Kept drain pot/pump path `V-401 -- P-401 -- CV-402 -- HV-401 -- SH-100`.
- Kept `V-401 -- DH-100 -- HV-403 -- OPC-107`.

## Ambiguous Cases Retained

- `FCV-171 -- IAH-100`: retained as a visible pneumatic/header association, not a process-pipe edge.
- `LSHH-101 -- VV-107` and `LSHH-101 -- PSV-108`: retained because the dashed relation is visible, but exact control/alarm semantics are uncertain.
- `PT-201 -- H-107`: retained; the pressure tap is near the chemical injection header/riser and is best represented by `H-107`.
- Bottom row-G sample/drain chain and `H-106` taps: retained as the least overexpanded representation without adding anonymous junction nodes.

## Final Validation Counts

- Nodes: 172
- Inventory component nodes retained: 150
- Accepted non-inventory nodes: 22
- Rejected Diego added nodes: 1 (`CAP-101`)
- Undirected edges: 208
- Row/column labels identical: True
- Matrix symmetric: True
- Diagonal zero: True
- Values valid: True
- Duplicate row labels: 0
- Duplicate column labels: 0
- Malformed rows: 0
- Isolated nodes: none
