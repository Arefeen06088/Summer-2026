# Token Usage Estimate

No `OPENAI_API_KEY` was present, so the Responses input-token counting endpoint could not be called.
Actual usage objects were not exposed by the Codex subagent tool responses.
Text estimates use local tokenizer assets when available, otherwise a chars/4 fallback; image/file estimates are local approximations.

| Document | Iteration | Call | Agent | Text In | Image/File In Tile Est | Output Est | Expected Total | Status |
|---|---:|---|---|---:|---:|---:|---:|---|
| 18 | 1 | main_agent_aggregate | main | 683 | 33915 | 520 | 35118 | completed_estimated |
| 18 | 1 | diego_round_01 | Diego | 2732 | 13260 | 2600 | 18592 | completed |
| 18 | 1 | jennifer_round_02 | Jennifer | 3030 | 13345 | 2500 | 18875 | completed |
| 18 | 1 | diego_round_03 | Diego | 1830 | 7310 | 320 | 9460 | completed |
| 18 | 1 | jennifer_round_04a_interrupted | Jennifer | 444 | 4420 | 0 | 4864 | interrupted_no_matrix |
| 18 | 1 | jennifer_round_04b_final | Jennifer | 544 | 7735 | 520 | 8799 | completed_final |

Expected total, tile estimate: 95708
High total, patch estimate: 138019

Low/expected/high output estimates are in `token_usage_estimates.csv`.
