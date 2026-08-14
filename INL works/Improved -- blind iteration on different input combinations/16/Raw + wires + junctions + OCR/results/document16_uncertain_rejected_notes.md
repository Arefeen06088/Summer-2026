# Document 16 Uncertain And Rejected Notes

Scope: only resources inside the document 16 Raw + wires + junctions + OCR folder were used. The raw schematic was treated as primary evidence; overlays and crop masks were only aids. No ground truth, evaluator output, prior documents, external OCR, or off-folder resources were used.

## Included With Low Confidence

- 480 V breaker trip/control associations from dashed fail-safe wiring were included as `control_trip` edges where a dashed vertical/control path visibly descends from breaker areas toward lower control panels. These are plausible trip/control associations, not power continuity.
- `BUS-480-B` was added as a logical bus even though the text label is not as legible as `BUS-480-A`; the lower horizontal 480 V bus geometry and B-side feeder junction dots make it visually/geometrically plausible.
- `BUS-480-B -> TR-RPS-B` was included with medium confidence because the vertical source path to `TR-RPS-B` is congested by B MCC branch geometry.
- Instrument/control taps involving `MG-RPS-A -> FT-AFW101`, `MG-RPS-B -> RTD-RCS101`, `RTD-RCS101 -> BUS-120-RPS-B`, `JB-CONTAIN -> XS-DOOR101`, and `UCP-01 -> BUS-120-RPS-B` were included at low confidence because the visible dotted/vertical paths share conductors or crop-edge continuations.

## Rejected Or Not Connected

- Wire crossings without a filled dot were not made into connectivity edges. Important examples: `TR-4KV-480A` visually crosses the lower 4 kV bus while dropping from `BUS-4KV-A`; `GEN-EDG-B` crosses the upper 4 kV bus while feeding `CB-EDG-B`; `CB-480B-IN` crosses the upper 480 V bus before landing on the lower 480 V bus.
- `PP-E1-480-125R` was rejected as a title-block/drawing-number artifact. It appears in the title block rather than on a wired schematic device.
- Dashed rectangular boundaries around selected load/control areas were not treated as electrical connections.
- Repeated grid/page border ticks and title-block fields were ignored as non-connectivity graphics.

## Modeling Choices

- MCC labels such as `MCC-11A`, `MCC-12A`, `MCC-21A`, `MCC-31A`, `MCC-11B`, `MCC-12B`, `MCC-21B`, and `MCC-31B` were treated as busbar components. Edges were captured from the 480 V feeder breaker into the MCC and from the MCC busbar down to each branch breaker.
- Relay-to-breaker relationships were captured as `relay_association` edges when the relay/contact symbol sits on the same vertical feeder beneath the branch breaker and shares the suffix/load name.
- Individual grounds were kept separate (`GND-P201A`, `GND-P211A`, etc.) rather than merged into a common ground node, because the drawing labels them individually.
