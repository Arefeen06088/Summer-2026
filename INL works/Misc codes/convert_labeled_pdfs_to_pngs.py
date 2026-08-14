import os

try:
    import fitz  # PyMuPDF
except ImportError:  # pragma: no cover
    raise SystemExit(
        "PyMuPDF (fitz) is not installed. Install it with "
        "`pip install pymupdf` inside your environment."
    )

BASE_LABELED_PDF_DIR = r"C:\Asif_all_python_projects\INL\Labeled_Real_diagrams"
BASE_LAYER_DIR = r"C:\Asif_all_python_projects\INL\Labeled Real Diagram Layers"


def get_source_dirs(base_dir: str):
    """Return sorted list of subdirectory names under base_dir."""
    entries = []
    for name in os.listdir(base_dir):
        full = os.path.join(base_dir, name)
        if os.path.isdir(full):
            entries.append(name)
    entries.sort()
    return entries


def find_raw_dirs(layer_dir: str):
    """Find subdirectories whose name contains 'raw' (case-insensitive)."""
    if not os.path.isdir(layer_dir):
        print(f"[WARN] Layer dir does not exist: {layer_dir}")
        return []

    raw_dirs = []
    for name in os.listdir(layer_dir):
        full = os.path.join(layer_dir, name)
        if os.path.isdir(full) and "raw" in name.lower():
            raw_dirs.append(full)

    if not raw_dirs:
        print(f"[WARN] No 'Raw' dirs found under {layer_dir}")

    return raw_dirs


def convert_pdf_to_pngs(pdf_path: str, output_dirs):
    """Convert all pages of a PDF to high-resolution PNGs saved into each output dir."""
    doc = fitz.open(pdf_path)
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]

    # Use a high DPI so the PNGs retain as much clarity as possible.
    # This does not downscale; it just rasterizes the original page
    # at a finer grid (more pixels per inch).
    target_dpi = 600

    for page_index in range(doc.page_count):
        page = doc[page_index]
        pix = page.get_pixmap(dpi=target_dpi)
        filename = f"{base_name}_page_{page_index + 1:03d}.png"

        for out_dir in output_dirs:
            os.makedirs(out_dir, exist_ok=True)
            out_path = os.path.join(out_dir, filename)
            pix.save(out_path)

    doc.close()


def main():
    if not os.path.isdir(BASE_LABELED_PDF_DIR):
        raise SystemExit(f"Source PDF base dir not found: {BASE_LABELED_PDF_DIR}")
    if not os.path.isdir(BASE_LAYER_DIR):
        raise SystemExit(f"Layer base dir not found: {BASE_LAYER_DIR}")

    source_dirs = get_source_dirs(BASE_LABELED_PDF_DIR)
    if len(source_dirs) < 6:
        print(
            f"[WARN] Expected at least 6 source folders, "
            f"found {len(source_dirs)}: {source_dirs}"
        )

    # Map the six labeled-diagram folders to layer indices 1-6
    print("[INFO] Source folder to layer index mapping:")
    for idx, dirname in enumerate(source_dirs[:6], start=1):
        print(f"  {dirname} -> {idx}")

    for idx, dirname in enumerate(source_dirs[:6], start=1):
        pdf_dir = os.path.join(BASE_LABELED_PDF_DIR, dirname)
        layer_dir = os.path.join(BASE_LAYER_DIR, str(idx))

        pdf_files = [
            f for f in os.listdir(pdf_dir)
            if f.lower().endswith(".pdf")
        ]

        if not pdf_files:
            print(f"[SKIP] No PDFs found in {pdf_dir}")
            continue

        raw_dirs = find_raw_dirs(layer_dir)
        if not raw_dirs:
            print(f"[SKIP] No Raw* dirs to write into for {layer_dir}")
            continue

        for pdf_name in pdf_files:
            pdf_path = os.path.join(pdf_dir, pdf_name)
            print(f"[INFO] Converting {pdf_path} -> Raw* dirs under {layer_dir}")
            convert_pdf_to_pngs(pdf_path, raw_dirs)


if __name__ == "__main__":
    main()
