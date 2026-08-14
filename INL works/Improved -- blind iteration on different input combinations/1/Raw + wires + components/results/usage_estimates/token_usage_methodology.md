# Token Usage Estimate Methodology

The exact OpenAI Responses `usage` objects were not exposed by the Codex main-agent or subagent tools in this run.

The official OpenAI input token counting endpoint is `POST /responses/input_tokens`.
It was not called because no API key was available in this environment. If an API key is added later, that endpoint should replace these estimates.

Offline method used here:

- Text tokens: approximate ranges from prompt/response character volume and visible payload size.
- Image/file input tokens: patch-count estimates from actual image dimensions.
- Main-agent image views used high-detail estimates because `view_image` was called with `detail=high`.
- Subagent `local_image` detail is not exposed; expected uses GPT-5.5-style omitted/auto-or-original behavior, with high-detail as the low bound.
- Cached input tokens and exact reasoning tokens are not exposed; cached tokens are treated as 0 for totals, and reasoning tokens are low/expected/high estimates.

Expected total tokens for document 1, iteration 1: 263391.
Low/high range: 123233 - 391126.
