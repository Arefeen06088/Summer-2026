# Connectivity Extraction Note - Document 41

Generated: 2026-07-14T14:17:53

## Scope

- Raw resource folder: `C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\41\Raw`
- Raw image: `raw -- synthetic_npp_electrical_schematic(2).png`
- Constraint followed: Diego and Jennifer used only the Raw/Input resources. Ground Truth and GT-derived feedback were not used.
- Derived sibling folders outside `Raw` were not used for extraction.

## Agent Rounds

- Round 01 Diego `high_recall`: 60 nodes, 68 edges, valid=True
- Round 02 Jennifer `precision_review`: 58 nodes, 60 edges, valid=True
- Round 03 Diego `saturation`: 58 nodes, 60 edges, valid=True
- Round 04 Jennifer `final`: 58 nodes, 60 edges, valid=True

## Final Result

- Final node count: 58
- Final edge count: 60
- Matrix: 58 x 58
- Symmetric: True
- Diagonal zero: True
- Validation errors: 0

## Final Edges

- `OFFSITE-A-161KV -- TR-1A`
- `TR-1A -- CB-101`
- `CB-101 -- BUS-1A-4.16KV`
- `TR-1A -- GND-1E`
- `EDG-1A -- CB-105`
- `CB-105 -- BUS-1A-4.16KV`
- `BUS-1A-4.16KV -- CB-TIE-1AB`
- `CB-TIE-1AB -- BUS-1B-4.16KV`
- `BUS-1B-4.16KV -- CB-102`
- `CB-102 -- TR-1B`
- `TR-1B -- OFFSITE-B-161KV`
- `EDG-1B -- CB-106`
- `CB-106 -- BUS-1B-4.16KV`
- `BUS-1A-4.16KV -- TR-LC-1A`
- `TR-LC-1A -- CB-201`
- `CB-201 -- BUS-480A`
- `BUS-1A-4.16KV -- TR-SAF-1A`
- `TR-SAF-1A -- CB-203`
- `CB-203 -- BUS-480E1A`
- `BUS-1B-4.16KV -- TR-LC-1B`
- `TR-LC-1B -- CB-202`
- `CB-202 -- BUS-480B`
- `BUS-1B-4.16KV -- TR-SAF-1B`
- `TR-SAF-1B -- CB-204`
- `CB-204 -- BUS-480E1B`
- `BUS-480A -- MCC-1A`
- `MCC-1A -- PUMP-CCW-103A`
- `BUS-480A -- MCC-1C`
- `MCC-1C -- FAN-CRHV-104A`
- `BUS-480E1A -- MCC-ESS-A`
- `MCC-ESS-A -- PUMP-SI-101A`
- `MCC-ESS-A -- PUMP-RHR-102A`
- `MCC-ESS-A -- MOV-1201A`
- `BUS-480B -- MCC-1B`
- `MCC-1B -- PUMP-CCW-103B`
- `BUS-480B -- MCC-1D`
- `MCC-1D -- FAN-CRHV-104B`
- `BUS-480E1B -- MCC-ESS-B`
- `MCC-ESS-B -- PUMP-SI-101B`
- `MCC-ESS-B -- PUMP-RHR-102B`
- `MCC-ESS-B -- MOV-1201B`
- `BUS-480A -- CHGR-125A`
- `CHGR-125A -- DC-BUS-125A`
- `BAT-125A -- DC-BUS-125A`
- `DC-BUS-125A -- INV-120A`
- `INV-120A -- UPS-BUS-A`
- `UPS-BUS-A -- PANEL-RPS-A`
- `UPS-BUS-A -- INST-RACK-1`
- `CB-204 -- CHGR-125B`
- `CHGR-125B -- DC-BUS-125B`
- `BAT-125B -- DC-BUS-125B`
- `DC-BUS-125B -- INV-120B`
- `INV-120B -- UPS-BUS-B`
- `UPS-BUS-B -- PANEL-RPS-B`
- `CB-105 -- RELAY-K86A`
- `RELAY-K86A -- PANEL-RPS-A`
- `PANEL-RPS-A -- JB-ESF-01-TB1`
- `JB-ESF-01-TB1 -- PANEL-RPS-B`
- `PANEL-RPS-B -- RELAY-K86B`
- `RELAY-K86B -- CB-106`

## Precision Changes

- `CTRL-86A`, `CTRL-86B` removed as callout/conductor labels, not device nodes.
- `BUS-1A-4.16KV -- BUS-1B-4.16KV` direct bus collapse removed; `CB-TIE-1AB` remains between buses.
- `BUS-480E1B -- CHGR-125B` changed to `CB-204 -- CHGR-125B` based on visible load-side branch.
- `PUMP-RHR-102A -- CTRL-86A` and `FAN-CRHV-104B -- CTRL-86B` removed as unsupported crossings/nearby dashed runs.
- `UPS-BUS-A -- UPS-BUS-B` and `UPS-BUS-B -- INST-RACK-1` removed because no terminal dot/device port supports those joins.

## Label Notes

- Cable labels such as `CABLE 1A-480-7`, `CABLE 1B-480-9`, `4160V FEED A`, `FDR A-DC`, and `FDR B-DC` were treated as annotations, not component nodes.
- `JB-ESF-01-TB1` was aggregated as one junction/terminal-block node.
- Internal labels inside `INST-RACK-1` (`PT`, `UV`, `SEQ`) were treated as internal subdevices without separate external edges.

## Token Tracking

- Expected total tokens: 206800 (low 160150, high 278400).
- Model calls counted: 9.
- Actual usage objects unavailable: yes.

Actual per-response usage objects were not exposed by the available Codex subagent tools. The Responses input-token counting endpoint was not called because `OPENAI_API_KEY` was unavailable in this execution environment. The CSV files therefore contain low/expected/high estimates and explicit `actual_usage_available=no` markers.
