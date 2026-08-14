# Doc 7 Iteration 1 Final Connectivity Summary

Workflow: Diego high-recall extraction -> Jennifer precision review -> Diego high-recall challenge -> Jennifer precision acceptance -> Diego saturation check.

Nodes: 120
Edges: 131

Node policy: 110 component/OCR labels plus ten visible named electrical buses/load centers: BUS-13A, BUS-13B, BUS-4A, BUS-4B, LC-480A, LC-480B, LC-480C, LC-480D, BUS-125DCA, BUS-125DCB.

Final key corrections:
- Restored DS-SAT-1--TR-SAT-B after zoom review of the long upper solid feeder.
- Rejected DC-bus-to-AC-panel taps because the panel routes are dashed/control and not solid DC bus taps.
- Added direct dashed control terminal edges for UPS/ANN/PPS/relay/SR paths where both endpoints were visually supported.
- Excluded raceways, container headings, feeder labels, and anonymous intermediate wire points.

Raw title-block sanity note: the drawing visibly says 120 nodes / 140 edges. The final matrix keeps 120 nodes and 131 visually supported unique edges; ambiguous dashed crossings/pass-throughs were documented rather than promoted.

No GT, GT-derived validation, evaluator output, or metric feedback was used during extraction.
