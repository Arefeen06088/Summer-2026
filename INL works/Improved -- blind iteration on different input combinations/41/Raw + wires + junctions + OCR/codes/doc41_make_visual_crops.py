from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

from PIL import Image


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\41\Raw + wires + junctions + OCR"
)
CODES = BASE / "codes"
RESULTS = BASE / "results"
CROPS = BASE / "precision_review_crops"


def raw_path() -> Path:
    matches = sorted(BASE.glob("raw -- *.png"))
    if not matches:
        raise FileNotFoundError(f"No raw schematic found in {BASE}")
    return matches[0]


SOURCES = {
    "raw": raw_path(),
    "labels": BASE / "component_labels_banners_overlay.png",
    "wires": BASE / "wires_mask_overlay.png",
    "nodes": BASE / "wire_nodes_overlay.png",
}


def parse_bbox(row: dict[str, str]) -> tuple[int, int, int, int]:
    text = (row.get("bbox") or "").strip()
    if text:
        nums = [int(float(part.strip())) for part in text.strip("[]").split(",")]
        return nums[0], nums[1], nums[2], nums[3]
    return (
        int(float(row["bbox_x1"])),
        int(float(row["bbox_y1"])),
        int(float(row["bbox_x2"])),
        int(float(row["bbox_y2"])),
    )


def label(row: dict[str, str]) -> str:
    return (row.get("final_label") or row.get("label") or row.get("stable_node_id") or "").strip()


def component_rows() -> list[dict[str, str]]:
    with (BASE / "component_visual_ocr_labels.csv").open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def save_crop(image: Image.Image, box: tuple[int, int, int, int], out: Path, max_side: int = 2600) -> dict[str, object]:
    left, top, right, bottom = box
    crop = image.crop((max(0, left), max(0, top), min(image.width, right), min(image.height, bottom))).convert("RGB")
    scale = min(1.0, max_side / max(crop.size))
    if scale < 1.0:
        crop = crop.resize((int(crop.width * scale), int(crop.height * scale)), Image.Resampling.LANCZOS)
    crop.save(out)
    return {"file": str(out), "box": [left, top, right, bottom], "size": list(crop.size)}


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
        "focus_top_distribution": (120, 180, width - 120, 1050),
        "focus_middle_distribution": (120, 850, width - 120, 2050),
        "focus_lower_distribution": (120, 1850, width - 120, height - 140),
        "focus_dc_controls": (150, 2350, width - 150, height - 180),
    }
    for row in range(3):
        y0 = row * third_h
        y1 = height if row == 2 else (row + 1) * third_h
        for col in range(3):
            x0 = col * third_w
            x1 = width if col == 2 else (col + 1) * third_w
            boxes[f"row{row + 1}_col{col + 1}"] = (x0, y0, x1, y1)
    return boxes


def write_component_index(rows: list[dict[str, str]]) -> None:
    rows_sorted = sorted(rows, key=lambda r: (parse_bbox(r)[1], parse_bbox(r)[0], label(r)))
    counts = Counter(row.get("component_type", "") for row in rows_sorted)
    lines = ["# Document 41 Component Index", "", "## Counts By Type", ""]
    for kind, count in sorted(counts.items()):
        lines.append(f"- {kind}: {count}")
    lines.extend(["", "## Labels By Position", ""])
    for row in rows_sorted:
        lines.append(
            f"- {label(row)} | {row.get('component_type', '')} | {row.get('node_kind', '')} | "
            f"id={row.get('stable_node_id', '')} | bbox={row.get('bbox', '')} | centroid={row.get('centroid', '')}"
        )
    (CROPS / "component_index_by_position.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    with (CROPS / "component_index_by_position.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["final_label", "component_type", "node_kind", "source_id", "bbox", "centroid"],
        )
        writer.writeheader()
        for row in rows_sorted:
            writer.writerow(
                {
                    "final_label": label(row),
                    "component_type": row.get("component_type", ""),
                    "node_kind": row.get("node_kind", ""),
                    "source_id": row.get("stable_node_id", ""),
                    "bbox": row.get("bbox", ""),
                    "centroid": row.get("centroid", ""),
                }
            )


def main() -> None:
    CODES.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)
    CROPS.mkdir(parents=True, exist_ok=True)
    (CODES / "doc41_make_visual_crops.py").write_text(Path(__file__).read_text(encoding="utf-8"), encoding="utf-8")

    manifest: list[dict[str, object]] = []
    for source_name, source_path in SOURCES.items():
        with Image.open(source_path) as image:
            for crop_name, box in crop_boxes(image.width, image.height).items():
                out = CROPS / f"{source_name}__{crop_name}.png"
                entry = save_crop(image, box, out)
                entry.update({"source": source_name, "crop": crop_name})
                manifest.append(entry)

    rows = component_rows()
    write_component_index(rows)
    (CROPS / "crop_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps({"base": str(BASE), "crops": len(manifest), "components": len(rows)}, indent=2))


if __name__ == "__main__":
    main()
