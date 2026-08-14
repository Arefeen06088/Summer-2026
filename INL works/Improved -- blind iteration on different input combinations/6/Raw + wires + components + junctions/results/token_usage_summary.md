# Document 6 Token Usage Estimate

No `OPENAI_API_KEY` was present, so `/v1/responses/input_tokens` could not be called.
Usage objects for Codex main-agent/subagent wrapper calls were not exposed by the tool environment.

Local method:
- Text: `tiktoken` with `o200k_base` when available; deterministic `ceil(characters/4)` fallback if local encoder data cannot load.
- Image low estimate: GPT-5 low-detail base, 70 tokens/image.
- Image expected estimate: GPT-5 high-detail tile formula, 70 base + 140 per 512px tile after documented resizing.
- Image high estimate: 32px original patch count, a conservative proxy for GPT-5.6 original/auto behavior on large images.

Total low estimate: 22,240 tokens
Total expected estimate: 81,299 tokens
Total high estimate: 570,701 tokens

See `model_call_token_estimates.csv` for per-call details.
