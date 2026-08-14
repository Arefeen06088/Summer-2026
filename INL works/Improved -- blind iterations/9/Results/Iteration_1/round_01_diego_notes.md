# Round 01 Diego Notes

## Node policy

I included physical schematic components, explicitly named bus bars, and ground nodes as matrix nodes. I did not include unlabeled junction dots, wire elbows, sheet borders, title blocks, dashed train/container outlines, or section headings such as OFFSITE / UNIT AUXILIARY SOURCES unless the item visually functions as a named electrical node.

Raw schematic labels were preferred over OCR. Corrections applied: `CB-COMP-AI` was read visually as `CB-COMP-A`; `JB-1BO` and `JB-2BO` were read visually as `JB-1B0` and `JB-2B0` because the A-side equivalents use zero (`JB-1A0`, `JB-2A0`) and the raw glyphs match zero-like terminal-box naming. I also added visible boxes not present in the component CSV: `RTD-PNL-A`, `RTD-PNL-B`, `TDR-SEQ-A`, and `TDR-SEQ-B`.

## Edge evidence by region

Top sources and normal auxiliary: solid power paths connect `UTIL-230A/B` through `DS-230A/B`, `SAT-1A/B`, and `CB-SAT-A/B` to the safety 4.16 kV buses. `GEN-1A` connects through `CB-GEN-1` to `BUS-13K-01`, which taps to `UAT-1A/B`; `CB-UAT-1A/B` feed `BUS-4160-N1/N2`, tied through `CB-TIE-41N`.

Normal 4.16 kV to 480 V: each normal 4.16 kV bus has breaker-transformer-breaker chains into named 480 V buses (`BUS-480-N1A/N1B/N2A/N2B`), then to MCC and panel nodes. Panel feeders are represented one line per visible breaker/load branch.

Safety train A/B: `EDG-1A/B` feed their train 4.16 kV buses through `CB-EDG-A/B`. Each train bus feeds two 480 V transformer strings, then 480 V safety buses and MCCs. MCC outgoing breaker/load branches are high-confidence solid edges.

MOV/fuse panels: `PN-MOV-A/B` feed individual fuses and MOV/valve nodes through visible solid conductors. The upstream source into each MOV panel is geometrically plausible but not fully unambiguous, so those are in the plausible file.

DC/UPS/control: `BAT-125A/B`, `CHG-125A/B`, `BUS-125DC-A/B`, `INV-120A/B`, `BUS-120AC-A/B`, `PN-125A/B`, `PN-120A/B`, and `GND-A/B` are high-confidence bus/control power connections. Dashed PLC, relay, annunciator, and junction-box links are kept in the plausible file.

Protection/instrumentation: CT/PT taps from `BUS-4160S1A/B` are high-confidence instrument taps. Dashed CT/PT-to-relay and relay-to-trip/interlock paths are plausible, because the dashed routing is visible but some endpoints share turns/crossings.

## Uncertain cases

- The upstream solid feed into `PN-MOV-A`/`PN-MOV-B` appears to bend from the safety MCC/fan feeder area; exact source endpoint is uncertain, so both MCC-to-panel and fan-to-panel variants are plausible.
- Dashed trip/control paths around `RELAY-86A`, `RELAY-86B`, `CB-TIE-41N`, and the Train B 4.16 kV breakers have visible geometry but ambiguous terminal ownership.
- `JB-1B0` and `JB-2B0` are visually corrected from OCR-like `O`; retain this as a raw-label correction rather than a guaranteed equipment-number convention.
- Long dashed control runs from the DC/control areas to MCC regions are included as plausible only, because the diagram shows train-level routing more clearly than terminal-by-terminal endpoints.
