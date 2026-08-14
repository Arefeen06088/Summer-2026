# Round 01 Jennifer Precision Review Notes

Scope and evidence rules: I used only doc 23 input resources and doc 23 input-derived Codes/artifacts/Results. I did not use ground truth, evaluator output, metric feedback, or anything derived from ground truth. The raw schematic remained the primary evidence; overlays, wire-node views, component labels, masks, and temporary zoom crops were used only as aids.

## Node List Decision

Accepted Diego's node list unchanged.

- Node count remains 200: 184 detected physical components, raw-visible added physical component `DC-DC-1`, and 15 printed bus nodes.
- `DC-DC-1` is visible in the lower control/24 VDC area as the small DC/DC converter symbol feeding the printed `BUS-24DC-C`.
- Printed bus nodes retained: `BUS-4160-A`, `BUS-4160-B`, `BUS-4160-ESF-A`, `BUS-4160-ESF-B`, `BUS-480-1A`, `BUS-480-1C`, `BUS-480-1B`, `BUS-480-2A`, `BUS-480-2C`, `BUS-480-2B`, `BUS-125DC-A`, `BUS-125DC-B`, `BUS-120AC-A`, `BUS-120AC-B`, `BUS-24DC-C`.
- I did not add section titles, voltage descriptions, title-block text, WN IDs, unlabeled junctions, or extra text nodes.

## Overall Review Result

- Started from Diego round 1: 200 nodes and 225 unique undirected edges.
- Jennifer reviewed matrix: 200 nodes and 216 unique undirected edges.
- Solid power paths, printed bus taps, grounds, transformer/breaker feeder chains, diesel/ATS paths, DC/UPS chains, and bus-mediated MCC/load branches were retained where the raw linework directly supports them.
- Revisions concentrate on dashed/control overconnections and one unsupported 24 VDC/JB tap.

## Removed / Rejected Edges

| Edge | Action | Visual evidence |
|---|---|---|
| `ANN-A -- PNL-RPS-A` | removed | ANN-A is on the left-side dashed trunk; REC-SER-A is the adjacent endpoint before PNL-RPS-A. |
| `ANN-B -- PNL-RPS-B` | removed | ANN-B is on the left-side dashed trunk; REC-SER-B is the adjacent endpoint before PNL-RPS-B. |
| `BUS-24DC-C -- JB-CTRL-A` | removed | JB-CTRL-A sits on the lower DCS/control dashed run; the printed 24 VDC bus does not visibly tap it. |
| `JB-1A-1 -- PNL-1A` | removed | The PNL-1A dashed drop is left of JB-1A-1; no direct endpoint contact is visible. |
| `JB-1A-1 -- RELAY-K12` | removed | The lower dashed/JB run does not terminate at the second relay; K12 is only on the relay pair line. |
| `JB-1B-1 -- PNL-1B` | removed | The PNL-1B dashed drop is offset from JB-1B-1; no direct endpoint contact is visible. |
| `JB-1B-1 -- RELAY-K32` | removed | The lower dashed/JB run does not terminate at the second relay; K32 is only on the relay pair line. |
| `JB-1C-1 -- PNL-1C` | removed | The PNL-1C dashed drop is offset from JB-1C-1; no direct endpoint contact is visible. |
| `JB-1C-1 -- RELAY-K22` | removed | The lower dashed/JB run does not terminate at the second relay; K22 is only on the relay pair line. |
| `JB-2A-1 -- PNL-2A` | removed | The PNL-2A dashed drop is offset from JB-2A-1; no direct endpoint contact is visible. |
| `JB-2A-1 -- RELAY-K42` | removed | The lower dashed/JB run does not terminate at the second relay; K42 is only on the relay pair line. |
| `JB-2B-1 -- PNL-2B` | removed | The PNL-2B dashed drop is offset from JB-2B-1; no direct endpoint contact is visible. |
| `JB-2B-1 -- RELAY-K62` | removed | The lower dashed/JB run does not terminate at the second relay; K62 is only on the relay pair line. |
| `JB-2C-1 -- PNL-2C` | removed | The PNL-2C dashed drop is offset from JB-2C-1; no direct endpoint contact is visible. |
| `JB-2C-1 -- RELAY-K52` | removed | The lower dashed/JB run does not terminate at the second relay; K52 is only on the relay pair line. |
| `PNL-RPS-A -- RELAY-KA1` | removed | RPS A dashed bundle reaches KA1 through the relay/annunciator trunk, not as a direct PNL-RPS endpoint. |
| `PNL-RPS-A -- RELAY-KA2` | removed | RPS A dashed bundle reaches KA2 through the relay/annunciator trunk, not as a direct PNL-RPS endpoint. |
| `PNL-RPS-B -- RELAY-KB1` | removed | RPS B dashed bundle reaches KB1 through the relay/annunciator trunk, not as a direct PNL-RPS endpoint. |
| `PNL-RPS-B -- RELAY-KB2` | removed | RPS B dashed bundle reaches KB2 through the relay/annunciator trunk, not as a direct PNL-RPS endpoint. |

