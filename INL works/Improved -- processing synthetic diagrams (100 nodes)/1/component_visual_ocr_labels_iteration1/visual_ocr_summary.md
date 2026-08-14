# Component Detection / Visual OCR Summary - Document 1

Source folder: `C:\Asif_all_python_projects\INL\Improved -- processing synthetic diagrams (100 nodes)\1`

Input used: `schematic_image_clean_100_connected.png` only.

Strict leakage control:
- Connectivity matrix used: **no**
- Ground truth used: **no**
- Evaluator/metric files used: **no**

Counts:
- Physical components: **90**
- Logical/bus/region nodes: **17**
- Combined physical + logical nodes: **107**

Visual style:
- Orange boxes mark physical components.
- White banners with blue text mark physical component labels and are drawn after boxes so they stay on top.
- Green boxes/banners mark logical buses and regions in the combined overlay.

OCR note:
- Local Tesseract/pytesseract is unavailable in this environment, so this is a visual-OCR pass from the raw schematic image rather than an engine OCR pass.
- All labels are recorded with raw-image bbox evidence and no connectivity matrix access.
