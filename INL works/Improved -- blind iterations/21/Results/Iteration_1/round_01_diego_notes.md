# Diego Round 01 Connectivity Notes

## Extraction Scope
- Inputs inspected only from doc 21 `Input resources` and doc 21 `Codes and artifacts`.
- Raw schematic was treated as primary; component/OCR lists, wire masks, wire-node overlays, and inspection crops were used as aids.
- WN-* wire-node IDs and arbitrary intermediate points were not used as matrix nodes.

## Node List Rationale
- Included 183 physical component labels from `component_labels_list.csv`.
- Added raw-verified logical bus nodes: BUS-101, BUS-102, BUS-201A, BUS-201B, BUS-202A, BUS-202B, BUS-301A, BUS-301B, BUS-302A, BUS-302B, BUS-401A, BUS-401B, BUS-501A, BUS-501B.
- Added `CB-204A` because the raw EDG-1B/BUS-201B feeder visibly labels a breaker `CB-204A`, although the detector/component CSV omitted that physical breaker.
- Added `DS-401B` because the raw DC/UPS B-side chain visibly labels the disconnect `DS-401B`, although the detector/component CSV omitted that physical disconnect.
- Did not include section headers, notes, line-code legend text, WN-* wire IDs, or unlabeled small breaker symbols as named nodes.

