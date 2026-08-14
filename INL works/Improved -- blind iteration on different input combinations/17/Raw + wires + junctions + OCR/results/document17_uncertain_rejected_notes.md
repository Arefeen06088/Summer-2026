# Document 17 Uncertain And Rejected Notes

Scope used: only files in `Raw + wires + junctions + OCR` were used. I used the raw drawing as authoritative plus the provided component label CSV wire node CSV overlays and review crops. I did not use Ground Truth evaluator feedback or off-the-shelf OCR.

## Modeling Choices

- Edge endpoints in `document17_edge_list.csv` use visual labels. Proposed non-component nodes are listed in `document17_node_additions_corrections.csv` with `ADD-*` IDs.
- BUS-4KV-A and BUS-4KV-B are normalized labels for raw BUS-4160-A and BUS-4160-B.
- BUS-120-RPS-A and BUS-120-RPS-B are normalized labels for the raw lower BUS-120AC-A and BUS-120AC-B buses in the Train A/B DC RPS ESF control areas.
- MCC-480-A and MCC-480-B are semantic aliases for the long BUS-480-A and BUS-480-B feeder busbars rather than separate electrical conductors.

## Included Low Confidence Connectivity

- MASTER-TERMINAL-BLOCKS to CB-TIE-4AB and CB-TIE-480AB is included because dashed control geometry is visually near the master terminal block and tie-breaker area. The exact terminal numbers are not resolved.
- BUS-125DC-A and BUS-125DC-B to PNL-DCS are included as low confidence control-power continuations because long dashed lower routes visually enter the central control/DCS region.
- Selected MCC load feedback paths from terminal blocks limit switches and junction boxes to lower RPS ESF DCS or annunciator panels are included with low confidence. These are visually/geometrically plausible dashed continuations but not always traceable continuously through crossings.
- ANN-ESF-A to REC-SOE-1 and ANN-ESF-B to REC-SOE-2 are included as low confidence annunciator/SOE signal paths because dashed boundaries overlap in the central annunciation area.
- BUS-480-A to CB-DC-A and BUS-480-B to CB-DC-B are medium confidence because the long route is visually plausible from the AC train regions to the lower DC charger breaker areas but portions pass through dashed boundary corridors.
- GND-DC-B is proposed as a missing ground node because the raw lower right DC bus shows a ground symbol near BUS-125DC-B that is not present as a labeled component row.

## Rejected Artifact

- PP-E1-480-125R is treated as a title-block or reference drawing artifact. It is proposed in the node additions file with action `reject_artifact` and intentionally excluded from the edge list.

## Residual Ambiguity

- Several MCC feeder lower continuations use dashed control lines that cross other dashed boundaries. I kept them as low confidence rather than dropping them.
- The raw terminal block box labelled MASTER TERMINAL BLOCKS is visible but its individual terminal numbering is too small in the provided crops to assign terminal-level edges confidently.
- Some CT and instrument taps are represented as direct instrument-tap edges even when the symbol is drawn on the same physical feeder conductor.
