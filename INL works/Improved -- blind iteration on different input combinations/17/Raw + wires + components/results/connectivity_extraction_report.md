# Document 17 Connectivity Extraction Report

Scope: raw schematic and visual aids only. No GT, target, answer, or GT-derived feedback was used. No off-the-shelf OCR was used; labels were read visually from the provided crops.

## Jennifer R1 Corrections

KEEP:
- `GEN-001` visibly lands on both `UAT-1A` and `UAT-1B` through solid feeders with black terminations.
- `SAT-1A/B`, `UAT-1A/B`, `DG-1A/B`, bus ties, and transformer feeder chains are visually supported.
- Dotted PT/AM/VM/CT instrument taps are retained as direct bus-to-instrument edges.
- 480 V feeder chains are retained where the solid/dashed/dotted line style visibly enters and leaves each symbol.

REMOVE:
- `PNL-DCS -> ANN-ESF-A/B` remain excluded; the nearby dashed routing does not show a clean landed junction.
- Long control-wireway continuations from UV/RPS relays remain excluded where their final labelled endpoint is not visible.

ADD:
- `PNL-ANN -> ANN-ESF-A` and `PNL-ANN -> ANN-ESF-B`; the singular `PNL-ANN` panel has a dashed horizontal run visibly landing at both annunciator boxes.

RENAME / TYPE CHANGE:
- `PNL-ANN-A` and `PNL-ANN-B` are collapsed to one node, `PNL-ANN`.
- `CIP-AIR-1A/B` are renamed to `CMP-AIR-1A/B`; magnified label crops show `CMP-AIR`.
- Line types are normalized to `P` for solid power, `GND` for solid ground branches, `CTRL` for dashed control/trip, and `INST` for dotted instrument.

## Final Counts

- Nodes: 200
- Undirected edges: 201
- Matrix ones: 402
- Duplicate undirected edges: False
- Self-loops: 0

## Remaining Uncertain Edges

These are excluded from the accepted matrix.

```csv
source,target,type,reason
CB-TR-A1,MASTER-TERMINAL-BLOCKS,CTRL,dashed route leaves breaker area but exact terminal landing is unclear
CB-TR-A2,MASTER-TERMINAL-BLOCKS,CTRL,dashed route approaches terminal block area but terminal number is unclear
CB-TR-B1,MASTER-TERMINAL-BLOCKS,CTRL,dashed route crosses top-center area but exact terminal landing is unclear
CB-TR-B2,MASTER-TERMINAL-BLOCKS,CTRL,dashed route leaves breaker area but exact terminal landing is unclear
PNL-DCS,ANN-ESF-A,CTRL,annunciation routing crosses nearby but no clear landed junction
PNL-DCS,ANN-ESF-B,CTRL,annunciation routing crosses nearby but no clear landed junction
RELAY-UV-A1,TRAIN-A-CONTROL-WIREWAY,CTRL,dashed run continues into wireway with destination not explicit
RELAY-UV-A2,TRAIN-A-CONTROL-WIREWAY,CTRL,dashed run continues into wireway with destination not explicit
RELAY-UV-B1,TRAIN-B-CONTROL-WIREWAY,CTRL,dashed run continues into wireway with destination not explicit
RELAY-UV-B2,TRAIN-B-CONTROL-WIREWAY,CTRL,dashed run continues into wireway with destination not explicit
RELAY-RPS-A,TRAIN-A-RPS-ESF-CONTROL,CTRL,side-channel run continues beyond visible labelled landing
RELAY-RPS-B,TRAIN-B-RPS-ESF-CONTROL,CTRL,side-channel run continues beyond visible labelled landing
```
