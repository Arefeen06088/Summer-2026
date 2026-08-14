# Token Usage Estimate Methodology

The exact OpenAI Responses `usage` objects were not exposed by the Codex
main-agent or subagent tools in this run, so this folder contains estimates.

The official OpenAI input token counting endpoint is `POST /v1/responses/input_tokens`.
It was not called because no API key was available in this environment. If an
API key is added later, the payloads represented by `model_call_token_estimates.csv`
should be sent to that endpoint for exact input counts.

Offline method used here:

- Text input tokens: low/expected/high ranges estimated from visible prompt and
  conversation payload sizes.
- Image/file input tokens: patch-count estimates from the actual local image
  dimensions in `image_token_estimates.csv`.
- Main-agent image views use high-detail estimates.
- Subagent `local_image` detail is not exposed; expected uses original-resolution
  patch estimates for completed visual subagent calls and high-detail estimates
  for the aborted retry.
- Cached input tokens and exact reasoning tokens are not exposed. Cached tokens
  are treated as 0 for totals; reasoning tokens are low/expected/high estimates.
- The aborted Jennifer retry is included because a subagent model call was
  spawned and then shut down before a useful final answer.

Official docs used:

- https://developers.openai.com/api/docs/guides/token-counting
- https://developers.openai.com/api/docs/guides/images-vision
- https://developers.openai.com/api/docs/guides/prompt-caching

Expected total tokens for document 3, iteration 1: 334781.
Low/high range: 151998 - 555680.