## Added / Corrected Edges

| Edge | Action | Visual evidence |
|---|---|---|
| `ANN-A -- REC-SER-A` | added/corrected | RPS A dashed bundle visibly runs between the annunciator and sequence recorder. |
| `ANN-A -- RELAY-KA2` | added/corrected | RPS A dashed relay trunk continues from KA2 to the annunciator side before the recorder/RPS bundle. |
| `ANN-B -- REC-SER-B` | added/corrected | RPS B dashed bundle visibly runs between the annunciator and sequence recorder. |
| `ANN-B -- RELAY-KB2` | added/corrected | RPS B dashed relay trunk continues from KB2 to the annunciator side before the recorder/RPS bundle. |
| `JB-1A-1 -- RELAY-K11` | added/corrected | The local dashed control run from the JB/valve corner terminates at the first relay K11. |
| `JB-1B-1 -- RELAY-K31` | added/corrected | The local dashed control run from the JB/valve corner terminates at the first relay K31. |
| `JB-1C-1 -- RELAY-K21` | added/corrected | The local dashed control run from the JB/valve corner terminates at the first relay K21. |
| `JB-2A-1 -- RELAY-K41` | added/corrected | The local dashed control run from the JB/valve corner terminates at the first relay K41. |
| `JB-2B-1 -- RELAY-K61` | added/corrected | The local dashed control run from the JB/valve corner terminates at the first relay K61. |
| `JB-2C-1 -- RELAY-K51` | added/corrected | The local dashed control run from the JB/valve corner terminates at the first relay K51. |

## Remaining Uncertain / Lower-Confidence Included Cases

- `BUS-480-2A -- CB-DC-A`: Included; left-full raw crop shows a continuous routed feed from the 480 V 2A bus tap down to CB-DC-A.
- `BUS-480-2B -- CB-DC-B`: Included; right/full raw crop shows the analogous routed feed from the 480 V 2B bus tap to CB-DC-B.
- `BUS-125DC-A -- DC-DC-1`: Included; DC-DC-1 is raw-visible and its upper input trace routes from the upper DC run, though less legible than the 24 V output.
- `DC-DC-1 -- BUS-24DC-C`: Included; converter output drops directly to the printed 24 VDC bus.
- 480 V `PNL-* -- RELAY-K*1` and `RELAY-K*1 -- RELAY-K*2`: Included as lower-confidence dashed/local control edges where the first-relay drop and relay-pair line are visibly drawn.
- RPS `REC-SER-* -- PNL-RPS-*` and `PNL-RPS-* -- INST-NIS-*`: Included; dashed bundles enter the RPS panel directly from the recorder side and from the NIS side.

## Deliberately Excluded Ambiguous Cases

- 480 V `PNL-* -- JB-*`: Excluded; the panel dashed drop is offset from the JB box and no direct endpoint contact is visible.
- 480 V `JB-* -- RELAY-K*2`: Excluded/retargeted; the visible lower local run terminates at the first relay, not the second relay.
- RPS direct `PNL-RPS-* -- RELAY-K*`: Excluded; relays are reached through the left dashed trunk rather than direct panel endpoints.
- RPS direct `ANN-* -- PNL-RPS-*`: Excluded; ANN connects through the adjacent recorder-side dashed trunk before the RPS panel.
- `BUS-24DC-C -- JB-CTRL-A`: Excluded; JB-CTRL-A is on the lower DCS/JB dashed run below the 24 V bus.

## Validation Summary

- Node count: 200
- Undirected edge count: 216
- Matrix shape/order: 200 rows x 200 columns, row and column labels identical
- Symmetric: True
- Diagonal zero: True
- Isolated nodes: none

Output files:

- `C:\Asif_all_python_projects\INL\Improved -- blind iterations\23\Results\Iteration_1\round_01_jennifer_matrix.csv`
- `C:\Asif_all_python_projects\INL\Improved -- blind iterations\23\Results\Iteration_1\round_01_jennifer_notes.md`
