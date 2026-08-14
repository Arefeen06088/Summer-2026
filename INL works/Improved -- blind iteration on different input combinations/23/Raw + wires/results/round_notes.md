# Document 23 Round Notes

## Scope
- Used only resources under `Raw + wires`.
- No ground-truth file or GT-derived feedback was used.
- No OCR engine was used. Labels were read by visual inspection.

## Diego Round 1 - High Recall
Diego identified the 4160/source chains, ESF buses, ATS/DG feeds, six 480 V load centers (`1A`, `1C`, `1B`, `2A`, `2C`, `2B`), local MCC/load groups, DC/UPS buses, and lower control panels. His high-recall graph included dashed control/instrument candidates and initially placed `CB-1C-FDR` on `BUS-4160-ESF-A`.

## Jennifer Round 1 - Precision Refinement
Jennifer corrected `CB-1C-FDR` to `BUS-4160-A`, kept `CB-2A-FDR` and `CB-2C-FDR` on `BUS-4160-ESF-A`, kept `CB-2B-FDR` on `BUS-4160-ESF-B`, and confirmed `CB-DC-B` feeds from `BUS-480-2B`. She rejected dashed-only relay, metering, PT, instrument, DCS/JB, and KTIE/RADMON chains from the binary connectivity matrix. She confirmed labels `BUS-24DC-C` and `JB-CTRL/A`.

## Diego Round 2 - Recall Check
Diego accepted the dashed-edge removals and identified supported solid/grounding taps that Jennifer's first refinement had left out: 4160 bus grounds, 125 VDC battery/charger/ground taps, and 120 VAC fuse/RPS-panel drops.

## Jennifer Round 2 - Saturated Final
Jennifer accepted Diego Round 2's remaining supported taps and declared the extraction saturated. Final graph includes solid power lines and light-solid grounding. Dashed-only visual components are retained as visible nodes but isolated unless they also have a solid/grounding edge.
