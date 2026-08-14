# Round 2 Diego Notes

## Review scope

Reviewed Jennifer's Round 1 files in Results/Iteration_1 against only the doc 13 Input resources and generated doc 13 crops/artifacts. I did not use ground truth, evaluator files, metrics, or any prior answer as an authority. The raw schematic remains authoritative; component/OCR overlays and wire-node crops were used only as navigation aids.

## Bottom line

I agree with Jennifer's precision refinement except for node pruning: the off-sheet continuation annotations should not remain in the accepted node set when no accepted in-sheet edge uses them. Round 2 therefore keeps Jennifer's accepted edge set, prunes the two isolated off-sheet continuation nodes, and removes the two off-sheet uncertain rows so all Round 2 edge endpoints are covered by the Round 2 node file.

## Decisions on requested focus areas

1. Battery connectivity: accepted Jennifer's BAT-125* -> CHG-125* -> DC-BUS-* structure. The raw DC/UPS crops show each battery symbol dropping into the charger cluster, with the charger landing on the thick DC-BUS-* 125 VDC bar. I did not restore direct BAT-125* -> DC-BUS-* edges because I did not see a separate clean solid conductor/junction dot from battery directly to the DC bus.

2. LOCAL-IO-* nodes: kept. The raw train crops show LOCAL I/O text at a drawn terminal/tap on the right end of each LC-480* bus region. These are real named terminal endpoints rather than floating notes, so the accepted LC-480* -> LOCAL-IO-* edges remain.

3. Off-sheet continuation nodes: pruned from the accepted node set. CONTINUATION-125VDC-SHT-DC-2 and TO-ANNUNCIATOR-PLANT-PROCESS-COMPUTER are visible annotation/continuation labels, but Jennifer accepted no off-sheet edges and the raw drawing does not provide a clean in-sheet component terminal to accept. To avoid isolated annotation nodes, they are absent from round_02_diego_nodes.csv, and their uncertain edges are also removed.

4. Relays/control edges: relay nodes remain because the relay symbols are physical components in the raw schematic/component inventory. Relay-to-breaker relationships remain uncertain, not accepted, because the visible connections are dashed/short control-trip conductors rather than direct solid power conductors; the drawing notes identify dashed lines as control/trip circuits.

5. Cross-routing and dense DC/UPS candidates: no promotions. SUT/UAT/EDG cross-bus routes, LC-480* -> CHG-125* AC-input candidates, JB-* -> DC-BUS-* candidates, and UPS-* -> LOCAL-IO-* candidates remain uncertain where retained. I did not find raw dots or unambiguous solid conductors strong enough to restore them as accepted edges.

## Output counts and validation

- round_02_diego_nodes.csv: 191 rows, columns node,kind,type,evidence.
- round_02_diego_edges.csv: 170 rows, columns source,target,evidence.
- round_02_diego_uncertain.csv: 33 rows, columns source,target,evidence,uncertainty_reason.
- Duplicate node labels: 0.
- Missing accepted-edge endpoint nodes: 0.
- Missing uncertain-edge endpoint nodes: 0.

Accepted-edge endpoint coverage and uncertain-edge endpoint coverage both validate against the Round 2 node set.
