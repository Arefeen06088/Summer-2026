# Token Usage Estimate

No OpenAI API key was available, so the Responses input-token counting endpoint could not be used.
The subagent tool did not expose response usage objects.
Text estimates use ceil(characters/4); image estimates use a high-detail 512-tile approximation.

| Document | Iteration | Call | Agent | Input est | Image/file input est | Output low/exp/high | Reasoning low/exp/high | Total low/exp/high |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Raw + wires + junctions | 2 | main_group_estimate | Main Codex agent | 18551 | 18020 | 1200/2500/4500 | 3000/9000/22000 | 22751/30051/45051 |
| Raw + wires + junctions | 2 | diego_round_01 | Diego | 23991 | 23460 | 1700/3200/6400 | 3000/10000/28000 | 28691/37191/58391 |
| Raw + wires + junctions | 2 | jennifer_round_01 | Jennifer | 23154 | 22355 | 1300/2400/4800 | 2000/7000/18000 | 26454/32554/45954 |

Grouped totals for Raw + wires + junctions, iteration 2:
- Total input estimate: 65696
- Total tokens low/expected/high: 77896/99796/149396
