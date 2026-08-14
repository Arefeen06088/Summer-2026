from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\20\Raw + wires + junctions + OCR")
OUT = BASE / "precision_review_crops"

IMAGES = {
    "raw": BASE / "raw -- synthetic_npp_electrical_schematic_v3_label_clearance.png",
    "labels": BASE / "component_labels_banners_overlay.png",
    "nodes": BASE / "wire_nodes_overlay.png",
    "wires": BASE / "wires_mask_overlay.png",
}

# Coordinate crops are selected from the document-20 sheet size (6200 x 4300)
# to preserve enough context for bus ties, load branches, and lower control power.
CROPS = {
    "full_top": (0, 0, 6200, 950),
    "full_middle": (0, 800, 6200, 2600),
    "full_lower": (0, 2400, 6200, 4300),
    "left_top_sources": (0, 0, 2150, 1050),
    "center_top_buses": (1900, 0, 4300, 1050),
    "right_top_sources": (4050, 0, 6200, 1050),
    "left_mid": (0, 850, 2150, 2600),
    "center_mid": (1900, 850, 4300, 2600),
    "right_mid": (4050, 850, 6200, 2600),
    "left_lower": (0, 2450, 2150, 4300),
    "center_lower": (1900, 2450, 4300, 4300),
    "right_lower": (4050, 2450, 6200, 4300),
    "lower_controls_left": (0, 3000, 3100, 4300),
    "lower_controls_right": (3000, 3000, 6200, 4300),
    "full_left_half": (0, 0, 3100, 4300),
    "full_right_half": (3100, 0, 6200, 4300),
}


def parse_box(text: str) -> tuple[int, int, int, int]:
    vals = json.loads(text)
    return tuple(int(v) for v in vals)


def write_crops() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for image_name, image_path in IMAGES.items():
        im = Image.open(image_path)
        for crop_name, box in CROPS.items():
            im.crop(box).save(OUT / f"{image_name}__{crop_name}.png")


def write_component_index() -> None:
    path = BASE / "component_visual_ocr_labels.csv"
    with path.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    for row in rows:
        x1, y1, x2, y2 = parse_box(row["bbox"])
        row["_x1"] = x1
        row["_y1"] = y1
        row["_x2"] = x2
        row["_y2"] = y2

    rows.sort(key=lambda r: (r["_y1"], r["_x1"], r["final_label"]))
    type_counts = Counter(r["component_type"] for r in rows)

    index_path = OUT / "component_index_by_position.csv"
    with index_path.open("w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "final_label",
            "component_type",
            "bbox",
            "centroid",
            "confidence",
            "stable_node_id",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({name: row[name] for name in fieldnames})

    md_lines = [
        "# Document 20 Component Index",
        "",
        "## Counts By Type",
        "",
    ]
    md_lines.extend(f"- {kind}: {count}" for kind, count in sorted(type_counts.items()))
    md_lines.extend(["", "## Labels By Position", ""])
    for row in rows:
        md_lines.append(
            f"- {row['final_label']} | {row['component_type']} | bbox={row['bbox']} | centroid={row['centroid']}"
        )
    (OUT / "component_index_by_position.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")


def main() -> None:
    write_crops()
    write_component_index()
    print(f"wrote {len(CROPS) * len(IMAGES)} crops to {OUT}")


if __name__ == "__main__":
    main()
