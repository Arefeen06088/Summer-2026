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


def parse_bbox(row: dict[str, str]) -> tuple[int, int, int, int]:
    if row.get("bbox"):
        nums = [int(float(part.strip())) for part in row["bbox"].strip("[]").split(",")]
        return nums[0], nums[1], nums[2], nums[3]
    return (
        int(float(row["bbox_x1"])),
        int(float(row["bbox_y1"])),
        int(float(row["bbox_x2"])),
        int(float(row["bbox_y2"])),
    )


def label(row: dict[str, str]) -> str:
    return (row.get("final_label") or row.get("label") or row.get("stable_node_id") or "").strip()


def centroid(row: dict[str, str]) -> str:
    if row.get("centroid"):
        return row["centroid"]
    left, upper, right, lower = parse_bbox(row)
    return f"[{(left + right) / 2:.1f}, {(upper + lower) / 2:.1f}]"


def bbox_text(row: dict[str, str]) -> str:
    left, upper, right, lower = parse_bbox(row)
    return f"[{left}, {upper}, {right}, {lower}]"


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
    rows_sorted = sorted(rows, key=lambda r: (parse_bbox(r)[1], parse_bbox(r)[0], label(r)))
    counts = Counter(row["component_type"] for row in rows_sorted)
    md = [f"# Document {DOCUMENT} Component Index", "", "## Counts By Type", ""]
    for kind, count in sorted(counts.items()):
        md.append(f"- {kind}: {count}")
    md.extend(["", "## Labels By Position", ""])
    for row in rows_sorted:
        md.append(f"- {label(row)} | {row['component_type']} | id={row.get('stable_node_id', '')} | bbox={bbox_text(row)} | centroid={centroid(row)}")
    (CROPS / "component_index_by_position.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    with (CROPS / "component_index_by_position.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["final_label", "component_type", "source_id", "bbox", "centroid"])
        writer.writeheader()
        for row in rows_sorted:
            writer.writerow(
                {
                    "final_label": label(row),
                    "component_type": row["component_type"],
                    "source_id": row.get("stable_node_id", ""),
                    "bbox": bbox_text(row),
                    "centroid": centroid(row),
                }
            )


def main() -> None:
    CROPS.mkdir(parents=True, exist_ok=True)
    for prefix, source in SOURCES.items():
        with Image.open(source) as img:
            boxes = crop_boxes(img.width, img.height)
            for name, box in boxes.items():
                save_crop(img, f"{prefix}__{name}.png", box)
    rows = component_rows()
    write_index(rows)
    print(f"wrote {len(SOURCES) * len(boxes)} crops to {CROPS}")
    print(f"indexed {len(rows)} components")


if __name__ == "__main__":
    main()
