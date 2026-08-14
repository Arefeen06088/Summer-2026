# Connectivity Extraction Report - Document 21

Allowed inputs used: raw schematic, detected-components overlay, wire mask, and wire-mask overlay. No GT or GT-derived feedback was used. No off-the-shelf OCR was used.

Subagent rounds:
- Round 1 Diego: high-recall extraction.
- Round 1 Jennifer: precision pruning of bus-end ties, ambiguous UVLS/inter-panel trunks, and unsupported labels.
- Round 2 Diego: accepted Jennifer's pruning, promoted zoom-supported CB-204A, and proposed UNLABELED-CB-EDG-2A.
- Round 2 Jennifer: accepted the final policy and saturated.

Final matrix nodes: 200
Final undirected edges: 192

Key final decisions:
- `CB-204A` is included because the zoom crop makes the EDG-1B upstream breaker label legible.
- `UNLABELED-CB-EDG-2A` is included as a visual placeholder for the clearly drawn but unlabeled breaker before `DS-202A`; `CB-204B` was not invented.
- `DS-501A/DS-502A/DS-501B/DS-502B` are used for the 480 V feeder disconnects.
- Horizontal dashed control rows and dotted signal rows are included as connectivity.
- UVLS taps, CP-CRD lower trunk, and vertical inter-panel trunks are preserved in the uncertain/excluded file rather than guessed into the matrix.
