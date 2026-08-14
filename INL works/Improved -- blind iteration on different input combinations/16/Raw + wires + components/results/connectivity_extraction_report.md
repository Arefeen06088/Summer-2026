# Document 16 Connectivity Extraction Report

## Scope

Resource folder: `C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\16\Raw + wires + components`

Only raw/visual schematic resources and derived visual aids in the document folder were used. No ground truth, answer files, GT-derived feedback, or off-the-shelf OCR were used.

## Saturated Result

- Final nodes: 178
- Final undirected edges: 183
- Matrix: symmetric, diagonal zero
- Review process: Diego R1 high-recall extraction -> Jennifer R1 precision correction -> Diego R2 agreement -> Jennifer R2 final agreement

## Major Jennifer Corrections Accepted

- Kept `BUS-480-B -> CB-31A-FDR30-B -> MCC-31A` because the filled junction is on the lower 480 V bus.
- Removed `METER-VM-1 -> BUS-125DC-A`; the vertical line does not show a clear filled junction to the upper DC bus.
- Replaced direct `MG-RPS-B -> BUS-120-RPS-B` with `MG-RPS-B -> RTD-RCS101 -> BUS-120-RPS-B`.
- Added/promoted `CP-ANN-01 -> JB-CONTAIN`; the dashed route visibly lands at `JB-CONTAIN`.
- Kept ambiguous dashed breaker/control rail candidates out of the final matrix.

## Validation

```json
{
  "nodes": 178,
  "edges": 183,
  "unique_undirected_edges": 183,
  "diagonal_zero": true,
  "symmetric": true,
  "missing_nodes": [],
  "isolated_nodes": []
}
```

## Final Files

- `final_connectivity_matrix.csv`
- `final_sparse_edges.csv`
- `round01_diego_matrix.csv`
- `round01_jennifer_matrix.csv`
- `round02_diego_matrix.csv`
- `round02_jennifer_matrix.csv`
- `uncertain_edges.csv`
- `token_usage_estimate.md`
