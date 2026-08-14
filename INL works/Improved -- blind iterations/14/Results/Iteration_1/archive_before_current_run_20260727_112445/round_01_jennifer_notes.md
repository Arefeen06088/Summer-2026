# Round 1 Jennifer Notes

## Scope

Inspected only doc 14 resources and generated doc 14 artifacts/crops under the paths named in the prompt. I did not use ground truth, evaluator files, metrics, prior answers outside this doc, or files outside the doc 14 resource/artifact/results folders.

## Node Refinement

- Kept the visually supported physical component inventory nodes from Diego's file.
- Kept the visually supported named components Diego added from the raw/crops: `PANEL-MCR`, `PANEL-ANN`, `INV-120B`, and `FS-B03`.
- Kept the major named buses: `BUS-4A`, `BUS-4B`, `BUS-480A`, `BUS-480B`, `BUS-125DCA`, `BUS-125DCB`, `BUS-UPS-A`, and `BUS-UPS-B`.
- Kept the individually labeled grounds as separate ground nodes because the drawing labels each ground symbol separately.
- Removed `MASTER-TERMINAL-BLOCKS`. The bottom-left item is a labeled table/cell row; I did not see a direct external wire landing on named terminal cells, so it is not a supported connectivity node for this pass.
- Did not add anonymous wire-node/intermediate points or cable callout nodes.

## Accepted Edge Policy

Accepted edges are limited to visually direct connectivity in the raw schematic/crops:

- solid power/feeder chains from sources through transformers/breakers to named buses;
- solid bus ties through `CB-TIE-4KV`, `CB-480-TIE`, and `CB-DG-TIE`;
- solid branch feeder chains from buses through breaker/disconnect/protection/terminal/load to labeled grounds;
- local dotted instrument stubs from terminal blocks to nearby instruments;
- short local relay/control stubs where a relay label/contact is drawn immediately adjacent to a specific breaker;
- DC/UPS solid feeder paths through chargers, batteries, inverters, and UPS buses.

I kept `BUS-480A -> PANEL-RPS-A -> CHG-125A` accepted because the raw lower-left crop shows a solid feeder entering/continuing through the `PANEL-RPS-A` box before landing on `CHG-125A`. I did not generalize that into other panel feeder edges.

## Uncertain / Not Accepted

All Diego plausible edges were written to `round_01_jennifer_uncertain.csv` rather than accepted. The shared dashed control corridors in the panel rows are visually present, but the exact endpoint is not unique enough to accept because crossings without junction dots are not connections.

Specific uncertainty classes:

- `PANEL-ESF-A`, `PANEL-RPS-A`, `PANEL-LS-A`, `PANEL-LS-B`, `PANEL-RPS-B`, `PANEL-ESF-B`, `PANEL-MCR`, and `PANEL-ANN` dashed panel/control associations remain uncertain.
- Panel-to-panel candidates remain uncertain because visible routing is shared corridor wiring, not a clear terminal-to-terminal connection.
- Panel-to-relay candidates remain uncertain even where the dashed run approaches the relay area; the local relay-to-breaker stub is accepted, but the longer panel source path is not uniquely proven.
- `PANEL-MCR`/`PANEL-ANN` tie-control candidates to `CB-480-TIE` and `CB-DG-TIE` remain uncertain.
- `CB-DG-TIE` to `BUS-UPS-A` / `BUS-UPS-B` remains uncertain because the visible route is dashed control near the UPS bus level, not a direct solid feeder landing.

## Counts

- Jennifer nodes: 178
- Jennifer accepted edges: 172
- Jennifer uncertain edges: 26

This is a precision refinement for Diego review, not a final graph.
