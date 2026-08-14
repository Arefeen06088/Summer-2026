# Token Usage Estimate

Exact OpenAI Responses token counting and response usage objects were unavailable in this environment because no API key/usage metadata was exposed.

Method: local text tokens were estimated with `tiktoken`; image tokens were estimated from image dimensions with a high-detail 512px tile heuristic. Cached input and reasoning tokens are marked unavailable.

| Document | Iteration | Input text est | Image/file input est | Low total | Expected total | High total |
|---:|---:|---:|---:|---:|---:|---:|
| 41 | 1 | 2287 | 37910 | 51197 | 61497 | 77397 |
