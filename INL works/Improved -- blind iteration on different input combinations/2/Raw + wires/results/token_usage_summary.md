# Token Usage Estimate

No `OPENAI_API_KEY` was available, so the OpenAI Responses input-token counting endpoint was not called. The multi-agent tool did not expose usage objects, cached-token counts, or reasoning-token counts. Text estimate method: character-count fallback because tiktoken encoding load failed: SSLError. Image estimate method: 512-tile heuristic.

| Document | Iteration | Calls | Low total | Expected total | High total |
|---:|---:|---:|---:|---:|---:|
| 2 | 1 | 5 | 32435 | 93224 | 131716 |

| Call | Input expected | Image expected | Output expected | Total expected |
|---|---:|---:|---:|---:|
| main_agent_orchestration_and_artifact_generation | 32380 | 19380 | 7339 | 39719 |
| diego_round1_high_recall_extraction | 4215 | 3315 | 3700 | 7915 |
| jennifer_round1_precision_review | 25685 | 20485 | 3100 | 28785 |
| diego_round2_reconciliation | 7905 | 6205 | 2600 | 10505 |
| jennifer_round2_final_confirmation | 5750 | 5100 | 550 | 6300 |
