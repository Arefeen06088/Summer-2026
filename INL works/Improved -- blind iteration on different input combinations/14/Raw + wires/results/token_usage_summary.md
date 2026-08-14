# Token Usage Estimate - Document 14, Iteration 1

OpenAI Responses input-token counting endpoint was not called because no API key was available in this run. The estimate uses a local method:

- Text tokens: ceil(character_count / 4).
- Image/file tokens: ceil(width / 32) * ceil(height / 32), computed from each raw/crop image.
- Reasoning tokens: not exposed by the subagent tool, so low/expected/high ranges are estimated.
- Cached input tokens: estimated prior subagent visual context for round-2 follow-up calls.

Estimated totals:

| document | iteration | low | expected | high | image/file input | cached input |
|---|---:|---:|---:|---:|---:|---:|
| 14 | 1 | 399981 | 412731 | 509160 | 209011 | 169843 |

Actual usage objects were not available from the main or subagent model responses in this environment.
