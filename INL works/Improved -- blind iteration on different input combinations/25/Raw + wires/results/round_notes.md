# Document 25 Connectivity Extraction Notes

Generated: 2026-07-18T13:16:32

Allowed inputs only: files under `Raw + wires`. No GT or GT-derived feedback was used. No off-the-shelf OCR engine was used; labels were read by visual inspection.

## Round Summary

- Round 01 Diego high-recall: 205 accepted candidate edges. Included A/B first-feeder starter label swaps and did not include the later 208th trip-coil tie.
- Round 02 Jennifer precision review: 207 edges. Corrected `MS-A01/MS-A02` and `MS-B01/MS-B02`, accepted `INV-120-1A -- RELAY-K501A` and `INV-120-1A -- BUS-125DC-B`, rejected unsupported lane/crossing edges.
- Round 03 Diego saturation acceptance: 207 edges, agreed with Jennifer's corrections.
- Round 04 Jennifer saturation confirmation: 207 edges.
- Round 05 Diego count recheck: 208 edges after focused raw crop showed `PNL A/B TIE -- TC-52-4A`.
- Round 06 Jennifer final: accepted `PNL A/B TIE -- TC-52-4A`; final matrix saturated at 208 visible connections.

## Final Matrix Rule

The binary matrix sets `1` for every accepted `solid`, `dashed`, `dotted`, or `ground` connection; it sets `0` for rejected/uncertain/non-edge pairs. The diagonal is `0`.

## Final Edge Count

Final unique undirected accepted edges: 208.
The raw drawing count strip reads `200 components / 208 connections`, and the final edge count matches 208.

## Naming Notes

The final CSVs use visible component tags. For panel-shaped symbols with `PNL` inside the symbol but a separate tag label, the tag is used directly, for example `LC-480-A03` and `CP-CTRL-A08`. `PNL-P1-601A/B/C` is retained as reviewed by Jennifer despite small-font ambiguity with `PI`.
