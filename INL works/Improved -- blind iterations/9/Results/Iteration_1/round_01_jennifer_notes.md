# Round 01 Jennifer Notes

## Scope

Reviewed only doc 9 input resources, raw schematic/crops, and Diego Round 1 proposal files in the doc 9 results folder. No GT, evaluator output, validation metrics, or prior keys were used.

## Node Review

- Final node count is 180.
- Diego's 17 named bus nodes are visually supported: BUS-13K-01; BUS-4160-N1/N2; BUS-4160S1A/S1B; BUS-480-A1/A2/B1/B2; BUS-480-N1A/N1B/N2A/N2B; BUS-125DC-A/B; BUS-120AC-A/B.
- The four center devices Diego added are real named nodes: RTD-PNL-A, RTD-PNL-B, TDR-SEQ-A, and TDR-SEQ-B.
- Name fixes: Diego's JB-1A0, JB-2A0, JB-1B0, and JB-2B0 were corrected to JB-1A, JB-2A, JB-1B, and JB-2B. Zoomed raw crops show the side circles are terminal marks, not trailing O/0 label characters.

## Edge Review

- No Diego high-confidence solid power edges were removed; they were visually supported as endpoint-to-endpoint connections in the reviewed crops.
- Accepted edge count is 180 after adding visually supported plausible connections and removing duplicate direction/type combinations.
- Promoted dashed/instrument/control edges where both endpoints are visibly named: CT/PT to relay inputs, relay-to-86 links, normal sequence chain MTR -> JB-NORM -> RTD-PNL -> TB-SEQ -> TDR-SEQ, PLC-to-relay/annunciator branches, PN-125 to JB links, PN-120 to PLC links, and adjacent PN-480 normal panel dashed ties.
- MOV feed refinement: PN-MOV-A is accepted from FAN-CR-A because the solid conductor visibly continues from the FAN-CR-A branch into PN-MOV-A. PN-MOV-B is accepted from MCC-SAF-B2 because its feed is a separate branch from the MCC-SAF-B2 feeder area, not through FAN-CR-B.

## Kept Out / Uncertain

- Removed/kept out overconnected MOV alternatives: MCC-SAF-A2 -- PN-MOV-A and FAN-CR-B -- PN-MOV-B.
- Kept out long MCC-to-PN-125 dashed routes because they follow broad train/control routing and do not show clean endpoint ownership.
- Kept out PN-120A/B direct-to-annunciator edges; the visually supported named path is via PLC-ESF-A/B to ANN-ESF-A/B.
- Kept out RELAY-86A/B direct trip edges to CB-482A, CB-481B, CB-482B, and CB-TIE-41N because nearby crossings/shared dashed paths make terminal ownership ambiguous.

## Round 2 Re-checks

- Re-check CB-TIE-41N dashed control path with a tighter crop if a later pass needs breaker-trip/interlock detail.
- Re-check B-side RELAY-86B paths to CB-481B/CB-482B only if terminal-level trip edges are required; current visual evidence supports uncertainty rather than acceptance.
- Re-check whether the synthetic schematic intended A-side PN-MOV-A to be functionally sourced upstream of FAN-CR-A; visually, the endpoint-to-endpoint line is FAN-CR-A -- PN-MOV-A.
