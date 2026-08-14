# Document 40 Round 01 Diego Notes

Scope followed: only files in this document-40 folder were used. The raw schematic was treated as authoritative. The provided component labels overlays wire-node CSV and local crops were used only as visual aids. No off-the-shelf OCR was used.

## Inclusion Rules

- Included all visually identified physical components from the local component label CSV when they had a drawn symbol or terminal.
- Included real electrical buses: `SWGR-21A`, `SWGR-21B`, `MCC-21A-480V-3PH`, `MCC-21B-480V-3PH`, `DC-BUS-21A`, and `DC-BUS-21B`.
- Kept the physical MCC labels `MCC-21A` and `MCC-21B` as components and connected each to its internal busbar node with `internal_bus` edges.
- Excluded title or route labels: train/channel boundaries source notes control lane captions and `VOLTAGE-SIG-A/B`.
- Crossings without dots were treated as non-connections. The explicit `NO DOT = NO JUNCTION` callout near MOV-RWST21A supports excluding any edge between the voltage signal route and the MOV power feeder.

## Main Topology Read

Train A normal/alternate sources feed `ATS-21A` from `DG-21A` and `UAT-2A` through `DS-21A`; `ATS-21A` feeds `SWGR-21A`. `SWGR-21A` feeds `CB-21A1`, `TR-21A`, and then the MCC path. Train B mirrors this through `SAT-2B`, `DG-21B`, `ATS-21B`, `SWGR-21B`, `CB-21B1`, and `TR-21B`. The two switchgear buses are joined only through `TIE-BKR-21AB`.

The MCC busbars feed the pump fan MOV and CPT loads. The CPT transformers feed AC panels which feed rectifier/chargers. Rectifiers batteries and inverters are tied to the train-specific 125 VDC busbars.

The RPS/control network is represented by direct endpoint edges rather than route-label nodes. LOCA signals pass through junction boxes to RPS panels. CT and VT dashed signal routes enter the RPS panels. RPS panels connect to inverters and relay chains. The 86 relays trip the associated pump breakers through the dash-dot trip-control paths.

## Lower-Confidence Included Edges

- `CT-21A` -- `RPS-PNL-A`: dashed CT signal route is visually continuous but the long vertical routing is inferred across crops.
- `VT-21A` -- `RPS-PNL-A`: voltage signal route label is excluded so the endpoint edge represents the continuous dashed route.
- `RELAY-86A` -- `CB-MPA1`: trip-control route is visually present but long and routed around the lower control lane.
- `CT-21B` -- `RPS-PNL-B`: dashed CT signal route is visually continuous but the long vertical routing is inferred across crops.
- `VT-21B` -- `RPS-PNL-B`: voltage signal route label is excluded so the endpoint edge represents the continuous dashed route.
- `RELAY-86B` -- `CB-MPB1`: trip-control route is visually present but long and routed around the lower control lane.
