# Round 01 Diego Extraction Notes

## Scope

Used only the allowed raw/input resources and the fresh current aids/crops for Improved doc 39 Iteration_1. The raw schematic PNG was treated as authoritative; OCR labels wire masks wire-node overlays and crops were used only to find and cross-check visual features.

## Kept final node classes

- Named physical components: offsite sources disconnects transformers breakers diesel generators chargers batteries inverters panels RPS panels MCCs relays pumps MOVs junction boxes annunciator recorder and plant ground.
- Explicit named buses/logical nodes: BUS-4160-A-DIV-I BUS-4160-B-DIV-II BUS-480-A BUS-480-B LC-A LC-B and CONTROL-ROOM-ANNUNCIATION.
- Ground: GND-PLANT is kept because a raw ground-reference symbol is visibly tied to the right end of BUS-480-A.

## Excluded annotation-like labels

- DIVISION-I-TRAIN-A-SAFETY-POWER and DIVISION-II-TRAIN-B-SAFETY-POWER are section headings/boundaries rather than electrical nodes.
- NORMAL-OFFSITE-FEED-A and NORMAL-OFFSITE-FEED-B are descriptive feed notes below the 4160 buses and were not included as nodes.
- N.O. TIE is an operating annotation above CB-TIE-AB rather than a separate node. The electrical tie is represented through CB-TIE-AB.
- WIRE-NODE-* points from the derived wire aid were not used as final matrix nodes.
- Terminal schedule labels such as DC-A were treated as raw-image supporting evidence only and were not promoted to nodes without a clear named conductor in the geometry.

## Modeling choices

- Solid power paths are represented through intervening named components. For example offsite A reaches BUS-4160-A-DIV-I through DS-230A TR-1A and CB-1A; the A/B bus tie is through CB-TIE-AB.
- The 4160-to-480 paths are represented through TR-480-A or TR-480-B and the corresponding 480 breaker.
- CONTROL-ROOM-ANNUNCIATION is modeled as a named logical control bus. JB-A101 ANN-CR01 REC-SOE01 and JB-B101 are kept as taps on that logical node rather than forcing every long dashed segment into direct component-to-component edges.
- LC-A and LC-B are kept as named conductor labels at the ends of the 480 buses. Direct inverter-to-LC ownership is visually plausible but not certain so those edges are uncertain only.

## Uncertainty highlights

- Long dashed routes from RPS-A and RPS-B toward the lower perimeter/control-room route are visible but ambiguous over long distances. These are recorded as uncertain edges and excluded from the matrix.
- Direct dashed component-to-component chain edges among JB-A101 ANN-CR01 REC-SOE01 and JB-B101 are recorded as uncertain because the kept graph uses the named CONTROL-ROOM-ANNUNCIATION bus as the final node.
- The A-side relay KA1 sits near solid load routing from MCC-A1 but a direct MCC-A1-to-RELAY-KA1 terminal is not visually certain.
- BUS-480-B to GND-PLANT is marked remove; the raw ground-reference symbol is drawn on the A-side bus end and no clear B-side ground tie is visible.
