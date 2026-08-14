# Connectivity Extraction Note - Document 40

Generated: 2026-07-14T13:58:47

## Scope

- Raw resource folder: `C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\40\Raw`
- Raw image: `raw -- synthetic_nuclear_distribution_schematic.png`
- Constraint followed: Diego and Jennifer used only the Raw/Input resources. Ground Truth and GT-derived feedback were not used.
- Derived sibling folders outside `Raw` were not used for extraction.

## Agent Rounds

- Round 01 Diego `high_recall`: 55 nodes, 66 edges, valid=True
- Round 02 Jennifer `precision_review`: 55 nodes, 56 edges, valid=True
- Round 03 Diego `saturation`: 55 nodes, 56 edges, valid=True
- Round 04 Jennifer `final`: 55 nodes, 56 edges, valid=True

Diego's high-recall round carried review-only extras where nearby lines or crossings could be visually tempting. Jennifer pruned them because the schematic legend states that a dot denotes a junction and a line crossing without a dot is not a connection.

## Final Result

- Final node count: 55
- Final edge count: 56
- Matrix: 55 x 55
- Symmetric: True
- Diagonal zero: True
- Validation errors: 0

## Final Edges

- `DG-21A -- ATS-21A`
- `UAT-2A -- DS-21A`
- `DS-21A -- ATS-21A`
- `ATS-21A -- SWGR-21A`
- `SWGR-21A -- CB-21A1`
- `CB-21A1 -- TR-21A`
- `TR-21A -- MCC-21A`
- `SWGR-21A -- TIE-BKR-21AB`
- `TIE-BKR-21AB -- SWGR-21B`
- `MCC-21A -- CB-MPA1`
- `CB-MPA1 -- PUMP-SI21A`
- `MCC-21A -- PUMP-CCW21A`
- `MCC-21A -- FAN-RB21A`
- `MCC-21A -- MOV-HV211A`
- `MCC-21A -- MOV-RWST21A`
- `MCC-21A -- XFMR-CPT21A`
- `XFMR-CPT21A -- AC-PNL-120A`
- `AC-PNL-120A -- RECT-21A`
- `RECT-21A -- DC-BUS-21A`
- `BAT-21A -- DC-BUS-21A`
- `INV-21A -- DC-BUS-21A`
- `LOCA-SIG-A -- JB-21A`
- `JB-21A -- RPS-PNL-A`
- `CT-21A -- RPS-PNL-A`
- `VT-21A -- RPS-PNL-A`
- `INV-21A -- RPS-PNL-A`
- `RPS-PNL-A -- RELAY-K21A`
- `RELAY-K21A -- RELAY-86A`
- `RELAY-86A -- CB-MPA1`
- `DG-21B -- ATS-21B`
- `SAT-2B -- DS-21B`
- `DS-21B -- ATS-21B`
- `ATS-21B -- SWGR-21B`
- `SWGR-21B -- CB-21B1`
- `CB-21B1 -- TR-21B`
- `TR-21B -- MCC-21B`
- `MCC-21B -- XFMR-CPT21B`
- `XFMR-CPT21B -- AC-PNL-120B`
- `AC-PNL-120B -- RECT-21B`
- `RECT-21B -- DC-BUS-21B`
- `BAT-21B -- DC-BUS-21B`
- `INV-21B -- DC-BUS-21B`
- `MCC-21B -- CB-MPB1`
- `CB-MPB1 -- PUMP-SI21B`
- `MCC-21B -- PUMP-CCW21B`
- `MCC-21B -- FAN-RB21B`
- `MCC-21B -- MOV-HV211B`
- `MCC-21B -- MOV-RWST21B`
- `LOCA-SIG-B -- JB-21B`
- `JB-21B -- RPS-PNL-B`
- `CT-21B -- RPS-PNL-B`
- `VT-21B -- RPS-PNL-B`
- `INV-21B -- RPS-PNL-B`
- `RPS-PNL-B -- RELAY-K21B`
- `RELAY-K21B -- RELAY-86B`
- `RELAY-86B -- CB-MPB1`

## Pruned High-Recall Candidates

- `MOV-RWST21A -- RPS-PNL-A`
- `MOV-RWST21B -- RPS-PNL-B`
- `DC-BUS-21A -- RPS-PNL-A`
- `DC-BUS-21B -- RPS-PNL-B`
- `SWGR-21A -- VT-21A`
- `SWGR-21B -- VT-21B`
- `MCC-21A -- CT-21A`
- `FAN-RB21A -- CT-21A`
- `MCC-21B -- CT-21B`
- `FAN-RB21B -- CT-21B`

## Label Notes

- `PUMP-SI21A` and `PUMP-SI21B` are safety-injection pump labels; the middle characters are `SI`, not `S1`.
- The right-side offsite/source label is `SAT-2B`.
- Cable or route labels such as `C21A-01`, `C21B-01`, `D21A-07`, `D21B-07`, `S21A-11`, and `S21B-11` were treated as annotations, not connectivity nodes.

## Token Tracking

-
 
E
x
p
e
c
t
e
d
 
t
o
t
a
l
 
t
o
k
e
n
s
:
 
1
7
2
0
2
0
 
(
l
o
w
 
1
3
1
6
5
0
,
 
h
i
g
h
 
2
3
5
0
0
0
)
;
 
m
o
d
e
l
 
c
a
l
l
s
 
c
o
u
n
t
e
d
:
 
9
.

Actual per-response usage objects were not exposed by the available Codex subagent tools. The Responses input-token counting endpoint was not called because `OPENAI_API_KEY` was unavailable in this execution environment. The CSV files therefore contain low/expected/high estimates and explicit `actual_usage_available=no` markers.
