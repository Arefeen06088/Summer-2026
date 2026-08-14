# Round 02 Diego Saturation Review Notes

Scope: doc34 Input resources, doc34 Codes and artifacts, and doc34 Results round files only. I did not open or use ground truth, evaluator output, scores, previous-doc feedback, validation metrics, or anything outside the allowed doc34 paths.

## Decision

I agree with Jennifer Round 01. `round_02_diego_matrix.csv` is an exact copy of `round_01_jennifer_matrix.csv`.

No Round 02 edge or node changes were made beyond Jennifer's Round 01 refinement.

## Visual Review Rationale

- Top control row crops support the local chain `JB-401--JB-102--JB-101--PLC-101--CP-101--DCS-001`, the CP drop to `YI-101`, and the DCS local endpoints. They do not support restoring `MCC-101--P-501`.
- IA/N2 crops support solid process chains through `OPC-501--HV-501--PRV-501--H-IA-101` and `OPC-502--HV-520--PRV-520--H-N2-101--PCV-501`; `PT-501` is better represented in the local `PT-501--PIC-501--PAH-501` / `PIC-501--PCV-501` signal/control detail than as a direct `H-N2-101` tap.
- Upper CCW supply crops support replacing actuator-position bridges with local named process endpoints: `H-CCW-S--TIE-101` and `TIE-103--OPC-102`. `ZSO/ZSC` instruments remain paired locally but are not process-line bridges.
- Cleanup/filter crops support Jennifer's `HV-113A--H-CLN-DIS` and `TK-101--VV-101` corrections. The rejected `HV-113A--VV-101`, `HV-113B--LIC-101`, and LIC/LT-to-level-switch shortcuts are plausible associations but not clear local endpoint adjacencies.
- Service-water crops support `H-SW-S--TIE-301--TCV-101--H-SW-SPL`; `HS-201` is local to the actuated valve/hand-switch detail and should not bridge the process path.
- Chemical dosing crops support the two pump trains and the local `H-CD-MIX` pairs. `SV-105--Q-401` and `AIC-401--SP-101` would close unsupported shortcuts, so Jennifer's stricter graph is preferable.
- Sample/drain/vent/waste crops support local header routing through `H-DRN-101`, `H-VNT-101`, `H-WW-101`, `SP-501`, `LT-501`, `LIC-501`, and `P-501`. The long `H-SMP-101--SP-501` and direct `H-VNT-101--LIC-501` skips are not locally clear enough for matrix edges.

## Ambiguous But Not Restored

- `H-SMP-101--SP-501`: plausible long sample routing, but no clear local termination into `SP-501`.
- `H-VNT-101--LIC-501`: vent adjacency is represented locally as `H-VNT-101--LT-501--LIC-501`.
- `LIC-401--HV-410` and `LIC-401--HV-411`: dashed control/association linework is near the valves, but direct terminations are not unambiguous.
- `ZSO/ZSC` to CCW process endpoints: visually tied to actuator position indication, not named process endpoints.
- `SV-102` remains visible but non-inventory and was not promoted to a Round 02 node.

## Basic Validation Summary

- Node count: 167
- Inventory components retained: 129 of 129
- Unique undirected edges: 181
- Row labels equal column labels in the same order: true
- Symmetric matrix: true
- Values are 0/1 only: true
- Diagonal zero: true
- Isolated nodes: none
- Matrix relation to Jennifer Round 01: exact copy
