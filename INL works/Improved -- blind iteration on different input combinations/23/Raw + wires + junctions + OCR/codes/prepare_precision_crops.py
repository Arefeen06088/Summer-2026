from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

from PIL import Image

Image.MAX_IMAGE_PIXELS = None


BASE = Path(__file__).resolve().parents[1]
CROPS = BASE / "precision_review_crops"

SOURCES = {
    "raw": BASE / "raw -- synthetic_npp_electrical_schematic_ats_components_shifted_v18.png",
    "labels": BASE / "component_labels_banners_overlay.png",
    "nodes": BASE / "wire_nodes_overlay.png",
    "wires": BASE / "wires_mask_overlay.png",
}


def fit_box(box: tuple[int, int, int, int], width: int, height: int) -> tuple[int, int, int, int]:
    left, upper, right, lower = box
    return max(0, left), max(0, upper), min(width, right), min(height, lower)


def save_crop(img: Image.Image, name: str, box: tuple[int, int, int, int], max_side: int = 2600) -> None:
    crop = img.crop(fit_box(box, img.width, img.height)).convert("RGB")
    scale = min(1.0, max_side / max(crop.width, crop.height))
    if scale < 1.0:
        crop = crop.resize((int(crop.width * scale), int(crop.height * scale)), Image.Resampling.LANCZOS)
    crop.save(CROPS / name)


def parse_bbox(value: str) -> tuple[int, int, int, int]:
    nums = [int(float(part.strip())) for part in value.strip("[]").split(",")]
    return nums[0], nums[1], nums[2], nums[3]


def component_rows() -> list[dict[str, str]]:
    path = BASE / "component_visual_ocr_labels.csv"
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_index(rows: list[dict[str, str]]) -> None:
    rows_sorted = sorted(rows, key=lambda r: (parse_bbox(r["bbox"])[1], parse_bbox(r["bbox"])[0], r["final_label"]))
    counts = Counter(row["component_type"] for row in rows_sorted)
    md = ["# Document 23 Component Index", "", "## Counts By Type", ""]
    for kind, count in sorted(counts.items()):
        md.append(f"- {kind}: {count}")
    md.extend(["", "## Labels By Position", ""])
    for row in rows_sorted:
        md.append(
            f"- {row['final_label']} | {row['component_type']} | "
            f"bbox={row['bbox']} | centroid={row['centroid']}"
        )
    (CROPS / "component_index_by_position.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    with (CROPS / "component_index_by_position.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["final_label", "component_type", "bbox", "centroid"])
        writer.writeheader()
        for row in rows_sorted:
            writer.writerow(
                {
                    "final_label": row["final_label"],
                    "component_type": row["component_type"],
                    "bbox": row["bbox"],
                    "centroid": row["centroid"],
                }
            )


def main() -> None:
    CROPS.mkdir(parents=True, exist_ok=True)
    with Image.open(SOURCES["raw"]) as raw:
        width, height = raw.size

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
    for row_name, y0 in (("row1", 0), ("row2", third_h), ("row3", 2 * third_h)):
        y1 = third_h if row_name == "row1" else 2 * third_h if row_name == "row2" else height
        if row_name == "row2":
            y0 = third_h
        if row_name == "row3":
            y0 = 2 * third_h
        for col_idx, x0 in enumerate((0, third_w, 2 * third_w), start=1):
            x1 = width if col_idx == 3 else col_idx * third_w
            boxes[f"{row_name}_col{col_idx}"] = (x0, y0, x1, y1)

    for prefix, source in SOURCES.items():
        with Image.open(source) as img:
            for crop_name, box in boxes.items():
                save_crop(img, f"{prefix}__{crop_name}.png", box)

    rows = component_rows()
    write_index(rows)
    print(f"wrote {len(SOURCES) * len(boxes)} crops to {CROPS}")
    print(f"indexed {len(rows)} components")


if __name__ == "__main__":
    main()
