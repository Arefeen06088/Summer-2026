# Round 2 Jennifer Precision Review

Jennifer tightened Diego's high-recall graph by removing tap/status pseudo-nodes and low-confidence dashed ESF trunk edges.

## Removed Standalone Nodes

SU-A, EDG-A, SU-B, EDG-B, LC-A1, LC-A2, LC-B1, LC-B2, RPS-LOCKOUT, RPS-TRIP, MOV-A, MOV-B, ESF-A-CONTROL-TRUNK, ESF-B-CONTROL-TRUNK

## Normalizations

- Kept `CB-4K-TIE`; visually it reads as `CB-4K-TIE`, not `CB-4K-1E`.
- Treated `TIE OPEN` and `RPS LOCKOUT` as state annotations, not nodes.
- Folded generic `MOV` actuator boxes into `VALVE-MOV-A` and `VALVE-MOV-B`.
- Treated `SU-*`, `EDG-*`, and `LC-*` labels as tap evidence, not nodes.

## Corrected Edge Count

55

## Corrected Edge List

See round_02_jennifer_edges.csv.

## Uncertain / Excluded

See uncertain_or_excluded_edges.csv.
