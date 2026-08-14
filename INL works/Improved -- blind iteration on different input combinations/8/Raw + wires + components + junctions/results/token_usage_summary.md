# Document 8 Token Usage Estimate

No `OPENAI_API_KEY` was present, so the official `POST /v1/responses/input_tokens` endpoint could not be called.
Usage objects for the Codex main-agent/subagent wrapper calls were not exposed in this environment.

Local method:
- Text: `tiktoken` with `o200k_base` if available; otherwise deterministic `ceil(characters / 4)` fallback.
- Image low: 70 tokens per image as a low-detail floor.
- Image expected: `ceil(width / 32) * ceil(height / 32)` original patch count, matching GPT-5.6 `auto/original` guidance.
- Image high: original patch count plus 15 percent and a small per-image overhead allowance.
- `image_tile_high_reference_tokens` is included as a separate GPT-5 tile-based comparison column.

Total low estimate: 17,937 tokens
Total expected estimate: 304,516 tokens
Total high estimate: 369,617 tokens

See `model_call_token_estimates.csv` for per-call details.

Official references:
- https://developers.openai.com/api/docs/guides/token-counting
- https://developers.openai.com/api/docs/guides/images-vision
