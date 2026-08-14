# Round 1 Diego Notes

## Scope

Inspected only doc 14 Input resources and the generated doc 14 crops/artifacts named in the prompt. I did not open or use ground truth, evaluator files, metrics, prior answers, or any connectivity matrix.

## Node Policy

- Started from `component_visual_ocr_labels.csv` / `component_labels_list.csv` for the 166 detected physical component labels.
- Added visually supported labels that were visible in the raw/crop images but missing from the component CSV: `PANEL-MCR`, `PANEL-ANN`, `INV-120B`, and `FS-B03`.
- Added named buses from the raw schematic: `BUS-4A`, `BUS-4B`, `BUS-480A`, `BUS-480B`, `BUS-125DCA`, `BUS-125DCB`, `BUS-UPS-A`, and `BUS-UPS-B`.
- Included `MASTER-TERMINAL-BLOCKS` as a named logical/terminal group because the bottom-left table is labeled, but I did not create high-confidence edges to the individual XA/XB/XC/YD cells because no external wire termination is visually supported.
- Did not create `WN-*` wire-node points or cable callout nodes such as `C-48A-03-P`; these are routing/cable labels, not named connectivity nodes for this round.
- Kept each labeled ground (`GND-A01`, `GND-B08`, etc.) as its own node. I did not collapse them into a single global ground because the raw schematic labels each ground symbol separately.

## Edge Policy

High-confidence edges contain visually direct connectivity:

- solid power/feeder chains from sources to buses, buses through breakers/disconnects/protection devices to loads, and loads to labeled grounds;
- named bus ties through `CB-TIE-4KV`, `CB-480-TIE`, and `CB-DG-TIE` where a continuous tie conductor is drawn;
- direct single-segment instrument stubs from terminal blocks to nearby instruments;
- direct relay/contact stubs from branch relays to their associated breakers where the relay label and dashed control contact are adjacent to the breaker.

Plausible edges contain visually supported but non-unique dashed control/panel associations. The lower panel regions have several shared horizontal dashed conductors, vertical dashed runs, and crossings. Because the raw notes say crossings without junction dots are not electrical junctions and the shared dashed paths are dense, I placed panel-to-relay and central tie-panel relationships in the plausible file instead of forcing them into high confidence.

## Bus And Ground Choices

- `BUS-4A` and `BUS-4B` are the heavy 4.16 kV Train A/B safety distribution buses in the upper third of the drawing.
- `BUS-480A` and `BUS-480B` are the heavy 480 V load center/MCC buses in the middle of the drawing, each fed from the respective 4.16 kV bus through `TR-480A/B`.
- `BUS-125DCA` and `BUS-125DCB` are the heavy 125 VDC buses in the lower DC/UPS sections.
- `BUS-UPS-A` and `BUS-UPS-B` are the lower UPS buses fed by `INV-120A` and the visually added `INV-120B` respectively.
- All labeled ground symbols remain separate ground nodes.

## Difficult Regions

- The A-side and B-side panel rows (`PANEL-ESF-*`, `PANEL-RPS-*`, `PANEL-LS-*`, `PANEL-MCR`, `PANEL-ANN`) are connected by dense dashed control wiring. The exact panel endpoint for each branch relay/control run is not always unique, especially where dashed conductors share long horizontal runs.
- `PANEL-MCR` and `PANEL-ANN` are visible near the center but partly clipped across the existing crops; their dashed conductors plausibly relate to tie-control/annunciation, but exact breaker endpoints are uncertain.
- The 125 VDC tie region around `CB-DG-TIE` has both solid tie-feeder geometry and nearby dashed control conductors. Solid bus-to-breaker-to-bus edges are high confidence; dashed relations to panels/UPS-level conductors are plausible only.
- `MASTER-TERMINAL-BLOCKS` is visibly labeled at the bottom-left, but no direct conductor from `BUS-UPS-A` into the individual terminal cells is visible in the raw/crops.

## Counts

- Nodes written: 179
- High-confidence edges written: 172
- Plausible/uncertain edges written: 26
