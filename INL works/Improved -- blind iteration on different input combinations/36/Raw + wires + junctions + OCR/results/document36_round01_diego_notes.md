# Document 36 Round 01 Diego Notes

## Scope and allowed evidence

- Used only the allowed doc36 folder resources: raw schematic image, wire mask/overlay, wire-node overlay/CSV, component_visual_ocr_labels.csv, precision_review_crops, and the provided matrix helper.
- Did not use Ground Truth, evaluator output, or OCR outside the provided component_visual_ocr_labels.csv.
- Treated the raw schematic and component_visual_ocr_labels.csv as authoritative for names. Did not use component_labels_banners_overlay.png for naming because it was flagged as visually inconsistent.

## Node assumptions

- Included all 47 physical components from component_visual_ocr_labels.csv using the label column exactly.
- Added 8 logical busbar nodes where names or busbar labels are visible and where many-to-one taps would otherwise collapse important connectivity: BUS-13K-A, BUS-13K-B, BUS-4K-A, BUS-4K-B, BUS-480-A, BUS-480-B, BUS-DC125-A, and BUS-DC125-B.
- Logical bus bboxes are approximate visual extents covering the visible labeled busbar region rather than OCR-generated component boxes.

## Edge assumptions

- Solid schematic lines were classified as power_feeder except for bus tie breaker connections, which were classified as bus_tie.
- Dashed lines or RPS/ESF labeled control paths were classified as control_interlock.
- Tie breakers labeled TIE OPEN or RPS LOCKOUT are still included as visible connectivity to the breaker component; operational open/closed state is not encoded in the undirected adjacency matrix.
- Filled dots/taps were used as evidence for intentional bus connections. Crossings without dots were not converted into edges.

## Validation summary

- Nodes: 55 total, including 47 physical components and 8 logical busbar nodes.
- Edges: 62 included undirected pairs, with 48 power_feeder, 4 bus_tie, and 10 control_interlock edges.
- Matrix validation: no unknown edge endpoints, no duplicate undirected pairs, zero diagonal, and symmetric 55 by 55 adjacency matrix.

## Ambiguities and low-confidence inclusions

- CB-13-TIE to PNL-RPS-1 is included at medium confidence. The dashed RPS TRIP route is visible from the 13 kV tie area toward the RPS panel, but portions are interrupted by labels and keep-out borders.
- PNL-ESF-A to FAN-CONTAIN-A and PNL-ESF-B to FAN-CONTAIN-B are included at low confidence. A dashed control lane is visible near each fan and routes toward the ESF panel side, but the fan-side vertical contact is less clear than the AFW pump and MOV branches.
- No direct PNL-RPS-1 to PNL-ESF-A or PNL-ESF-B edge was included. The central dashed vertical line visually separates trains and does not show a clear contact into either ESF panel.
- No direct BUS-13K-A to BUS-13K-B or BUS-4K-A to BUS-4K-B edge was added; those ties are represented through CB-13-TIE and CB-4K-TIE respectively.
