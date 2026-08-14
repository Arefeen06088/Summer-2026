# Document 41 Connectivity Extraction

## Scope

Only resources inside:

`C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\41\Raw + wires + components + junctions`

were used. No Ground Truth files, GT-derived feedback, OCR sibling folders, or off-the-shelf OCR outputs were used. The extraction relied on visual inspection of the raw schematic plus the allowed wire/component/junction aids.

## Multi-Agent Rounds

1. Diego round 1: high-recall extraction with plausible labels/internal symbols retained.
2. Jennifer round 2: precision review; removed callouts/internal annotations and corrected the B charger feed.
3. Diego round 3: agreed with Jennifer unchanged.
4. Jennifer round 4: confirmed saturation unchanged.

## Final Result

- Final nodes: 58
- Final undirected edges: 60
- Matrix: `final_connectivity_matrix.csv`
- Edge list: `final_edges.csv`

## Final Edges

- OFFSITE-A -- TR-1A (power_feeder, high)
- TR-1A -- GND-1E (grounding, high)
- TR-1A -- CB-101 (power_feeder, high)
- CB-101 -- BUS-1A-4.16KV (power_feeder, high)
- EDG-1A -- CB-105 (power_feeder, high)
- CB-105 -- BUS-1A-4.16KV (power_feeder, high)
- BUS-1A-4.16KV -- CB-TIE-1AB (power_feeder, high)
- CB-TIE-1AB -- BUS-1B-4.16KV (power_feeder, high)
- BUS-1B-4.16KV -- CB-102 (power_feeder, high)
- CB-102 -- TR-1B (power_feeder, high)
- TR-1B -- OFFSITE-B (power_feeder, high)
- EDG-1B -- CB-106 (power_feeder, high)
- CB-106 -- BUS-1B-4.16KV (power_feeder, high)
- BUS-1A-4.16KV -- TR-LC-1A (power_feeder, high)
- BUS-1A-4.16KV -- TR-SAF-1A (power_feeder, high)
- BUS-1B-4.16KV -- TR-LC-1B (power_feeder, high)
- BUS-1B-4.16KV -- TR-SAF-1B (power_feeder, high)
- TR-LC-1A -- CB-201 (power_feeder, high)
- CB-201 -- BUS-480A (power_feeder, high)
- TR-SAF-1A -- CB-203 (power_feeder, high)
- CB-203 -- BUS-480E1A (power_feeder, high)
- TR-LC-1B -- CB-202 (power_feeder, high)
- CB-202 -- BUS-480B (power_feeder, high)
- TR-SAF-1B -- CB-204 (power_feeder, high)
- CB-204 -- BUS-480E1B (power_feeder, high)
- BUS-480A -- MCC-1A (power_feeder, high)
- BUS-480A -- MCC-1C (power_feeder, high)
- BUS-480A -- CHGR-125A (power_feeder, high)
- BUS-480E1A -- MCC-ESS-A (power_feeder, high)
- MCC-1A -- PUMP-CCW-103A (power_feeder, high)
- MCC-1C -- FAN-CRHV-104A (power_feeder, high)
- MCC-ESS-A -- PUMP-SI-101A (power_feeder, high)
- MCC-ESS-A -- PUMP-RHR-102A (power_feeder, high)
- MCC-ESS-A -- MOV-1201A (power_feeder, high)
- BUS-480B -- MCC-1B (power_feeder, high)
- BUS-480B -- MCC-1D (power_feeder, high)
- BUS-480E1B -- MCC-ESS-B (power_feeder, high)
- BUS-480E1B -- CHGR-125B (power_feeder, medium)
- MCC-1B -- PUMP-CCW-103B (power_feeder, high)
- MCC-1D -- FAN-CRHV-104B (power_feeder, high)
- MCC-ESS-B -- PUMP-SI-101B (power_feeder, high)
- MCC-ESS-B -- PUMP-RHR-102B (power_feeder, high)
- MCC-ESS-B -- MOV-1201B (power_feeder, high)
- CHGR-125A -- DC-BUS-125A (dc_power, high)
- BAT-125A -- DC-BUS-125A (dc_power, high)
- DC-BUS-125A -- INV-120A (dc_power, high)
- INV-120A -- UPS-BUS-A (ac_power, high)
- UPS-BUS-A -- PANEL-RPS-A (ac_power, medium)
- UPS-BUS-A -- INST-RACK-1 (instrument_power, high)
- CHGR-125B -- DC-BUS-125B (dc_power, high)
- BAT-125B -- DC-BUS-125B (dc_power, high)
- DC-BUS-125B -- INV-120B (dc_power, high)
- INV-120B -- UPS-BUS-B (ac_power, high)
- UPS-BUS-B -- PANEL-RPS-B (ac_power, medium)
- CB-105 -- RELAY-K86A (control_interlock, high)
- RELAY-K86A -- PANEL-RPS-A (control_interlock, high)
- CB-106 -- RELAY-K86B (control_interlock, high)
- RELAY-K86B -- PANEL-RPS-B (control_interlock, high)
- JB-ESF-01 -- PANEL-RPS-A (control_interlock, medium)
- JB-ESF-01 -- PANEL-RPS-B (control_interlock, medium)

## Excluded Or Collapsed Items

- EDG A INCOMING: feeder/callout label, not a component node
- EDG B INCOMING: feeder/callout label, not a component node
- CTRL-86A: control circuit label; collapsed to CB-105--RELAY-K86A
- CTRL-86B: control circuit label; collapsed to CB-106--RELAY-K86B
- CABLE 1A-480-7: cable callout used as evidence, not a node
- CABLE 1B-480-9: cable callout used as evidence, not a node
- FDR A-DC: feeder label used as evidence, not a node
- FDR B-DC: feeder label used as evidence, not a node
- TB1: terminal label internal to JB-ESF-01
- PT: internal function inside INST-RACK-1
- UV: internal function inside INST-RACK-1
- SEQ: internal function inside INST-RACK-1
- BUS-480B--CHGR-125B: excluded; final review supports BUS-480E1B--CHGR-125B instead
- INST-RACK-1--PT/UV/SEQ: excluded as internal annotations without separate external terminals
- JB-ESF-01--TB1: excluded as an internal terminal annotation

## Token Accounting

The OpenAI Responses input-token counting endpoint was not called because no API key was available in this environment. Response `usage` objects for the main agent and subagents were not exposed by the local tooling. Token counts are therefore local low/expected/high estimates.

- Estimated total low: 68620
- Estimated total expected: 77680
- Estimated total high: 90500
- Estimated image/file input tokens: 24000

Detailed call-level estimates are in `token_usage_estimate.csv`; grouped totals are in `token_usage_summary.csv` and `token_usage_summary.json`.
