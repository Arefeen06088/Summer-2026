# Document 11 Token Usage Estimate

No OpenAI API key was present, and the Codex/subagent runtime did not expose response usage objects. The official Responses input-token counting endpoint could therefore not be called.

Fallback method: text tokens are estimated as ceil(characters / 4). Image/file input tokens are estimated with a high-detail 512-tile method (fit within 2048 px, shortest side 768 px when larger, 85 base + 170 per tile). Low/high ranges apply multipliers around that expected value.

- Total expected input tokens: 85645
- Total expected image/file input tokens: 85510
- Total low / expected / high tokens including estimated visible output and reasoning: 103558 / 172593 / 310669

| Document | Iteration | Calls | Total Low | Total Expected | Total High |
|---|---:|---:|---:|---:|---:|
| 11 | 1 | 5 | 103558 | 172593 | 310669 |

Per-call details are in `token_usage_estimate.csv`.
