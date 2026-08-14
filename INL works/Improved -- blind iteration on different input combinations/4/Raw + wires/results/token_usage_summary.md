# Token Usage Estimate

No `OPENAI_API_KEY` was available, so the OpenAI Responses input-token counting endpoint was not called. The multi-agent tool did not return usage objects, cached-token counts, or reasoning-token counts. Text estimate method: character-count fallback because tiktoken encoding load failed: SSLError. Image estimate method: 512-tile heuristic.

| Document | Iteration | Calls | Low total | Expected total | High total |
|---:|---:|---:|---:|---:|---:|
| 4 | 1 | 5 | 36456 | 92146 | 129251 |

| Call | Input expected | Image expected | Output expected | Total expected |
|---|---:|---:|---:|---:|
| main_agent_orchestration_and_artifact_generation | 29340 | 17340 | 8426 | 37766 |
| diego_round1_high_recall_extraction | 4215 | 3315 | 4200 | 8415 |
| jennifer_round1_precision_review | 19625 | 14025 | 3300 | 22925 |
| diego_round2_reconciliation | 10530 | 6630 | 3600 | 14130 |
| jennifer_round2_final_confirmation | 8210 | 7310 | 700 | 8910 |
