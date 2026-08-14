# Document 37 Round 01 Diego Notes

Scope used only the allowed document 37 folder resources: raw image overlays wire nodes component label CSV and precision review crops. No Ground Truth evaluator output or off-the-shelf OCR was used.

## Extraction Summary

- Included all 47 physical components from `component_visual_ocr_labels.csv` using the visible `label` text exactly.
- Added 8 logical bus nodes where labeled busbars are visible and useful for many-to-one connectivity: `BUS-6KA` `BUS-6KB` `BUS-480A` `BUS-480B` `BUS-125DCA` `BUS-125DCB` `BUS-120A` `BUS-120B`.
- Solid conductors are represented as `power_feeder` except the 6.9 kV tie through `CB-TIE-6K` which is `bus_tie` and the DC reference symbols which are `ground`.
- Dashed ATS permissive lines C01 and C04 are represented as `control_interlock`.
- Dashed lower RPS/PLC functional cable routes C03 and C06 are included as low-confidence `control_interlock` edges because they visibly terminate at component boundaries but do not show filled junction dots at crossings.

## Assumptions

- Long horizontal labeled busbars are logical nodes and all filled-dot taps on them connect to that bus node.
- Visual crossings without a filled dot were not treated as connectivity.
- Dashed train boundary boxes and title-block lines were ignored as non-connectivity even where the wire mask highlighted them.
- `CB-TIE-6K` is represented as a two-edge bus tie: `BUS-6KA -- CB-TIE-6K -- BUS-6KB`.
- MCC internal bus wiring is collapsed to one edge from each MCC to each visibly fed load.

## Ambiguities

- C03 and C06 are functional dashed cable tray routes rather than solid conductors. They were included at low confidence as panel-to-PLC control interlocks.
- Dashed vertical lines near C02 and C05 pass through the center area but do not clearly terminate on labeled physical components. They were not included.
- No direct edge was added from `GRID-345` to `CB-TIE-6K` because the raw top crop shows no explicit conductor from the source circle to the tie breaker.