## Edge Evidence by Area
### incoming sources
- `GEN-UT` -- `CB-101` (solid/raw)
- `GEN-UT` -- `CB-102` (solid/raw)
- `CB-101` -- `DS-101A` (solid/raw)
- `DS-101A` -- `TR-UAT1` (solid/raw)
- `TR-UAT1` -- `CB-201A` (solid/raw)
- `CB-201A` -- `BUS-201A` (solid/raw)
- `CB-102` -- `DS-101B` (solid/raw)
- `DS-101B` -- `TR-UAT2` (solid/raw)
- `TR-UAT2` -- `CB-201B` (solid/raw)
- `CB-201B` -- `BUS-201B` (solid/raw)
- `BUS-101` -- `CB-103` (solid/raw)
- `CB-103` -- `DS-102A` (solid/raw)
- `DS-102A` -- `TR-SU1` (solid/raw)
- `TR-SU1` -- `CB-202A` (solid/raw)
- `CB-202A` -- `BUS-202A` (solid/raw)
- `BUS-102` -- `CB-104` (solid/raw)
- `CB-104` -- `DS-102B` (solid/raw)
- `DS-102B` -- `TR-SU2` (solid/raw)
- `TR-SU2` -- `CB-202B` (solid/raw)
- `CB-202B` -- `BUS-202B` (solid/raw)
### upper switchgear / EDG
- `BUS-201A` -- `DS-201A` (solid/raw)
- `DS-201A` -- `CB-105` (solid/raw)
- `CB-105` -- `EDG-1A` (solid/raw)
- `BUS-201B` -- `CB-204A` (raw-visible; CB-204A detector-omitted)
- `CB-204A` -- `DS-201B` (raw-visible; CB-204A detector-omitted)
- `DS-201B` -- `CB-106` (raw-visible; CB-204A detector-omitted)
- `CB-106` -- `EDG-1B` (raw-visible; CB-204A detector-omitted)
- `BUS-202A` -- `DS-202A` (solid/raw)
- `DS-202A` -- `CB-203A` (solid/raw)
- `CB-203A` -- `EDG-2A` (solid/raw)
- `BUS-202B` -- `DS-202B` (solid/raw)
- `DS-202B` -- `CB-203B` (solid/raw)
- `CB-203B` -- `EDG-2B` (solid/raw)
### 480 V transformer feeders
- `BUS-201A` -- `CB-301A` (solid/raw)
- `CB-301A` -- `DS-J01A` (solid/raw)
- `DS-J01A` -- `TR-SA` (solid/raw)
- `TR-SA` -- `CB-501A` (solid/raw)
- `CB-501A` -- `BUS-301A` (solid/raw)
- `BUS-202A` -- `CB-302A` (solid/raw)
- `CB-302A` -- `DS-J02A` (solid/raw)
- `DS-J02A` -- `TR-NA` (solid/raw)
- `TR-NA` -- `CB-502A` (solid/raw)
- `CB-502A` -- `BUS-302A` (solid/raw)
- `BUS-201B` -- `CB-301B` (solid/raw)
- `CB-301B` -- `DS-J01B` (solid/raw)
- `DS-J01B` -- `TR-SB` (solid/raw)
- `TR-SB` -- `CB-501B` (solid/raw)
- `CB-501B` -- `BUS-301B` (solid/raw)
- `BUS-202B` -- `CB-302B` (solid/raw)
- `CB-302B` -- `DS-J02B` (solid/raw)
- `DS-J02B` -- `CB-502B` (solid/raw)
- `CB-502B` -- `TR-NB` (solid/raw)
- `TR-NB` -- `BUS-302B` (solid/raw)
### 480 V train A
- `BUS-301A` -- `GND-1` (solid/raw)
- `BUS-301A` -- `CB-303A` (solid/raw)
- `CB-303A` -- `MCC-1A` (solid/raw)
- `BUS-301A` -- `CB-304A` (solid/raw)
- `CB-304A` -- `MCC-2A` (solid/raw)
- `BUS-302A` -- `CB-503A` (solid/raw)
- `CB-503A` -- `MCC-3A` (solid/raw)
- `MCC-3A` -- `GND-5` (solid/raw)
### 480 V train A MCC loads
- `MCC-1A` -- `MOTOR-SI101A` (solid/raw)
- `MCC-1A` -- `PUMP-SI101A` (solid/raw)
- `MCC-1A` -- `MOTOR-CCW101A` (solid/raw)
- `MCC-1A` -- `PUMP-CCW101A` (solid/raw)
- `MCC-1A` -- `VLV-8801A` (solid/raw)
- `MCC-2A` -- `MOTOR-AFW101A` (solid/raw)
- `MCC-2A` -- `PUMP-AFW101A` (solid/raw)
- `MCC-2A` -- `MOTOR-RHR101A` (solid/raw)
- `MCC-2A` -- `PUMP-RHR101A` (solid/raw)
- `MCC-2A` -- `VLV-8802A` (solid/raw)
- `MCC-3A` -- `MOTOR-SW101A` (solid/raw)
- `MCC-3A` -- `PUMP-SW101A` (solid/raw)
- `MCC-3A` -- `MOTOR-CHG101A` (solid/raw)
- `MCC-3A` -- `PUMP-CHG101A` (solid/raw)
- `MCC-3A` -- `MOTOR-FAN101A` (solid/raw)
- `MCC-3A` -- `VLV-8901A` (solid/raw)
### 480 V train B
- `BUS-301B` -- `GND-2` (solid/raw)
- `BUS-301B` -- `CB-303B` (solid/raw)
- `CB-303B` -- `MCC-1B` (solid/raw)
- `BUS-301B` -- `CB-304B` (solid/raw)
- `CB-304B` -- `MCC-2B` (solid/raw)
- `BUS-302B` -- `CB-503B` (solid/raw)
- `CB-503B` -- `MCC-3B` (solid/raw)
- `MCC-3B` -- `GND-6` (solid/raw)
### 480 V train B MCC loads
- `MCC-1B` -- `MOTOR-SI101B` (solid/raw)
- `MCC-1B` -- `PUMP-SI101B` (solid/raw)
- `MCC-1B` -- `MOTOR-CCW101B` (solid/raw)
- `MCC-1B` -- `PUMP-CCW101B` (solid/raw)
- `MCC-1B` -- `VLV-8801B` (solid/raw)
- `MCC-2B` -- `MOTOR-AFW101B` (solid/raw)
- `MCC-2B` -- `PUMP-AFW101B` (solid/raw)
- `MCC-2B` -- `MOTOR-RHR101B` (solid/raw)
- `MCC-2B` -- `PUMP-RHR101B` (solid/raw)
- `MCC-2B` -- `VLV-8802B` (solid/raw)
- `MCC-3B` -- `MOTOR-SW101B` (solid/raw)
- `MCC-3B` -- `PUMP-SW101B` (solid/raw)
- `MCC-3B` -- `MOTOR-CHG101B` (solid/raw)
- `MCC-3B` -- `PUMP-CHG101B` (solid/raw)
- `MCC-3B` -- `MOTOR-FAN101B` (solid/raw)
- `MCC-3B` -- `VLV-8901B` (solid/raw)
### DC/UPS supplies
- `BUS-301A` -- `DS-401A` (solid/raw; upstream 480 V tap plausible)
- `DS-401A` -- `TR-DC-A` (solid/raw; upstream 480 V tap plausible)
- `TR-DC-A` -- `RECT-125A` (solid/raw; upstream 480 V tap plausible)
- `RECT-125A` -- `BUS-401A` (solid/raw; upstream 480 V tap plausible)
- `BUS-301B` -- `DS-401B` (solid/raw; upstream 480 V tap plausible)
- `DS-401B` -- `TR-DC-B` (solid/raw; upstream 480 V tap plausible)
- `TR-DC-B` -- `RECT-125B` (solid/raw; upstream 480 V tap plausible)
- `RECT-125B` -- `BUS-401B` (solid/raw; upstream 480 V tap plausible)
- `BUS-302A` -- `DS-402A` (solid/raw; INV-120C output to control bus plausible)
- `DS-402A` -- `TR-INV-A` (solid/raw; INV-120C output to control bus plausible)
- `TR-INV-A` -- `INV-120C` (solid/raw; INV-120C output to control bus plausible)
- `INV-120C` -- `BUS-501A` (solid/raw; INV-120C output to control bus plausible)
- `BUS-302B` -- `DS-402B` (solid/raw; RECT-24C return/feed plausible)
- `DS-402B` -- `TR-INV-B` (solid/raw; RECT-24C return/feed plausible)
- `TR-INV-B` -- `RECT-24C` (solid/raw; RECT-24C return/feed plausible)
- `RECT-24C` -- `BUS-401B` (solid/raw; RECT-24C return/feed plausible)
- `BUS-401A` -- `BAT-1A` (solid/raw)
- `BUS-401A` -- `BAT-2A` (solid/raw)
- `BUS-401A` -- `GND-3` (solid/raw)
- `BUS-401A` -- `INV-120A` (solid/raw)
- `BUS-401B` -- `BAT-1B` (solid/raw)
- `BUS-401B` -- `BAT-2B` (solid/raw)
- `BUS-401B` -- `GND-4` (solid/raw)
- `BUS-401B` -- `INV-120B` (solid/raw)
### DC/UPS to ladder rails
- `INV-120A` -- `BUS-501A` (solid/raw)
- `INV-120B` -- `BUS-501B` (solid/raw)
### DC/UPS dashed EDG battery link
- `BAT-EDG-A` -- `CP-EDG-A` (dashed/weak)
- `BAT-EDG-B` -- `CP-EDG-B` (dashed/weak)
- `BAT-EDG-A` -- `BAT-EDG-B` (dashed/weak)
### control ladder rails
- `BUS-501A` -- `CP-SI-A` (dashed/control)
- `BUS-501B` -- `CP-SI-A` (dashed/control)
- `BUS-501A` -- `CP-SI-B` (dashed/control)
- `BUS-501B` -- `CP-SI-B` (dashed/control)
- `BUS-501A` -- `CP-CCW-A` (dashed/control)
- `BUS-501B` -- `CP-CCW-A` (dashed/control)
- `BUS-501A` -- `CP-CCW-B` (dashed/control)
- `BUS-501B` -- `CP-CCW-B` (dashed/control)
- `BUS-501A` -- `CP-EDG-A` (dashed/control)
- `BUS-501B` -- `CP-EDG-A` (dashed/control)
- `BUS-501A` -- `CP-EDG-B` (dashed/control)
- `BUS-501B` -- `CP-EDG-B` (dashed/control)
- `BUS-501A` -- `RPS-A` (dashed/control)
- `BUS-501B` -- `RPS-A` (dashed/control)
- `BUS-501A` -- `RPS-B` (dashed/control)
- `BUS-501B` -- `RPS-B` (dashed/control)
- `BUS-501A` -- `ESFAS-A` (dashed/control)
- `BUS-501B` -- `ESFAS-A` (dashed/control)
- `BUS-501A` -- `ESFAS-B` (dashed/control)
- `BUS-501B` -- `ESFAS-B` (dashed/control)
- `BUS-501A` -- `CP-SWGR` (dashed/control)
- `BUS-501B` -- `CP-SWGR` (dashed/control)
- `BUS-501A` -- `CP-CRD` (dashed/control)
- `BUS-501B` -- `CP-CRD` (dashed/control)
### control ladder vertical interlock
- `CP-SWGR` -- `CP-SI-A` (dashed/control)
- `CP-EDG-A` -- `CP-EDG-B` (dashed/control)
- `CP-EDG-B` -- `RPS-A` (dashed/control)
- `RPS-A` -- `RPS-B` (dashed/control)
- `RPS-B` -- `ESFAS-A` (dashed/control)
- `ESFAS-A` -- `ESFAS-B` (dashed/control)
- `ESFAS-B` -- `CP-CRD` (dashed/control)
### control ladder top interlock
- `CP-SWGR` -- `UVLS-A` (dashed/weak)
- `UVLS-A` -- `UVLS-B` (dashed/weak)
- `UVLS-A` -- `RELAY-K101` (dashed/weak)
- `UVLS-B` -- `RELAY-K102` (dashed/weak)
### control ladder rows
- `CP-CCW-A` row: `CP-CCW-A -- RELAY-K107 -- RELAY-K108 -- RELAY-K109 -- JB-103 -- INST-FT202 -- INST-LT301` (dashed/dotted control-signal)
- `CP-CCW-B` row: `CP-CCW-B -- RELAY-K110 -- RELAY-K111 -- RELAY-K112 -- JB-104 -- INST-LT302 -- INST-TT401` (dashed/dotted control-signal)
- `CP-EDG-A` row: `CP-EDG-A -- RELAY-K113 -- RELAY-K114 -- RELAY-K115 -- JB-105 -- INST-TT402 -- INST-CT501` (dashed/dotted control-signal)
- `CP-EDG-B` row: `CP-EDG-B -- RELAY-K116 -- RELAY-K117 -- RELAY-K118 -- JB-106 -- INST-CT502` (dashed/dotted control-signal)
- `CP-SI-A` row: `CP-SI-A -- RELAY-K101 -- RELAY-K102 -- RELAY-K103 -- JB-101 -- INST-PT101 -- INST-PT102` (dashed/dotted control-signal)
- `CP-SI-B` row: `CP-SI-B -- RELAY-K104 -- RELAY-K105 -- RELAY-K106 -- JB-102 -- INST-PT103 -- INST-FT201` (dashed/dotted control-signal)
- `ESFAS-A` row: `ESFAS-A -- RELAY-K125 -- RELAY-K126 -- RELAY-K127 -- JB-109 -- INST-ZS701` (dashed/dotted control-signal)
- `ESFAS-B` row: `ESFAS-B -- RELAY-K128 -- RELAY-K129 -- RELAY-K130 -- JB-110 -- INST-ZS702` (dashed/dotted control-signal)
- `RPS-A` row: `RPS-A -- RELAY-K119 -- RELAY-K120 -- RELAY-K121 -- JB-107 -- INST-VT601` (dashed/dotted control-signal)
- `RPS-B` row: `RPS-B -- RELAY-K122 -- RELAY-K123 -- RELAY-K124 -- JB-108 -- INST-VT602` (dashed/dotted control-signal)

## Uncertain / High-Recall Candidates
- Included `CB-204A` and `DS-401B` as raw-visible physical components despite detector omission.
- Included plausible upstream 480 V feeder taps from `BUS-301A/BUS-301B/BUS-302A/BUS-302B` into the DC/UPS disconnect chains; the long drops are visible, but their exact source-bus assignment is inferred from alignment.
- Included `INV-120C` to `BUS-501A` and `RECT-24C` to `BUS-401B` as plausible output/feed connections from the raw paths.
- Included dashed `BAT-EDG-A/B` links to `CP-EDG-A/B` and to each other as weak high-recall candidates; these dashed paths are visually present but not as solid power conductors.
- Included row-wise ladder connections and vertical interlock links as dashed/dotted control/signal evidence, not solid power feeders.
- Kept out unlabeled small breaker-like symbols on some EDG feeders because no exact raw-printed label was verified except `CB-204A`.

## Validation Summary
- Node count: 199
- Edge count: 220
- Symmetric: True
- Diagonal zero: True
- Row and column labels: identical and in the same order by construction.
