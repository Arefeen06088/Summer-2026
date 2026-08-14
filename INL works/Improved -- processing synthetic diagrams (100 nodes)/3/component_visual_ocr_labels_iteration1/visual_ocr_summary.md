# Component Detection / Visual OCR Summary - Document 3

Source folder: `C:\Asif_all_python_projects\INL\Improved -- processing synthetic diagrams (100 nodes)\3`

Input used: `synthetic_npp_100_component_electrical_schematic.png` only.

Strict leakage control:
- Connectivity matrix used: **no**
- Ground truth used: **no**
- Evaluator/metric files used: **no**

Counts:
- Physical components: **89**
- Logical/bus/ground nodes: **11**
- Combined physical + logical nodes: **100**

Visual style:
- Orange boxes mark physical devices.
- White banners with blue text mark physical component labels and are drawn after boxes so they stay on top.
- Green boxes/banners mark logical buses and ground in the combined overlay.

OCR note:
- Local Tesseract/pytesseract is unavailable in this environment, so this is a visual-OCR pass from the raw schematic image rather than an engine OCR pass.
- All labels are recorded with raw-image bbox evidence and no connectivity matrix access.
