# Token Usage Estimate - Document 16, Iteration 1

OpenAI Responses input-token counting endpoint was not called because no API key was available. Actual usage objects were not exposed by the main/subagent tools.

Local estimate method:
- Text tokens: coarse manual estimate based on prompt/response size.
- Image/file tokens: ceil(width / 32) * ceil(height / 32) for each included local image.
- Reasoning tokens: unavailable, so low/expected/high ranges are estimated.
- Cached input tokens: estimated prior subagent visual packet for round-2 follow-ups.

| document | iteration | low | expected | high | image/file input | cached input |
|---|---:|---:|---:|---:|---:|---:|
| 16 | 1 | 105766 | 119066 | 140166 | 71226 | 32984 |
