# Token Usage Estimate - Document 17, Iteration 1

OpenAI Responses input-token counting endpoint was not called because no API key was available. Actual usage objects were not exposed by the main/subagent tools.

Local estimate method: coarse text estimates plus image tokens as ceil(width / 32) * ceil(height / 32); reasoning tokens are low/expected/high estimates.

| document | iteration | low | expected | high | image/file input | cached input |
|---|---:|---:|---:|---:|---:|---:|
| 17 | 1 | 136834 | 150834 | 173034 | 100234 | 47510 |
