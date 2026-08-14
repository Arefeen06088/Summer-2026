# Document 23 Connectivity Extraction

Source folder: `C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\23\Raw + wires + components`

Allowed resources used: raw schematic image, detected component overlay, wire mask/overlay, and generated visual crops under `results/visual_crops`.

GT/feedback use: none. OCR use: none.

## Multi-agent rounds

1. Diego high-recall extraction: proposed all visually/geometrically plausible nodes and edges.
2. Jennifer precision review: removed INST-to-GND overedges, corrected feeder sources, added BUS-24DC-C to DCS panel taps, and marked six main-to-480V-bus edges uncertain.
3. Diego consensus: agreed with Jennifer except he preferred including the six main-to-480V-bus links as functional inferred candidates.
4. Jennifer final: excluded the six main-to-480V-bus links from the hard matrix because the raw/wire crops show a visible gap.

## Final hard matrix policy

- Include directly visible high/medium confidence power, control/interlock, metering, and grounding connections.
- Treat named buses as nodes; components that tap a named bus connect to the bus node.
- Exclude section frames, title blocks, notes, reference drawings, and crop borders.
- Exclude functional-but-not-visually-hard-supported candidates from `final_connectivity_matrix.csv`; list them in `uncertain_or_excluded_edges.csv`.

Final node count: 200

Final hard edge count: 199

Primary result files:

- `final_connectivity_matrix.csv`
- `final_edges.csv`
- `round_01_diego_matrix.csv`
- `round_02_jennifer_matrix.csv`
- `round_03_diego_matrix.csv`
- `round_04_jennifer_final_matrix.csv`
- `uncertain_or_excluded_edges.csv`
- `token_usage_estimate.csv`

## Token estimate method

No OpenAI API key was available, so the Responses input-token counting endpoint could not be called. The local estimate uses:

- Text tokens: `ceil(characters / 4)`.
- Image/file tokens: low = 85 tokens per image, expected = approximate high-detail 512-tile heuristic after resizing to the common 2048/768 bounds, high = 1.35x expected.
- Output tokens: low/expected/high scenario estimates based on actual response lengths and round scope.
- Cached input and hidden reasoning tokens were not exposed by the local subagent tooling.
