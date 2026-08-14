# Visual OCR Component Label Summary - Document 2

Source image: `C:\Asif_all_python_projects\INL\Processing Simpler synthetic data\2\synthetic_npp_electrical_schematic_v2(1).png`

This pass visually reads labels from the raw schematic and places compact solid banners near the detected component boxes. No external OCR, connectivity matrix CSV, GT, or evaluation files were used.

Physical component labels: 47
Component + logical labels: 71

Primary output:
- `C:\Asif_all_python_projects\INL\Processing Simpler synthetic data\2\component_visual_ocr_labels_iteration1\component_labels_banners_overlay.png`

Useful companion output:
- `C:\Asif_all_python_projects\INL\Processing Simpler synthetic data\2\component_visual_ocr_labels_iteration1\component_and_logical_labels_banners_overlay.png`

Data outputs:
- `C:\Asif_all_python_projects\INL\Processing Simpler synthetic data\2\component_visual_ocr_labels_iteration1\component_visual_ocr_labels.csv`
- `C:\Asif_all_python_projects\INL\Processing Simpler synthetic data\2\component_visual_ocr_labels_iteration1\component_and_logical_visual_ocr_labels.csv`
- `C:\Asif_all_python_projects\INL\Processing Simpler synthetic data\2\component_visual_ocr_labels_iteration1\component_label_evidence_log.csv`
- `C:\Asif_all_python_projects\INL\Processing Simpler synthetic data\2\component_visual_ocr_labels_iteration1\generated_visual_ocr_artifacts\ocr_results.csv`
- `C:\Asif_all_python_projects\INL\Processing Simpler synthetic data\2\component_visual_ocr_labels_iteration1\generated_visual_ocr_artifacts\ocr_text.txt`
- `C:\Asif_all_python_projects\INL\Processing Simpler synthetic data\2\component_visual_ocr_labels_iteration1\generated_visual_ocr_artifacts\ocr_text_layer.png`

Notes:
- Orange boxes mark physical components.
- Green boxes in the combined overlay mark visually labeled buses/ports/control labels/logical nodes.
- Solid banners contain the visually read labels.
- Banner placement is logged in the CSV.
