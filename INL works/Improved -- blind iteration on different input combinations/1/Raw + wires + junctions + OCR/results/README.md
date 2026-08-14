# Connectivity Extraction Results

Final selected file: `round_04_jennifer_final_matrix.csv`, duplicated as `final_connectivity_matrix.csv`.

Interpretation: closed solid power/DC connectivity. Off-sheet terminals are included. Normally-open bus/DC ties and dashed/dotted control/instrumentation links are retained only in `final_excluded_or_nonclosed_edges.csv` and are encoded as 0 in the final matrix.

Token accounting note: no OpenAI API key or model usage object was available. Local `tiktoken` was installed, but tokenizer-data download failed SSL verification, so local text token counts use the transparent `chars_div_4` fallback and image counts use a high-detail tiling estimate.

Rows and columns use the same ordered component/node names. Matrices are symmetric and have zero diagonals.
