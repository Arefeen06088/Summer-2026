# Token Usage Estimate

No `OPENAI_API_KEY` is available, so the OpenAI Responses input-token counting endpoint was not called.
Official endpoint noted for future runs: `POST /v1/responses/input_tokens`.

| Document | Iteration | Low | Expected | High |
|---:|---:|---:|---:|---:|
| 3 | 1 | 52127 | 80215 | 113585 |

Fallback method: text tokens via `tiktoken` when available, otherwise `ceil(characters / 4)`; image/file tokens via high-detail 512px tile estimate.
