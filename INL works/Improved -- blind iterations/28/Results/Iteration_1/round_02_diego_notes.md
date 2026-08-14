# Round 02 Diego Notes - Doc 28 Iteration 1

## Scope
I inspected only the doc 28 input resources, the prepared doc 28 inspection crops/artifacts, and the two round-01 proposals in `Results/Iteration_1` for this same document/iteration. The raw schematic/crops were primary evidence. No ground truth, evaluator output, score feedback, or other document/iteration resources were used.

## Final Validation
- Matrix path: `C:\Asif_all_python_projects\INL\Improved -- blind iterations\28\Results\Iteration_1\round_02_diego_matrix.csv`
- Node count: 194
- Undirected edge count: 196
- Row/column labels identical: yes
- Duplicate node labels: no
- Values only 0/1: yes
- Symmetric: yes
- Diagonal all zero: yes
- Isolated nodes: JB-101, JB-201, V-301, AIT-301, JB-301, DCS-001, CP-101, PLC-101

## Accepted Jennifer Changes
Accepted added edges because the named headers/connectors and local adjacency are raw-visible:
- `H-CCW-DIS -- H-CCW-FLTR`
- `H-CCW-FLTR -- HV-120`
- `H-CCW-FLTR -- HV-201A`
- `H-CCW-FLTR -- HV-201B`
- `H-CCW-FLTR -- HV-203`
- `H-SW-SUP -- HV-211A`
- `H-SW-SUP -- HV-211B`
- `H-SW-SUP -- PSV-215`
- `H-VT-001 -- VV-151A`
- `HV-103 -- TK-101`
- `OPC-501 -- VSR`

Accepted removals/replacements because I did not see a direct raw-visible termination on both named endpoints, or because Jennifer replaced a direct edge with a better named-header path:
- `AIT-301 -- DCS-001`
- `AIT-301 -- H-CD-001`
- `CP-101 -- PLC-101`
- `CV-203 -- TCV-203 and node CV-203`
- `DCS-001 -- JB-101`
- `DCS-001 -- JB-201`
- `DCS-001 -- JB-301`
- `DV-101 -- TK-101`
- `H-CCW-DIS -- HV-120`
- `H-CCW-DIS -- HV-201A`
- `H-CCW-DIS -- HV-201B`
- `H-CCW-DIS -- HV-203`
- `LCP-401 -- PLC-101`
- `TK-301 -- V-301`

## Rejected Jennifer Changes
- Jennifer removal of TIC-203: raw right/HX crop shows TIC-203 as a separate circular controller below TCV-203, so it is restored with TIC-203 -- TCV-203.

## New Round-02 Changes Beyond Both Round-01 Matrices
- Removed TIE-IN as a generic text node and replaced MOV-205 -- TIE-IN with MOV-205 -- OPC-102, the raw-visible off-page connector at that endpoint.
- Added MOV-214 -- OPC-202 from the raw-visible SW return endpoint after MOV-214.
- Added HV-403 -- OPC-401 from the raw-visible wastewater endpoint after HV-403.
- Added TIC-203 -- TCV-203 from the visible dashed control line between the controller bubble and the valve.

## Node Decisions
- Kept Jennifer's `H-CCW-FLTR`, `H-SW-SUP`, `H-VT-001`, and `OPC-501`; each is raw-visible as a named header/connector.
- Kept Jennifer's removal of `CV-203`; the valve on the process line is labeled `TCV-203`, not `CV-203`.
- Kept `MX-301` instead of inventory/OCR `M-301`; the raw static mixer label reads `MX-301`.
- Restored `TIC-203`; it is a separate raw-visible circular controller/instrument below `TCV-203`.
- Replaced generic `TIE-IN` with the specific raw-visible connector `OPC-102` at the `MOV-205` endpoint. Added similarly raw-visible `OPC-202` and `OPC-401`.
- Left raw-visible panel/JB/control boxes isolated when a dashed/control line passed nearby but did not visibly terminate on both endpoints: JB-101, JB-201, V-301, AIT-301, JB-301, DCS-001, CP-101, PLC-101.

## Decision Evidence By Disputed Area
- `H-CCW-FLTR`: center-full raw crop shows a boxed `H-CCW-FLTR`/filtered CCW header between the filter outlet/discharge area and the branches to `HV-201A`, `HV-201B`, `HV-203`, and `HV-120`; Jennifer's re-anchoring through this header is supported.
- `H-SW-SUP`: center/HX raw crops show a boxed 4-inch SW supply header feeding `PSV-215` and the `HV-211A/B` branches; Jennifer's added edges are supported.
- `H-VT-001`: center raw crop shows the boxed 2-inch vent header directly feeding the `VV-151A` through `VV-154` valve chain; Jennifer's `H-VT-001 -- VV-151A` edge is supported.
- `OPC-501`: right-full raw crop shows `VSR` followed by the off-page connector `OPC-501`; Jennifer's edge is supported.
- `HV-103`/`DV-101`/`TK-101`: tank crop shows the tank bottom branch reaches `HV-103` before `DV-101`; Jennifer's replacement of `TK-101 -- DV-101` with `TK-101 -- HV-103` is supported while retaining `HV-103 -- DV-101`.
- `V-301`, `AIT-301`, `JB-*`, `DCS-001`, `CP-101`, and `PLC-101`: raw crops show these labels/boxes, but I did not see direct endpoints on both sides for the removed Diego edges, so Jennifer's isolation/conservative treatment is accepted.
- `TIC-203`: right-full/HX crop shows a circular `TIC 203` instrument beneath `TCV-203`; it was not an OCR false split. I restored it and added `TIC-203 -- TCV-203`.
- `OPC-102`, `OPC-202`, `OPC-401`: right-full raw crop shows these as named off-page connector objects directly after `MOV-205`, `MOV-214`, and `HV-403`, respectively. These are visually obvious named connector nodes missing from both round-01 matrices.

## Ambiguous Cases Retained Conservatively
- I retained existing high-recall local instrument associations where the raw drawing shows nearby termination, including tank level instruments and local controller-to-valve links.
- I did not add edges from `DCS-001`, `JB-101`, `JB-201`, `JB-301`, `CP-101`, or `PLC-101` to passing dashed trunks because the raw crop does not clearly show endpoint termination on both named objects.
- I did not add line-number labels, `C1`/`C2`, numbered triangular continuation marks, spare-blind/cap text, or WN/intermediate wire nodes as graph nodes.
- Long headers remain represented by adjacent named components/header boxes rather than clique-expanded across every object on the same drawn line.
