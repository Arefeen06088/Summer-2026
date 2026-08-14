# Document 15 Round Notes

## Diego Round 1 - High Recall

Diego identified the 183-node schema matching the raw note block. He included offsite source chains, all division feeder and MCC load chains, relay/control/DC wiring, AB/CD tie paths, and high-recall same-division NF/DG dashed control edges. He left DG-to-NSS bus contacts uncertain.

## Jennifer Round 1 - Precision

Jennifer supported all 183 nodes, promoted DG-to-NSS contacts to hard, and kept the same-division NF/DG dashed interlocks hard. This produced an over-broad hard set relative to the raw 190-connection sanity note.

## Diego Round 2 - Saturation Check

Diego kept `RLY-*06 -- TB-1*` and `CP-1* -- JB-1*` as hard visual doglegs, but moved `BUS-NSS -- DG` and `CB-NF -- CB-DG` same-division dashed edges to uncertain.

## Jennifer Round 2 - Final

Jennifer accepted Diego Round 2. Final graph: 183 nodes, 190 hard edges, 8 uncertain edges.
