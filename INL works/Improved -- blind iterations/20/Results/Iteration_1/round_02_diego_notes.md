# Round 02 Diego Saturation Notes

## Scope

Reviewed only doc 20 input resources/artifacts and the round outputs derived from those resources. No GT, evaluator output, metric feedback, WN-* node IDs, or outside folders were used.

## Decision

I agree with Jennifer's round 01 precision review and copied her matrix exactly to `round_02_diego_matrix.csv`.

## Saturation Review Findings

- Node policy remains intact: 190 physical component labels plus 10 printed logical bus nodes.
- No new nodes were added.
- No nodes were removed.
- No Diego round 01 edges were removed.
- Jennifer's two added edges are visually supported and should remain:
  - `BUS-480-A -- RECT-125A`
  - `BUS-480-C -- RECT-125B`

## Evidence for Added Edges

- In the A/B load-center crop and full raw overview, `RECT-125A` has a solid vertical AC-side feed rising to the 480 V load center A bus. This supports `BUS-480-A -- RECT-125A` in addition to the dashed DC/control chain from `RECT-125A` down to `BUS-125DCA`.
- In the C/D load-center crop and full raw overview, `RECT-125B` has the analogous solid vertical AC-side feed rising to the 480 V load center C bus. This supports `BUS-480-C -- RECT-125B` in addition to the dashed DC/control chain from `RECT-125B` down to `BUS-125DCB`.
- The wire-node overlay also marks junction/trace continuity at these rectifier AC feed paths, but the raw schematic was treated as the primary evidence.

## Uncertain Candidates

- I did not identify further visually supported saturation additions beyond Jennifer's two AC-feed edges.
- I kept out direct cliques across printed buses, unlabeled intermediate junctions, WN-* IDs, section headings, dashed boundary-box artifacts, and unclear inverter AC-side upstream edges.
- I kept the existing high-recall dashed/interlock edges from round 01, including the long `RELAY-K106 -- RELAY-K108` ESF interlock.

## Diff and Hash Comparison

- Compared to Diego round 01, Jennifer/Diego round 02 has the same labels, +2 edges, -0 edges.
- Added edges versus Diego round 01: `BUS-480-A -- RECT-125A`, `BUS-480-C -- RECT-125B`.
- SHA256 `round_01_jennifer_matrix.csv`: `2B36DE472CDEAA23D9611AD652141B123342D00BB6B2A0760C0C3F80FEDF8ACA`
- SHA256 `round_02_diego_matrix.csv`: `2B36DE472CDEAA23D9611AD652141B123342D00BB6B2A0760C0C3F80FEDF8ACA`
- Hashes match: yes, matrix copied exactly.

## Validation Summary

- Node count: 200
- Edge count: 202
- Matrix is symmetric: yes
- Matrix diagonal is zero: yes
- Row and column labels are identical and in the same order: yes
