# Token Usage Estimate

No OpenAI API key was available, and the subagent tool did not expose response usage objects.
Estimates use local tiktoken text counts when cached; otherwise they fall back to ceil(characters/4).
Image tokens use a high-detail 512-tile approximation.

| Document | Iteration | Call | Agent | Input est | Image/file input est | Output low/exp/high | Reasoning low/exp/high | Total low/exp/high |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Raw + wires + junctions | 1 | main_group_estimate | Main Codex agent | 18747 | 17961 | 1200/2500/4500 | 3000/9000/22000 | 22947/30247/45247 |
| Raw + wires + junctions | 1 | diego_round_01 | Diego | 10037 | 9945 | 1800/3500/7000 | 3000/10000/28000 | 14837/23537/45037 |
| Raw + wires + junctions | 1 | jennifer_round_01 | Jennifer | 17968 | 17255 | 1200/2200/4500 | 2000/7000/18000 | 21168/27168/40468 |

Grouped totals for Raw + wires + junctions, iteration 1:
- Total input estimate: 46752
- Total tokens low/expected/high: 58952/80952/130752
