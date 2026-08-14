from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

from PIL import Image

Image.MAX_IMAGE_PIXELS = None

BASE = Path(__file__).resolve().parents[1]
CROPS = BASE / "precision_review_crops"
DOCUMENT = BASE.parent.name


def raw_path() -> Path:
    matches = sorted(BASE.glob("raw -- *.png"))
    if not matches:
        raise FileNotFoundError("raw schematic image not found")
    return matches[0]


SOURCES = {
    "raw": raw_path(),
    "labels": BASE / "component_labels_banners_overlay.png",
    "nodes": BASE / "wire_nodes_overlay.png",
    "wires": BASE / "wires_mask_overlay.png",
}


def parse_bbox(value: str) -> tuple[int, int, int, int]:
    nums = [int(float(part.strip())) for part in value.strip("[]").split(",")]
    return nums[0], nums[1], nums[2], nums[3]


def crop_boxes(width: int, height: int) -> dict[str, tuple[int, int, int, int]]:
    half_w, half_h = width // 2, height // 2
    third_w, third_h = width // 3, height // 3
    boxes = {
        "full_sheet": (0, 0, width, height),
        "top_band": (0, 0, width, third_h),
        "middle_band": (0, third_h, width, 2 * third_h),
        "bottom_band": (0, 2 * third_h, width, height),
        "left_half": (0, 0, half_w, height),
        "right_half": (half_w, 0, width, height),
        "top_left": (0, 0, half_w, half_h),
        "top_right": (half_w, 0, width, half_h),
        "bottom_left": (0, half_h, half_w, height),
        "bottom_right": (half_w, half_h, width, height),
    }
    for row in range(3):
        y0 = row * third_h
        y1 = height if row == 2 else (row + 1) * third_h
        for col in range(3):
            x0 = col * third_w
            x1 = width if col == 2 else (col + 1) * third_w
            boxes[f"row{row + 1}_col{col + 1}"] = (x0, y0, x1, y1)
    return boxes


def save_crop(image: Image.Image, name: str, box: tuple[int, int, int, int], max_side: int = 2600) -> None:
    left, upper, right, lower = box
    crop = image.crop((max(0, left), max(0, upper), min(image.width, right), min(image.height, lower))).convert("RGB")
    scale = min(1.0, max_side / max(crop.width, crop.height))
    if scale < 1.0:
        crop = crop.resize((int(crop.width * scale), int(crop.height * scale)), Image.Resampling.LANCZOS)
    crop.save(CROPS / name)


def component_rows() -> list[dict[str, str]]:
    with (BASE / "component_visual_ocr_labels.csv").open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_index(rows: list[dict[str, str]]) -> None:
    rows_sorted = sorted(rows, key=lambda r: (parse_bbox(r["bbox"])[1], parse_bbox(r["bbox"])[0], r["final_label"]))
    counts = Counter(row["component_type"] for row in rows_sorted)
    md = [f"# Document {DOCUMENT} Component Index", "", "## Counts By Type", ""]
    for kind, count in sorted(counts.items()):
        md.append(f"- {kind}: {count}")
    md.extend(["", "## Labels By Position", ""])
    for row in rows_sorted:
        md.append(f"- {row['final_label']} | {row['component_type']} | bbox={row['bbox']} | centroid={row['centroid']}")
    (CROPS / "component_index_by_position.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    with (CROPS / "component_index_by_position.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["final_label", "component_type", "bbox", "centroid"])
        writer.writeheader()
        for row in rows_sorted:
            writer.writerow({key: row[key] for key in ["final_label", "component_type", "bbox", "centroid"]})


def main() -> None:
    CROPS.mkdir(parents=True, exist_ok=True)
    with Image.open(SOURCES["raw"]) as raw:
        boxes = crop_boxes(raw.width, raw.height)
    for prefix, source in SOURCES.items():
        with Image.open(source) as img:
            for name, box in boxes.items():
                save_crop(img, f"{prefix}__{name}.png", box)
    rows = component_rows()
    write_index(rows)
    print(f"wrote {len(SOURCES) * len(boxes)} crops to {CROPS}")
    print(f"indexed {len(rows)} components")


if __name__ == "__main__":
    main()
