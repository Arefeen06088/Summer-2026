# Document 37 Round 02 Jennifer Notes

Scope used only resources inside `C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\37\Raw + wires + junctions + OCR`: the raw schematic, provided overlays, `component_visual_ocr_labels.csv`, `wire_nodes.csv`, Diego round01 files, and the allowed precision review crops. No GT, evaluator output, off-the-shelf OCR, or files outside the allowed folder were used. The raw schematic was treated as authoritative; overlays and CSVs were secondary aids.

## Round 02 Summary

- Nodes: retained Diego's 55 included nodes unchanged: 47 physical components plus 8 logical buses.
- Edges: retained 54 included edges after removing two low-confidence lower dashed control routes from Diego round01.
- Additions versus Diego: none.
- Removals versus Diego: `PAN-RPS-A -- PLC-ESF` and `PLC-ESF -- PAN-RPS-B`.

## Precision Checks

1. Lower dashed PAN/PLC routes:
   - Removed `PAN-RPS-A -- PLC-ESF`. In `raw__row3_col2.png` and `raw__bottom_left.png`, C03 visibly forms a lower dashed cable-tray/routing path that reaches the RPS A panel area, but the opposite side runs into the central dashed routing/partition area adjacent to PLC-ESF rather than a clear PLC-ESF terminal or component boundary. The wire-node overlay does not provide a component-to-component endpoint pair.
   - Removed `PLC-ESF -- PAN-RPS-B`. In `raw__row3_col2.png` and `raw__bottom_right.png`, C06 is drawn as a dashed functional routing box/path near PLC-ESF and PAN-RPS-B, but it does not show a clear visual termination on both components. The nearby note says cable tray routing is shown functionally and terminal numbers are typical, so I treated this as ambiguous routing, not a supported graph edge.

2. C02/C05 center dashed lines:
   - No C02 or C05 edges were added. In `raw__middle_band.png`, `raw__bottom_left.png`, and `raw__bottom_right.png`, C02/C05 sit on vertical dashed lines beside the central divider/battery area and do not clearly terminate on labeled components. They remain noted as ambiguous routing/partition lines.

3. ATS permissive controls:
   - Kept `ATS-1A -- RELAY-K12A`. C01 is a dashed control line visibly running from ATS-1A to RELAY-K12A.
   - Kept `RELAY-K12B -- ATS-1B`. C04 is a dashed control line visibly running from RELAY-K12B to ATS-1B.

4. Top/source topology:
   - Confirmed the offsite/source sequence `AUX-TR-1A -- CB-101 -- GRID-345 -- CB-102 -- AUX-TR-1B`.
   - Confirmed transformer taps to `BUS-6KA` and `BUS-6KB`, and the tie path `BUS-6KA -- CB-TIE-6K -- BUS-6KB`.
   - Confirmed the train A path `BUS-6KA -- CB-103A -- SWGR-1EA -- ATS-1A -- TR-480A -- BUS-480A`, plus `DG-1A -- CB-DG1A -- SWGR-1EA`.
   - Confirmed the train B path `BUS-6KB -- CB-103B -- SWGR-1EB -- ATS-1B -- TR-480B -- BUS-480B`, plus `DG-1B -- CB-DG1B -- SWGR-1EB`.
   - No direct `GRID-345 -- CB-TIE-6K` or cross-train shortcut was visually supported.

5. Lower AC/DC topology:
   - Confirmed MCC feeders from `BUS-480A`/`BUS-480B` to each MCC and from each MCC to its six visible loads.
   - Confirmed charger, battery, DC bus, ground, inverter, and 120 VAC bus paths on both trains using visible solid conductors and filled bus taps.
   - Confirmed `BUS-120A` feeds `PAN-RPS-A` and `INST-RACK-A`, and `BUS-120B` feeds `PAN-RPS-B` and `INST-RACK-B`.
   - No connectivity was inferred through visual crossings or dashed routing unless a supported terminal-to-terminal path was visible.

6. Logical bus nodes:
   - Retained Diego's bus nodes because each has a visible busbar and label: `BUS-6KA`, `BUS-6KB`, `BUS-480A`, `BUS-480B`, `BUS-125DCA`, `BUS-125DCB`, `BUS-120A`, and `BUS-120B`.
   - I did not add logical nodes for dashed cable-tray labels or division boundaries because they are not component/bus terminals.

## Remaining Ambiguities

- C03 and C06 may represent functional cable-tray/control routing among the lower ESF/RPS panels, but the raw drawing does not show enough terminal evidence to assign specific component-to-component edges.
- C02 and C05 remain visually ambiguous vertical dashed routes near the central battery/ESF area, with no clear labeled component termination.

## Saturation Recommendation

This graph appears saturated for visually supported connectivity under the current evidence rules. Further expansion should require a clearer terminal drawing or source document for the lower dashed control/cable-tray routes; otherwise, do not add the removed PAN/PLC or C02/C05 edges.
