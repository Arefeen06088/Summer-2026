# Round 02 Diego Notes

## Scope
Focused re-extraction used only doc 11 input resources, generated crops/artifacts, inspection crops, and Round 1 files in `Results\Iteration_1`. No ground truth, evaluator output, scores, metrics, or answer keys were used.

## Node Decision
Jennifer's 120-node policy stands. I kept the physical components, named buses, and named grounds/reference symbols; I did not restore printed reference-area nodes (`SAFETY-TRAIN-*`, `125-VDC-DIVISION-*`, or `CTRL-RPS-INTERLOCKS`). I agree with the diesel relabel from `DG-2A/B/C/D` to raw-visible `DG-1A/B/C/D`, and I agree with keeping the recovered raw-visible `CB-MCC-A1` breaker node.

## Edge Changes From Jennifer Round 1
I kept Jennifer's 128 accepted edges and promoted four direct I/C-panel-to-DC-bus branches:

- `PANEL-IC-A -- BUS-DC-125A`
- `PANEL-IC-B -- BUS-DC-125B`
- `PANEL-IC-C -- BUS-DC-125B`
- `PANEL-IC-D -- BUS-DC-125B`

These are represented from the named I/C panels to the named DC buses because the focused crops show DC-A125/B125/C125/D125 conductors leaving the panel/rectifier branches and landing on lower DC-bus junction dots. I did not add `RECT-125-* -- BUS-DC-*` skip edges because the I/C panel is the intervening named endpoint, and I did not add `GND-* -- BUS-DC-*` because the ground symbol is on a separate ground/reference conductor from the DC bus branch.

## Bus Ties
The four 480 V split-bus tie edges remain accepted: `BUS-480-A1--BUS-480-A2`, `BUS-480-B1--BUS-480-B2`, `BUS-480-C1--BUS-480-C2`, and `BUS-480-D1--BUS-480-D2`. Crops 05-08 and 25-28 show the `TIE-*12` locations with visible bus dots. I did not add any other direct bus-to-bus edges beyond Jennifer's accepted set.

## Remaining Uncertain Hotspots
The `MCC-A1/C1 -> ATS-480-A` and `MCC-B1/D1 -> ATS-480-B` candidates remain unpromoted: the ATS-A1/B1/C1/D1 labels are visible, but the routes are long, crossing-heavy, and not clean direct matrix edges. SSPS-to-RPS, SSPS-to-ATS, DC-bus-to-SSPS, and relay-to-SSPS dashed routes also remain unpromoted because the focused crops do not show clean named endpoint terminations at both ends. Crossings without dots were not treated as taps.
