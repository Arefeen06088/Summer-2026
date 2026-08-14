# Diego Extraction Notes - Doc 27 / Iteration 1 / Round 01

## Scope Statement
Inspected only the allowed Doc 27 resources under `Input resources` and the derived/crop artifacts already present under `Codes and artifacts`, with the raw schematic as primary evidence. No ground truth, GT-derived evaluator output, score feedback, or resources from any other document/iteration were used.

## Node List Rationale
- Matrix node count: 200.
- Component inventory nodes were retained when the component was raw-visible and named. The derived `TE-41` entry was excluded after raw inspection because the apparent detection corresponds to the printed `CB-TIE-41` breaker label, not a distinct visible instrument symbol/termination.
- Added raw-visible logical bus/conductor nodes: `BUS-13KV-N`, `BUS-4160-A`, `BUS-4160-B`, `BUS-480-A`, `BUS-480-B`, `BUS-480-C`, `BUS-480-D`, `DC-BUS-125A`, and `DC-BUS-125B`.
- Added raw-visible nodes beyond the component inventory: `PANEL-CTRL-MAIN` and `GND-EQ-B`. `GND-EQ-A` was already in inventory; `GND-EQ-B` is visible in the bottom/right raw crop.
- Section titles and feeder-family text such as load-center names and feeder descriptions were not used as matrix nodes unless they named an actual conductor bus or component.
- Intermediate wire-node IDs (`WN-*`) were not included because they are derived geometry points, not raw-named logical nodes/components.

## Edge Evidence by Schematic Region

### Top 13 kV Source Bus
- The normal/emergency source chain is represented as `GRID-345 -> DS-101 -> CB-101 -> BUS-13KV-N`.
- Generator taps are represented as `GEN-G1 -> CB-G1 -> BUS-13KV-N` and `GEN-G2 -> CB-G2 -> BUS-13KV-N`.
- Main transformer source chains are represented as `BUS-13KV-N -> TR-1A -> CB-4A-IN -> BUS-4160-A` and `BUS-13KV-N -> TR-1B -> CB-4B-IN -> BUS-4160-B`.

### 4.16 kV Buses, Diesel Sources, and Tie
- Diesel sources are represented as `DG-1A -> CB-DG1A -> BUS-4160-A` and `DG-1B -> CB-DG1B -> BUS-4160-B`.
- The tie is represented through the breaker only: `BUS-4160-A -> CB-TIE-41 -> BUS-4160-B`; no direct `BUS-4160-A` to `BUS-4160-B` shortcut was added.
- 480 V transformer feeds are represented as direct visible taps from `BUS-4160-A` to `TR-480-A`/`TR-480-C`, and from `BUS-4160-B` to `TR-480-B`/`TR-480-D`, then through their incoming breakers to the four 480 V buses.

### 480 V Load Centers
- `TR-480-A -> CB-480A-IN -> BUS-480-A`; `TR-480-B -> CB-480B-IN -> BUS-480-B`; `TR-480-C -> CB-480C-IN -> BUS-480-C`; `TR-480-D -> CB-480D-IN -> BUS-480-D`.
- Feeder breakers are connected only to their own load-center bus and their own downstream device; the bus bars were not clique-expanded across all devices.

### Train A/B Feeders
- A and B columns use the visible repeated chain: bus -> feeder breaker -> disconnect/fuse -> load/panel/MCC/junction -> named dashed endpoint where visibly terminated.
- Examples: `BUS-480-A -> CB-A01 -> DS-A01 -> PMP-A01 -> RLY-A01`; `BUS-480-A -> CB-A02 -> FU-A02 -> MOV-A02 -> LS-A02`; `BUS-480-B -> CB-B08 -> FU-B08 -> PMP-B08 -> PT-B08`.
- A/B feeder 10 branches were treated as the visible chain through `DS-A10`/`DS-B10` to `JB-A10`/`JB-B10` and `LT-A10`/`LT-B10`, with additional DC-center tap adjacencies where visible/plausible.

### Train C/D Feeders
- C/D columns use the visible repeated chain: bus -> feeder breaker -> disconnect/fuse -> load/panel/MCC/junction -> named dashed endpoint where visibly terminated.
- Examples: `BUS-480-C -> CB-C01 -> DS-C01 -> MOV-C01 -> RLY-C01`; `BUS-480-C -> CB-C05 -> FU-C05 -> INST-C05 -> JB-C05`; `BUS-480-D -> CB-D07 -> DS-D07 -> MCC-D07 -> TB-D07`.

### DC Center and Grounds
- The raw-visible DC bus labels `DC-BUS-125A` and `DC-BUS-125B` were included. Charger/battery/direct tap adjacencies were added for `CHGR-125A`, `BAT-125A`, `CHGR-125B`, `BAT-125B`, `JB-A10`, and `PANEL-CTRL-MAIN` where the raw schematic shows the horizontal DC bus and local vertical/dashed terminations.
- `DC-BUS-125A -- DC-BUS-125B` was included because the raw crop shows the labeled DC bus segments as a continuous horizontal conductor; see ambiguity note below.
- `GND-EQ-A -- BUS-480-C` and `GND-EQ-B -- BUS-480-D` were included because both grounds are raw-visible and have direct dashed conductors terminating at the lower 480 V bus regions.

## Ambiguous / Conservative Cases
- `TE-41`: excluded. The raw zoom shows only the `CB-TIE-41` breaker symbol and label; the derived `TE-41` appears to be a false split/partial OCR artifact rather than a separate connected instrument.
- DC center: the charger/battery area uses dotted enclosure boundaries and compact overlapping branch geometry. I included direct named tap adjacencies (`CHGR-*`, `BAT-*`, `JB-A10`, `PANEL-CTRL-MAIN`) but did not convert the dotted enclosure itself into a connectivity node.
- `DC-BUS-125A`/`DC-BUS-125B`: included a direct edge because the raw line appears continuous; if the labels are intended as separated logical buses rather than one continuous conductor, this is the highest-risk DC-center edge.
- Dashed control/instrument routes below loads were included only where a named component endpoint is visibly aligned and terminated under the associated load; no free-floating dashed routes or section-title text were promoted to nodes.

## Output Summary
- Nodes: 200
- Edges: 203
- Raw-visible nodes added beyond inventory: BUS-13KV-N, BUS-4160-A, BUS-4160-B, BUS-480-A, BUS-480-B, BUS-480-C, BUS-480-D, DC-BUS-125A, DC-BUS-125B, PANEL-CTRL-MAIN, GND-EQ-B
