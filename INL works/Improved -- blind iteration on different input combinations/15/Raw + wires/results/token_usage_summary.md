# Token Usage Estimate - Document 15, Iteration 1

OpenAI Responses input-token counting endpoint was not called because no API key was available. Actual usage objects were not exposed by the main/subagent tools.

Local estimate method:
- Text tokens: ceil(character_count / 4).
- Image/file tokens: ceil(width / 32) * ceil(height / 32), computed from each raw/crop image.
- Reasoning tokens: unavailable, so low/expected/high ranges are estimated.
- Cached input tokens: estimated prior subagent context for round-2 follow-ups.

| document | iteration | low | expected | high | image/file input | cached input |
|---|---:|---:|---:|---:|---:|---:|
| 15 | 1 | 549130 | 562530 | 697210 | 314009 | 212075 |
