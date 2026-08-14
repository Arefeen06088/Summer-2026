# Diego document 10 connectivity proposal

Allowed sources used: raw schematic image, component label overlay, wire node overlay, wire mask overlay, `component_visual_ocr_labels.csv`, and the crop/contrast images in `codes/`. No ground-truth files or evaluator feedback were opened.

## Node additions and corrections

- Base component CSV has 109 component labels.
- Add 13 nodes from `diego_doc10_node_additions.csv`.
- Final proposed node count: 122 nodes.
- Existing label corrections: no strong text-label correction needed for the 109 CSV labels.
- Type correction suggested: `PT-4160-A` and `PT-4160-B` are visually potential/voltage transformer instrument nodes rather than generic `pid_instrument`.
- Important missing physical nodes: `TR-UPS-A` and `TR-UPS-B`.
- Important logical/bus nodes: `BUS-SWY-345KV`, `BUS-4160-A`, `BUS-4160-B`, `480V-LC-FEEDERS-A/B`, `BUS-DC-A/B`, `BUS-UPS-A/B`, and `CT-CAB-A/B-CONTROL-CABLE-TRAY`.

## Edge confidence summary

- Edge CSV: `diego_doc10_edges.csv`.
- Final proposed edge count: 157 undirected edges.
- High-confidence edges are visible solid-line power runs or clear taps.
- Medium-confidence edges are visually plausible dashed/dotted control or signal routes, or solid routes that pass through crop boundaries.
- Low-confidence edges are retained only for high-recall review.
- Confidence distribution: 100 high, 55 medium, 2 low.
- Kind distribution: 87 power, 10 power_candidate, 19 control, 2 control_candidate, 10 control_signal, 17 signal, 4 signal_candidate, 4 signal_tap, 4 ground.

## Uncertain retained edges

- `PNL-UPS-A -- HTR-TRACE-A` and `PNL-UPS-B -- HTR-TRACE-B`: retained as low-confidence control candidates because a dashed vertical route is near both the UPS panels and heater-trace symbols.
- `MCC-102A -- FAN-AB-A` and `MCC-102B -- FAN-AB-B`: retained as medium power candidates because the shared lower conductor visually continues toward the fan branch, though the clearer named MCC feeder is from `MCC-103A/B`.
- `480V-LC-FEEDERS-A/B -- FUSE-*` and `FUSE-A02/B02 -- DS-*01`: retained as medium candidates because the low-voltage feeder and fuse/switch cluster is tightly overdrawn.
- `480V-LC-FEEDERS-A/B -- RECT-1A/B`: retained as medium candidates because the rectifier input conductor runs into the same low-voltage train area but the immediate source label is outside the crop.
- `CT-CAB-* -- MCR/ANN/SER/JB` routes: retained as medium because the dashed/dotted control lines enter the bay and converge visually, but not all individual junction dots are explicit.

## Rejected or not modelled as connectivity nodes

- `CLASS-1E-DIV A/B 4.16 kV / 480 V / UPS`: treated as area/system titles, not conductor nodes.
- `DC/UPS TRAIN A/B`: treated as enclosure/group titles, not conductor nodes; explicit `BUS-DC-*` and `BUS-UPS-*` nodes are used instead.
- `MCR / ANNUNCIATOR CONTROL BAY`: treated as an enclosure title, not a node; edges are made to `PNL-MCR-01`, `PNL-ANN-01`, `SER-01`, and `JB-CONTROL`.
- Title block, notes, legend, grid references, and physical-separation clearway labels are not connectivity nodes.
- Wire crossings without a dot were not promoted into connections unless a named bus/logical route already supported the edge.
