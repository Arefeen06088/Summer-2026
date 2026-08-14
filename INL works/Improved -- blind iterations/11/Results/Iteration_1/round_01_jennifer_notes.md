# Round 01 Jennifer Notes

## Scope
Reviewed only doc 11 input resources, generated inspection crops/artifacts, and Diego Round 1 files under `Results\Iteration_1`. I did not use ground truth, evaluator outputs, scores, validation metrics, or prior keys.

## Final Counts
- Nodes: 120.
- Accepted edges: 128.
- Uncertain/removed/relabel decisions recorded: 45.

## Node Decisions
- Removed `SAFETY-TRAIN-A/B/C/D`, `125-VDC-DIVISION-A/B`, and `CTRL-RPS-INTERLOCKS`. These are printed area/reference labels, not component, bus, ground, or direct electrical endpoint nodes.
- Kept `CB-MCC-A1`; crops 05, 09, and 25 show it on the Train A MCC-A1 branch.
- Corrected diesel generator component labels from Diego `DG-2A/B/C/D` to `DG-1A/B/C/D`. Jennifer zoom crops show `DG-1*` directly under the DG symbols, while `DG-2*` is the adjacent feeder/conductor label.
- Kept named buses and grounds: `BUS-13-8A/B`, `BUS-4160-A/B/C/D`, `BUS-480-A1/A2/B1/B2/C1/C2/D1/D2`, `BUS-DC-125A/B`, and `GND-A/B/C/D`.

## Edge Decisions
- Kept Diego's direct top-source, 13.8 kV tie, 4160 normal incoming, DG breaker, and short local relay-control edges after visual review.
- Added four accepted 480 V split-bus tie edges: `BUS-480-A1--BUS-480-A2`, `BUS-480-B1--BUS-480-B2`, `BUS-480-C1--BUS-480-C2`, and `BUS-480-D1--BUS-480-D2`. Crops 05-08 and 25-28 show labeled `TIE-*12` segments with junction dots.
- Kept local lower MCC ownership edges: MCC-X1 to SI pump, CCW pump, and HVAC fan; MCC-X2 to MOV-RHR-X and dashed local PANEL-IC-X route.
- Kept local rectifier/panel/ground edges and bottom battery/DC-bus/inverter/RPS chains. `ATS-AOUT` and `ATS-BOUT` are accepted as direct named ATS-to-RPS solid routes.
- Did not promote Diego plausible long routes: relay-to-SSPS, MCC-to-ATS inputs, rectifier/panel/ground-to-DC-bus shortcuts, SSPS/RPS interlocks, and DC-bus-to-SSPS candidates remain uncertain or rejected as direct edges.

## Ambiguity Policy
Crossings without dots were not treated as taps. Printed reference-area labels were not converted into nodes. Long routes were only accepted when a named endpoint-to-endpoint path was visually clear; otherwise the candidate was preserved in `round_01_jennifer_uncertain.csv` with a reason.
