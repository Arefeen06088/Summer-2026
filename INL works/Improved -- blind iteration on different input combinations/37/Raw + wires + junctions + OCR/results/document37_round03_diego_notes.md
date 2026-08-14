# Document 37 Round 03 Diego Notes

Scope: saturation review only. I used only resources inside the allowed document 37 folder: raw schematic, provided overlays, wire/component CSV aids, precision review crops, and the prior round01/round02 result files. I did not use Ground Truth, evaluator output, GT-derived feedback, off-the-shelf OCR, or data outside the allowed folder. The raw schematic remains authoritative.

## Round 03 Decision

I agree with Jennifer round02. Round03 carries forward Jennifer's 55-node, 54-edge graph unchanged:

- Nodes: unchanged from Diego round01 and Jennifer round02, with 47 physical components and 8 visible logical bus nodes.
- Edges: unchanged from Jennifer round02, with Diego round01's two low-confidence lower dashed edges removed.
- No new nodes or edges were added.

## Disputed Lower Dashed Routes

Removed and still not restored:

- `PAN-RPS-A -- PLC-ESF`
- `PLC-ESF -- PAN-RPS-B`

Reinspection of `raw__row3_col2.png`, `raw__bottom_band.png`, `raw__bottom_left.png`, `raw__bottom_right.png`, `wires__row3_col2.png`, and `nodes__row3_col2.png` shows that C03 and C06 are dashed functional cable-tray/routing paths rather than clear component-to-component terminals.

C03 visibly forms a dashed box/path around the lower RPS A / instrument rack A area and extends toward the central ESF/RPS distribution region, but it does not terminate cleanly on both `PAN-RPS-A` and `PLC-ESF`. The dashed route touches/runs near panel boundaries and partition/routing lines without a filled junction or unambiguous endpoint pair.

C06 similarly forms a dashed routing path between the central ESF area and the lower RPS B area, but the raw drawing does not show a clean terminal on both `PLC-ESF` and `PAN-RPS-B`. The nearby note "CABLE TRAY ROUTING SHOWN FUNCTIONALLY; TERMINAL NUMBERS TYPICAL" reinforces treating this as functional routing context, not matrix connectivity.

No specific dashed edge among `PAN-RPS-A`, `INST-RACK-A`, `PLC-ESF`, `PAN-RPS-B`, or `INST-RACK-B` is visually strong enough to include beyond the solid 120 VAC feeds already retained.

## Other Saturation Checks

- C01/C04: retained. `ATS-1A -- RELAY-K12A` and `RELAY-K12B -- ATS-1B` are clear dashed ATS permissive control lines with visible component-to-component runs.
- C02/C05: not included. The center vertical dashed lines near the batteries/central partition do not clearly terminate on labeled physical components.
- Top/source path: retained as `AUX-TR-1A -- CB-101 -- GRID-345 -- CB-102 -- AUX-TR-1B`, transformer taps to `BUS-6KA`/`BUS-6KB`, and `BUS-6KA -- CB-TIE-6K -- BUS-6KB`. No direct `GRID-345 -- CB-TIE-6K` edge is visible.
- Lower AC/DC paths: retained where solid conductors and filled bus taps support them: 480 V bus to MCC/chargers, chargers/batteries/grounds/inverters to DC buses, inverters to 120 VAC buses, and 120 VAC buses to RPS panels/instrument racks.
- No-connect crossings: no edge was inferred from line crossings without a filled dot or clear terminal endpoint.

## Saturation Outcome

Round03 is saturated at 55 nodes and 54 included undirected edges under the visual evidence standard. The only round01 removals remain removed because the lower dashed C03/C06 routes are not sufficiently terminal-specific for graph connectivity.
