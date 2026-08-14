from __future__ import annotations

import csv
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\3")
INPUT = BASE / "Input resources"
OUT = BASE / "Codes and artifacts" / "iteration_1_inspection"

RAW = INPUT / "raw -- synthetic_npp_100_component_electrical_schematic.png"
VIS = INPUT / "component_visual_ocr_labels_iteration1"
DET = INPUT / "component_detection_iteration1"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def parse_bbox(text: str) -> tuple[int, int, int, int]:
    vals = [int(float(v.strip())) for v in text.split(",")]
    return vals[0], vals[1], vals[2], vals[3]


def label_font(size: int = 20):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except OSError:
        return ImageFont.load_default()


def make_scaled_overview(image_path: Path, out_path: Path, width: int = 2400) -> None:
    im = Image.open(image_path).convert("RGB")
    scale = width / im.width
    resized = im.resize((width, int(im.height * scale)), Image.Resampling.LANCZOS)
    resized.save(out_path)


def crop_region(raw: Image.Image, bbox: tuple[int, int, int, int], pad: int = 180) -> Image.Image:
    x1, y1, x2, y2 = bbox
    x1 = max(0, x1 - pad)
    y1 = max(0, y1 - pad)
    x2 = min(raw.width, x2 + pad)
    y2 = min(raw.height, y2 + pad)
    return raw.crop((x1, y1, x2, y2))


def contact_sheet(images: list[tuple[str, Image.Image]], out_path: Path, cols: int = 3, thumb_w: int = 900) -> None:
    if not images:
        return
    font = label_font(22)
    thumbs: list[tuple[str, Image.Image]] = []
    for title, im in images:
        scale = min(thumb_w / im.width, 1.0)
        thumb = im.resize((int(im.width * scale), int(im.height * scale)), Image.Resampling.LANCZOS)
        thumbs.append((title, thumb))
    cell_w = thumb_w
    cell_h = max(t.height for _, t in thumbs) + 56
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell_w, rows * cell_h), "white")
    draw = ImageDraw.Draw(sheet)
    for idx, (title, thumb) in enumerate(thumbs):
        x = (idx % cols) * cell_w
        y = (idx // cols) * cell_h
        draw.text((x + 8, y + 8), title, fill=(0, 0, 0), font=font)
        sheet.paste(thumb, (x + 8, y + 44))
    sheet.save(out_path)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    raw = Image.open(RAW).convert("RGB")
    make_scaled_overview(RAW, OUT / "full_raw_overview.png")
    make_scaled_overview(INPUT / "wires_mask_overlay.png", OUT / "full_wires_overlay_overview.png")
    make_scaled_overview(INPUT / "wire_nodes_overlay.png", OUT / "full_wire_nodes_overlay_overview.png")
    make_scaled_overview(VIS / "component_and_logical_labels_banners_overlay.png", OUT / "full_labels_overlay_overview.png")

    physical = read_csv(VIS / "component_visual_ocr_labels.csv")
    logical = read_csv(DET / "detected_logical_nodes.csv")
    with (OUT / "physical_components.txt").open("w", encoding="utf-8") as f:
        for row in physical:
            f.write(f"{row['normalized_text']}\t{row['bbox']}\n")
    with (OUT / "logical_nodes.txt").open("w", encoding="utf-8") as f:
        for row in logical:
            f.write(f"{row['normalized_label']}\t{row['type']}\t{row['bbox']}\n")

    # Contact sheet around logical nodes and regional working crops from the allowed detector output.
    logical_crops = []
    for row in logical:
        logical_crops.append((row["normalized_label"], crop_region(raw, parse_bbox(row["bbox"]), pad=260)))
    contact_sheet(logical_crops, OUT / "logical_nodes_contact_sheet.png", cols=3, thumb_w=760)

    regions = []
    for path in sorted((DET / "regional_work_crops").glob("*.png")):
        regions.append((path.stem, Image.open(path).convert("RGB")))
    contact_sheet(regions, OUT / "regional_work_crops_contact_sheet.png", cols=3, thumb_w=850)

    packets = []
    for path in sorted((VIS / "component_label_packets").glob("*.png")):
        packets.append((path.stem.replace("DET-COMP-", ""), Image.open(path).convert("RGB")))
    contact_sheet(packets, OUT / "component_label_packets_contact_sheet.png", cols=5, thumb_w=480)

    print(f"inspection assets written to {OUT}")


if __name__ == "__main__":
    main()
