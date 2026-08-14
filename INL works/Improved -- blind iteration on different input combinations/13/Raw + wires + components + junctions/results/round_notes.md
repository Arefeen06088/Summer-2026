# Document 13 round notes

## Round 1 - Diego high recall
Diego extracted the four-train source, 4.16 kV, 480 V, MCC, DC/UPS, relay/control, and grounding graph.
He included low-confidence DG auto-start annotation nodes, JB-to-DC-bus dashed paths, and transformer-to-ground edges for Jennifer to verify.

## Round 2 - Jennifer precision
Jennifer retained the visually supported solid source, distribution, MCC, DC/UPS, relay/control, and plant-ground connections.
She normalized JB-X1/LOCAL-IO-X to JB-X1, removed text-only DG auto-start nodes, removed transformer-to-ground edges without clear terminals, and excluded JB-to-DC-bus dashed paths as uncertain.

## Round 3 - Diego saturation
Diego agreed Jennifer's corrected graph was saturated. Final matrix equals round 2.
