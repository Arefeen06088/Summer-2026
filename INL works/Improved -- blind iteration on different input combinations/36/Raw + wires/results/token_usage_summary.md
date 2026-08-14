# Token Usage Estimate - Document 36, Iteration 1

OpenAI Responses input-token counting endpoint was not called because no API key was available. Actual usage objects were not exposed by the main/subagent tools.

Local estimate method: coarse text estimates plus image tokens as 85 + 170 * ceil(width / 512) * ceil(height / 512); reasoning tokens are low/expected/high estimates.

| document | iteration | low | expected | high | image/file input | cached input |
|---|---:|---:|---:|---:|---:|---:|
| 36 | 1 | 483755 | 496755 | 517055 | 449055 | 240550 |
