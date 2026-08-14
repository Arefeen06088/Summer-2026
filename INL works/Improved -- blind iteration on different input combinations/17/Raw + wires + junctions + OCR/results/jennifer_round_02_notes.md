# Jennifer Round 02 Precision Notes

Scope: reviewed only the document 17 resource folder and the provided raw/aid images. I did not use Ground Truth, evaluator feedback, files outside the folder, or off-the-shelf OCR.

## Major Decisions

- Normalized Diego's semantic bus labels to the raw visual labels: BUS-4KV-A/B -> BUS-4160-A/B and BUS-120-RPS-A/B -> BUS-120AC-A/B.
- Kept the 4kV, 480V, and 125VDC ties only as breaker-mediated edges through CB-TIE-4AB, CB-TIE-480AB, and CB-DCTIE-AB; no direct bus-to-bus edge was added.
- Dropped both MASTER-TERMINAL-BLOCKS control edges. The terminal-block box is visible, but the dashed corridors near the tie breakers do not land on the block or breakers as clear connections.
- Dropped STS-120-A/B to PNL-ESF-A/B. The visible top dashed feed lands on the RPS panels; I did not infer ESF panel feeds without a visible landed top connection.
- Dropped PNL-RPS-A/B to RELAY-RPS-A/B. The RPS relay leads visually come from the ESF panel routing, not the RPS panel routing; I did not add substitute edges in this precision pass.
- Dropped broad annunciation/SOE overconnections: PNL-DCS to PNL-ANN, PNL-DCS to ANN-ESF-A/B, ANN-ESF-A/B to REC-SOE-1/2, and PNL-DCS to REC-SOE-2.
- Dropped all low-confidence long MCC/control corridor continuations from terminal blocks, limit switches, and radiation junction boxes to RPS/ESF/DCS/ANN panels. They pass through crossing-heavy dashed corridors and are not continuously traceable to landed endpoints.
- Retained local visually landed dashed/terminal continuations such as pump/MOV-to-LS and load-to-terminal-block rows where the crop shows a direct continuation.

## Residual Uncertainties

- Some dropped dashed control routes may represent functional signal relationships, but the raw drawing does not provide enough continuous visual evidence to keep them under a false-positive-heavy scoring regime.
- REC-SOE-2 remains visually present, but Diego's proposed DCS/ANN edges to it were not supported as drawn.
- MASTER-TERMINAL-BLOCKS remains a visible node with no retained edges from Diego's proposal.

## Counts

- Kept final edges: 191
- Removed Diego edges: 32
- Node renames: 4
- Rejected unsupported/artifact node labels: 4
- Merged duplicate aliases: 2
