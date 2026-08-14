# Document 14 round notes

## Round 1 - Diego high recall
Diego extracted the physical source, bus, branch, panel, DC/UPS, instrument, relay, load, and ground graph.
He also included artificial CTRL-* header nodes to preserve lower dashed control-bundle possibilities and used expanded CB-480A/B branch labels.

## Round 2 - Jennifer precision
Jennifer removed artificial CTRL-* nodes, removed MASTER-TB-XA1..YD2 because no individual terminal landings are clear,
pruned the implied relay-to-panel mesh through ambiguous dashed bundles, corrected 480 V breaker labels to CB-48A/B-*,
and corrected COMP-ITA-1A to COMP-IA-1A.

## Round 3 - Diego saturation
Diego agreed Jennifer's corrected graph was saturated. Final matrix equals round 2.
