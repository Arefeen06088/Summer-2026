from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\22\Raw + wires + junctions + OCR")
OUT = BASE / "precision_review_crops"

IMAGES = {
    "raw": BASE / "raw -- synthetic_npp_electrical_schematic_clean.png",
    "labels": BASE / "component_labels_banners_overlay.png",
    "nodes": BASE / "wire_nodes_overlay.png",
    "wires": BASE / "wires_mask_overlay.png",
}

# Document 22 is 7200 x 5100. These overlapping crops preserve source,
# bus-tie, feeder, DC/control, and lower auxiliary context.
CROPS = {
    "full_top": (0, 0, 7200, 1200),
    "full_upper_mid": (0, 950, 7200, 2500),
    "full_lower_mid": (0, 2250, 7200, 3800),
    "full_bottom": (0, 3500, 7200, 5100),
    "top_left": (0, 0, 2500, 1300),
    "top_center": (2200, 0, 5000, 1300),
    "top_right": (4700, 0, 7200, 1300),
    "upper_left": (0, 900, 2500, 2600),
    "upper_center": (2200, 900, 5000, 2600),
    "upper_right": (4700, 900, 7200, 2600),
    "lower_left": (0, 2300, 2500, 4050),
    "lower_center": (2200, 2300, 5000, 4050),
    "lower_right": (4700, 2300, 7200, 4050),
    "bottom_left": (0, 3400, 2500, 5100),
    "bottom_center": (2200, 3400, 5000, 5100),
    "bottom_right": (4700, 3400, 7200, 5100),
    "full_left_half": (0, 0, 3600, 5100),
    "full_right_half": (3600, 0, 7200, 5100),
}


def parse_box(text: str) -> tuple[int, int, int, int]:
    vals = json.loads(text)
    return tuple(int(v) for v in vals)


def write_crops() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for image_name, image_path in IMAGES.items():
        image = Image.open(image_path)
        for crop_name, box in CROPS.items():
            image.crop(box).save(OUT / f"{image_name}__{crop_name}.png")


def write_component_index() -> None:
    with (BASE / "component_visual_ocr_labels.csv").open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    for row in rows:
        x1, y1, x2, y2 = parse_box(row["bbox"])
        row["_x1"] = x1
        row["_y1"] = y1
        row["_x2"] = x2
        row["_y2"] = y2

    rows.sort(key=lambda r: (r["_y1"], r["_x1"], r["final_label"]))
    type_counts = Counter(row["component_type"] for row in rows)

    with (OUT / "component_index_by_position.csv").open("w", newline="", encoding="utf-8") as f:
        fieldnames = ["final_label", "component_type", "bbox", "centroid", "confidence", "stable_node_id"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row[field] for field in fieldnames})

    lines = ["# Document 22 Component Index", "", "## Counts By Type", ""]
    lines.extend(f"- {kind}: {count}" for kind, count in sorted(type_counts.items()))
    lines.extend(["", "## Labels By Position", ""])
    for row in rows:
        lines.append(f"- {row['final_label']} | {row['component_type']} | bbox={row['bbox']} | centroid={row['centroid']}")
    (OUT / "component_index_by_position.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    write_crops()
    write_component_index()
    print(f"wrote {len(CROPS) * len(IMAGES)} crops to {OUT}")


if __name__ == "__main__":
    main()
