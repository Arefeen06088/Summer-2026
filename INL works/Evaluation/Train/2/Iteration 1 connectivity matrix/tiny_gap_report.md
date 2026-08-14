# Tiny Gap Report

GT file: `C:\Asif_all_python_projects\INL\Evaluation\Train\2\synthetic_npp_connectivity_matrix.csv`
GT nodes: 100
GT edges: 115

## connectivity_matrix_balanced.csv

- Primary: TP=65, FP=12, FN=50, precision=0.844, recall=0.565, F1=0.677.
- Relaxed OCR: TP=65, FP=12, FN=50, precision=0.844, recall=0.565, F1=0.677, delta F1=0.000.
- 1. Main gap caused by missing/wrong component labels? Yes; 25 false-negative edges have at least one endpoint absent from predicted nodes.
- 2. Labels mostly correct but edges are missing? Yes; 25 false-negative edges have endpoints present but no predicted edge.
- 3. Are many extra edges present? Yes; 12 false-positive edges, 8 with endpoints that exist in GT.
- 4. Are components missing entirely? Yes; missing GT components: 6.
- 5. OCR-confusion improvement: F1 changes by 0.000; 0 primary errors look like OCR-confusion recoveries.
- Top likely bottleneck: missing components (25); missing edges/connectivity (25).

## connectivity_matrix_balanced_plus.csv

- Primary: TP=67, FP=19, FN=48, precision=0.779, recall=0.583, F1=0.667.
- Relaxed OCR: TP=67, FP=19, FN=48, precision=0.779, recall=0.583, F1=0.667, delta F1=0.000.
- 1. Main gap caused by missing/wrong component labels? Yes; 25 false-negative edges have at least one endpoint absent from predicted nodes.
- 2. Labels mostly correct but edges are missing? Yes; 23 false-negative edges have endpoints present but no predicted edge.
- 3. Are many extra edges present? Yes; 19 false-positive edges, 15 with endpoints that exist in GT.
- 4. Are components missing entirely? Yes; missing GT components: 6.
- 5. OCR-confusion improvement: F1 changes by 0.000; 0 primary errors look like OCR-confusion recoveries.
- Top likely bottleneck: missing components (25); missing edges/connectivity (23).

## connectivity_matrix_high_precision.csv

- Primary: TP=62, FP=8, FN=53, precision=0.886, recall=0.539, F1=0.670.
- Relaxed OCR: TP=62, FP=8, FN=53, precision=0.886, recall=0.539, F1=0.670, delta F1=0.000.
- 1. Main gap caused by missing/wrong component labels? Yes; 25 false-negative edges have at least one endpoint absent from predicted nodes.
- 2. Labels mostly correct but edges are missing? Yes; 28 false-negative edges have endpoints present but no predicted edge.
- 3. Are many extra edges present? No; 8 false-positive edges, 6 with endpoints that exist in GT.
- 4. Are components missing entirely? Yes; missing GT components: 6.
- 5. OCR-confusion improvement: F1 changes by 0.000; 0 primary errors look like OCR-confusion recoveries.
- Top likely bottleneck: missing edges/connectivity (28); missing components (25).

## connectivity_matrix_recall_favoring.csv

- Primary: TP=68, FP=32, FN=47, precision=0.680, recall=0.591, F1=0.633.
- Relaxed OCR: TP=68, FP=32, FN=47, precision=0.680, recall=0.591, F1=0.633, delta F1=0.000.
- 1. Main gap caused by missing/wrong component labels? Yes; 25 false-negative edges have at least one endpoint absent from predicted nodes.
- 2. Labels mostly correct but edges are missing? Yes; 22 false-negative edges have endpoints present but no predicted edge.
- 3. Are many extra edges present? Yes; 32 false-positive edges, 23 with endpoints that exist in GT.
- 4. Are components missing entirely? Yes; missing GT components: 6.
- 5. OCR-confusion improvement: F1 changes by 0.000; 0 primary errors look like OCR-confusion recoveries.
- Top likely bottleneck: missing components (25); extra/spurious edges (23).
