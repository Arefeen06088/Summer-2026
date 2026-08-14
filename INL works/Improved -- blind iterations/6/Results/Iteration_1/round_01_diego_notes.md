# Round 01 Diego Notes - Improved doc 6 / Iteration_1

## Scope and inputs

Blind extraction was performed from the listed raw schematic and input-derived aids only. The raw image was treated as authoritative; wire masks, wire-node overlays, and crop files were used only to confirm geometry. No GT, scoring, evaluation, previous Results files, or Results archives were opened.

## Included node classes

- Included all 100 named component labels from `component_labels_list_improved.csv`.
- Added explicitly visible labeled buses: `SWYD-BUS-A`, `SWYD-BUS-B`, `BUS-6KV-A`, `BUS-6KV-B`, and `BUS-6KV-N`.
- Included ground nodes `GND-A`, `GND-B`, and `GND-MAIN` from the component label list and connected their visible dotted ground-bond conductors.
- Excluded anonymous intermediate wire points such as `WN-*`; those were used only as geometry aids and are not final graph nodes.

## Evidence logic

- Solid power feeders on the raw schematic were treated as high-confidence direct edges, especially generator/switchyard, 6 kV bus, 480 V load center, MCC, DC/UPS, and heater/load paths.
- Explicit labeled buses were modeled as graph nodes, so devices landing on a common labeled bus connect to the bus node rather than being expanded into all-to-all device edges.
- Dashed control/interlock and sensing/instrument lines were included when they visibly terminated at a named component port or consistently routed between a named field component and a named control-bay device.
- Dotted grounding conductors were included as ground-bond edges to the named ground nodes.

## High-risk or uncertain inclusions

- `TR-UAT-202` to `CB-UAT-2` is a long routed feeder with visual congestion, so it is included at medium confidence.
- `BUS-6KV-N` is included because the central lower bus label is visible on the raw/wire-node crop; the label is small, so its exact glyph read is called out as a bus-label risk.
- Control-bay cross-train relay links (`RELAY-UV-A/B`, `RELAY-SI-A/B`, `RELAY-LOAD-A/B`, `RELAY-DG-A/B`) are lower confidence because multiple dashed returns and visual crossings overlap.
- Field-to-control edges from SI/load/DG relays to pumps, MOVs, fans, EDGs, and ATS/breakers are high-recall inclusions from dashed routing; several have confidence below 0.75 where terminal ownership is visually congested.
- `PNL-DC-A/B` ground edges are lower confidence than battery/rectifier ground edges because the dotted conductor passes through the panel/rectifier area and the exact landing device is visually close.

## Output summary

- Node count: 105
- Edge count: 153
- Isolated named nodes after extraction: none
- Matrix is symmetric with a zero diagonal, validated in `round_01_diego_validation.json`.
