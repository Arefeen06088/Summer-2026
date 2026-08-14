# Token Usage Estimate

No `OPENAI_API_KEY` is available, so the OpenAI Responses input-token counting endpoint was not called.
Official endpoint noted for future runs: `POST /v1/responses/input_tokens`.

| Document | Iteration | Low | Expected | High |
|---:|---:|---:|---:|---:|
| 11 | 1 | 56585 | 87450 | 125566 |

Fallback method: text prompt-size estimates plus image high-detail 512px tile estimates.
