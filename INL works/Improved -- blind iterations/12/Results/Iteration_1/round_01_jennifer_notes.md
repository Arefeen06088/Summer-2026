# Round 1 Jennifer Notes - Doc 12

## Scope And Sources

- Precision review used only doc 12 `Input resources`, doc 12 `Codes and artifacts` including `inspection_crops`, and Diego Round 1 files in `Results\Iteration_1`.
- I did not use ground truth, evaluator outputs, scores, validation metrics, prior answer keys, or anonymous `wire_nodes.csv` IDs as matrix nodes.
- Raw legend/rules followed: solid = power, dashed = control, dotted = signal, dash-dot = interlock; dots indicate taps/connections; crossings without dots are not connected; grounds are equipment ground reference only.

## Final Counts

- Final node count: 160.
- Final accepted edge count: 142.
- Uncertain/not accepted candidates recorded: 56.
- Node removals: 0. The named components, logical buses, and two ground reference nodes are visually present.
- Edge removals from Diego high-confidence set: 2 PT tap edges.
- Promotions from Diego plausible set: 0. The lower control/interlock/signal area stayed uncertain where named terminal evidence was not direct.

## Node And Label Decisions

- Kept logical buses exactly where the raw labels support them: `BUS-4KV-A`, `BUS-4KV-B`, `BUS-480-A`, `BUS-480-B`, `BUS-480-C`, `BUS-480-D`, `DC-BUS-A`, `DC-BUS-B`, and `BUS-120VAC-ESF`.
- Kept `MCC-1A`, `MCC-1B`, `MCC-2A`, and `MCC-2B` as physical motor-control-center bus/component nodes only; no duplicate bus aliases were added.
- Kept `GND-1` and `GND-2` as equipment ground reference nodes only.
- Diego's repeated feeder OCR corrections are visually supported in the raw load crops and retained, including `MS-F002`, `MS-F005`, `MS-F007`, `MS-F016`, `MS-F017`, `MS-F020`, `MS-F022`, `FU-F001`, `FU-F003`, `FU-F006`, `FU-F018`, `FU-F021`, `DS-F004`, `DS-F023`, `MS-F009`, `MS-F010`, `MS-F014`, `MS-F024`, `MS-F025`, `MS-F029`, `FU-F012`, `FU-F013`, `FU-F027`, and `FU-F028`.

## Accepted Connectivity

- Top power retained: generator/UAT/standby/EDG sources through named disconnects and breakers to `BUS-4KV-A`/`BUS-4KV-B`, plus `CB-TIE-1` between the two 4.16 kV buses.
- 480 V transformer feeders retained: 4.16 kV bus to breaker to transformer to `BUS-480-*`, then `BUS-480-*` to MCC breakers and the four MCC nodes.
- MCC branches retained only as direct named chains: `MCC -> CB-Fxxx -> fuse/starter/disconnect -> load`. No direct MCC-to-load shortcut edges were added.
- DC/static inverter retained: `MCC-2A/B -> CB-DC-1A/B -> CHGR-125A/B -> DC-BUS-A/B`, batteries to the DC buses, DC buses to `INV-1A/B`, inverters to `ATS-INV`, and `ATS-INV -> BUS-120VAC-ESF`.
- Ground reference retained only where visually direct: `PNL-RPS-A -> GND-1` and `PNL-RPS-B -> GND-2`.

## Removed Or Uncertain Connectivity

- Removed from accepted: `BUS-4KV-A --instrument_tap-- PT-4160A` and `BUS-4KV-B --instrument_tap-- PT-4160B`. The PT symbols and labels are visible, but the bus tap is not marked by a clear raw black connection dot; the PT nodes remain present.
- Left uncertain: top dash-dot breaker interlock spine candidates. The route is visible, but individual breaker-to-breaker logical terminations are inferred from adjacency rather than explicit terminal dots.
- Left uncertain: lower relay-to-TB, TB-to-panel, panel-to-ESFAS, annunciator/SER, 120 VAC ESF taps, ATS-to-TB, DC-bus-to-TB/panel, and relay-to-relay candidates. The raw routes are plausible, but crossings and compact terminal clusters do not show enough direct named endpoint evidence for a precision pass.
