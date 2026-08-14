# ESF Label Hypothetical Evaluation

Hypothetical operator-equivalence special case: ESF-PNL-A__DOC2-COMP-0079 and ESF-PNL-A__DOC2-COMP-0091 are evaluated as ESF-PNL-A; ESF-PNL-B__DOC2-COMP-0080 and ESF-PNL-B__DOC2-COMP-0092 are evaluated as ESF-PNL-B.

This file is supplemental and does not replace the primary evaluation results.

GT file: `C:\Asif_all_python_projects\INL\Evaluation\Train\2\synthetic_npp_connectivity_matrix.csv`
GT components: 100
GT edges: 115

## connectivity_matrix_balanced.csv

- Edge F1 after ESF alias: 0.684 (TP=65, FP=10, FN=50, precision=0.867, recall=0.565).
- Component F1 after ESF alias: 0.980 (TP=96, FP=0, FN=4, precision=1.000, recall=0.960).
- Remaining component misses: BUS-125DC-B, INV-1B, RPS-PNL-A, RPS-PNL-B.
- Remaining extra/wrong component labels: none.
- Remaining likely edge bottleneck: missing edges/connectivity (34); missing components (16).

## connectivity_matrix_balanced_plus.csv

- Edge F1 after ESF alias: 0.673 (TP=67, FP=17, FN=48, precision=0.798, recall=0.583).
- Component F1 after ESF alias: 0.980 (TP=96, FP=0, FN=4, precision=1.000, recall=0.960).
- Remaining component misses: BUS-125DC-B, INV-1B, RPS-PNL-A, RPS-PNL-B.
- Remaining extra/wrong component labels: none.
- Remaining likely edge bottleneck: missing edges/connectivity (32); extra/spurious edges (17).

## connectivity_matrix_high_precision.csv

- Edge F1 after ESF alias: 0.670 (TP=62, FP=8, FN=53, precision=0.886, recall=0.539).
- Component F1 after ESF alias: 0.980 (TP=96, FP=0, FN=4, precision=1.000, recall=0.960).
- Remaining component misses: BUS-125DC-B, INV-1B, RPS-PNL-A, RPS-PNL-B.
- Remaining extra/wrong component labels: none.
- Remaining likely edge bottleneck: missing edges/connectivity (37); missing components (16).

## connectivity_matrix_recall_favoring.csv

- Edge F1 after ESF alias: 0.676 (TP=72, FP=26, FN=43, precision=0.735, recall=0.626).
- Component F1 after ESF alias: 0.980 (TP=96, FP=0, FN=4, precision=1.000, recall=0.960).
- Remaining component misses: BUS-125DC-B, INV-1B, RPS-PNL-A, RPS-PNL-B.
- Remaining extra/wrong component labels: none.
- Remaining likely edge bottleneck: missing edges/connectivity (27); extra/spurious edges (26).
