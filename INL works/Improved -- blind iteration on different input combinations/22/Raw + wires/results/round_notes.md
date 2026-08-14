# Document 22 Round Notes

## Scope
- Used only resources under `Raw + wires`.
- No ground-truth file or GT-derived feedback was used.
- No OCR engine was used. Labels were read by visual inspection.

## Diego Round 1 - High Recall
Diego identified the full power-distribution structure: generator, GSU, switchyard, 13.8 kV source/header, 13.8 kV buses, 4160 V trains A-D, DG incomers, 480 V load centers, MCCs, AC loads, 125 V DC/UPS systems, RPS/ESF/PLC panels, junctions, terminals, and metering.

High-recall candidates retained for Jennifer included `XFRM-PT-1--METER-A01` and per-train CT series candidates from the left MCC to `INST-CT-*` and `CB-RHR-*`.

## Jennifer Round 1 - Precision Refinement
Jennifer kept the visually supported bus, breaker, transformer, MCC, load, DC/UPS, control-panel, junction, and metering connections. She removed the CT-series and `METER-A01` candidates because the raw and overlay crops did not show confirmed solid-wire connections. She treated `C-030`, `C-031`, `W-011`, and `W-022` as wire/cable annotations, not components. She added `SRC-13.8-HDR` as the unlabeled physical top source/header node feeding both `CB-13A1` and `CB-13B1` from the switchyard.

## Diego Round 2 - Agreement Check
Diego accepted Jennifer's corrections and made the eight MCC incomer paths explicit:
`BUS-480-A--CB-MCC-AA--MCC-AA`, `BUS-480-A--CB-MCC-AB--MCC-AB`,
`BUS-480-B--CB-MCC-BA--MCC-BA`, `BUS-480-B--CB-MCC-BB--MCC-BB`,
`BUS-480-C--CB-MCC-CA--MCC-CA`, `BUS-480-C--CB-MCC-CB--MCC-CB`,
`BUS-480-D--CB-MCC-DA--MCC-DA`, and `BUS-480-D--CB-MCC-DB--MCC-DB`.

## Jennifer Round 2 - Saturated Final
Jennifer confirmed the final matrix:
- `SRC-13.8-HDR` remains a logical/physical unlabeled source header.
- `INST-CT-A`, `INST-CT-B`, `INST-CT-C`, `INST-CT-D`, and `METER-A01` remain visible but isolated because direct solid-wire edges are not confirmed.
- The only confirmed PT/meter connection is `XFRM-PT-1--METER-V01`.
- The final edge set is saturated with Diego's Round 2 proposal.
