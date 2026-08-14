# Diego Round 03 Saturation Notes - Document 18

## Scope

Worked only inside the document 18 `Raw + wires + junctions + OCR` folder. I inspected Jennifer's round 02 kept/removed edge files against the raw schematic, wire mask overlay, wire-node overlay, and component/label CSV. I did not use Ground Truth, evaluator feedback, outside files, or off-the-shelf OCR.

## Saturation Decision

No changes relative to Jennifer round 02. The saturated round 03 edge set is Jennifer's 193 kept edges with round 03 action/notes added. I found no removed edge that should be restored and no missing corrected edge that should be added.

## Specific Review Points

- `BUS-SWYD-230 -> BB-SWYD-230`: agree. The raw top-left bus label reads `BB-SWYD-230`.
- `CB-SWYD-230`: agree with rejection. The top-left source breakers land directly on the `BB-SWYD-230` bus conductor/filled landing; I do not see a separate inline `CB-SWYD-230` breaker symbol.
- `BUS-GEN-TERMINAL -> GEN-MAIN-1-TERMINAL`: agree. The top-right common conductor after `CB-GEN-ISO` is a generator-terminal node tying `GEN-MAIN-1` to the UAT primary taps, not a labeled busbar.
- `CB-UAT-A -> BUS-4160B` and `CB-UAT-B -> BUS-4160B`: agree with removal. In the top-right raw/wire crop the UAT breaker lower terminals stop above the 4.16 kV busbar; no solid lower conductor or filled bus landing is visible.
- RPS relay dashed memberships: agree with removal. The relay boxes `RELAY-K101/K102/K103/K104` and `RELAY-K201/K202/K203/K204` are visibly present inside or near the dashed routing, but I do not see unambiguous landed terminals or filled junctions. The limited dashed-net model for PLC/JB/annunciator endpoints is the better precision model.

## Counts

- Saturated edges: 193
- Adds/restores relative to Jennifer round 02: 0
- Drops relative to Jennifer round 02: 0
- Renames relative to Jennifer round 02: 0
- Matrix saturated: yes

## Edge Counts By Kind

- `power_480_feeder`: 120
- `power_primary_230_4160`: 19
- `power_transformer_infeed`: 12
- `dc_control_power`: 12
- `instrumentation_control`: 10
- `rps_dashed_control`: 8
- `ac_control_power`: 6
- `grounding`: 4
- `bus_tie`: 2
