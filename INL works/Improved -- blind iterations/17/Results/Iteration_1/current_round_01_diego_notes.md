# Diego Blind Connectivity Extraction - Doc 17 Iteration 1

## Scope and Source Discipline

This extraction used only the provided input resources and input-derived artifacts under `Input resources` and `Codes and artifacts`. No ground truth, scoring, validation, evaluation, or feedback outputs were used.

## Node Decisions

- Kept the prepared inventory node order unchanged: 200 nodes from `component_inventory_doc17_current.csv`.
- Did not promote wire-node IDs (`WN-*`) into the matrix; they were used only as geometry aids.
- Did not add unlabeled routed side-channel, crossing, or generic control-lane nodes. Where a named bus existed, edges terminate at that bus; otherwise only visually named components/grounds/panels were connected.
- The visible master-terminal-block/control-lane annotation boxes were treated as routed annotation/grouping areas rather than stable matrix nodes, because the prepared inventory did not include them and their individual terminals were not named as standalone components.

## Edge Evidence by Region

- Top 4.16 kV/source region: source, transformer, diesel generator, tie-breaker, PT, and transformer-feeder edges were taken from solid vertical/horizontal conductors. Region edges: 30.
- Middle 480 V region: named bus rails connect to incoming transformer breakers, tie breaker, metering/CT taps, switchgear ground branches, and repeated load-feeder chains. Region edges: 134.
- Bottom DC/AC/control region: 480-to-DC charger feed, batteries, 125 VDC buses, DC tie, inverters, 120 VAC buses, STS outputs, panel/TB/relay wiring, annunciator and SOE paths were included. Region edges: 37.

## Uncertain / High-Recall Cases

- `GEN-001` to `UAT-1B` is visually continuous through a long top conductor, but the prepared wire-contact audit captured the left connection more cleanly; included at slightly lower confidence.
- `BUS-480-A/B` to `CB-DC-A/B` are long routed AC feeds from the 480/control area into the lower DC chargers; included with medium confidence because part of each route runs through side-channel routing.
- `STS-120-A/B` to `PNL-RPS-A/B` are dashed control/feed runs and therefore lower confidence than solid power buses, but the named endpoints are clear.
- `RELAY-ESF-A` to `REC-SOE-1` and `RELAY-ESF-B` to `REC-SOE-2` are dotted SOE/alarm-style paths; they are included for recall with explicit lower confidence.
- Long dashed side-channel routes that did not visibly terminate on another named component were not converted into pairwise component edges. Crossings without dots were not treated as junctions.

## Validation

- Edge rows written: 201.
- Matrix size: 200 x 200 with matching row/column order from the prepared inventory.
- Isolated inventory nodes after extraction: 0.
- Programmatic checks confirmed: every edge endpoint is in the node list; no self-edges; no duplicate undirected edges; matrix is symmetric; diagonal is all zero; matrix edge count matches edge CSV row count.

## Region Edge Counts

- bottom_annunciation_soe: 3
- bottom_annunciation_soe_uncertain: 2
- bottom_control_panels_A: 6
- bottom_control_panels_B: 6
- bottom_dc_ac_control_A: 9
- bottom_dc_ac_control_B: 9
- bottom_dc_ac_control_tie: 2
- middle_480_loads: 14
- middle_480_loads_A: 60
- middle_480_loads_B: 60
- top_4160_sources_tie: 18
- top_to_480_transformers: 12
