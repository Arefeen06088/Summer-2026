# Case 13 Extraction Notes

Allowed resources: no `Input resources` folder existed, so extraction used only the raw schematic PNG and crops derived directly from that PNG.

Final graph includes the four train power/control component networks A-D, source/tie equipment, DC/UPS equipment, PP-to-UPS solid lower feeders, JB-to-DC-bus dashed links, and relay-to-breaker dashed control links.

Excluded from final matrix: `LOCAL I/O-*`, `ESFAS`, continuation arrow text, and grounding labels/symbols. These were treated as labels, off-sheet references, or separate grounding topology rather than supported primary component nodes.
