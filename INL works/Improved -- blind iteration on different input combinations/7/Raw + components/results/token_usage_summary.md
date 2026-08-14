# Token Usage Estimate

Document: 7
Iteration: 1

Official Responses token counting endpoint used: no
Reason: no API key was available in the environment (`OPENAI_API_KEY_PRESENT=false`), and the subagent tool responses did not expose usage objects.

Fallback method:
- Text tokens estimated from prompt/response size by rough token budgeting.
- Image/file input tokens estimated with a high-detail 512-pixel tile method using actual image dimensions.
- Low/high totals apply conservative multipliers to text, image, and output estimates.

| document | iteration | calls | total low | total expected | total high |
|---:|---:|---:|---:|---:|---:|
| 7 | 1 | 5 | 79281 | 105835 | 144927 |
