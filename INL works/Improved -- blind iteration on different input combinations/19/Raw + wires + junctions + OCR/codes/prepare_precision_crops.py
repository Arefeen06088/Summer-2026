from __future__ import annotations

import csv
from pathlib import Path

from PIL import Image


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\19\Raw + wires + junctions + OCR"
)
OUT = BASE / "precision_review_crops"

SOURCES = {
    "raw": BASE / "raw -- synthetic_npp_electrical_schematic_v3.png",
    "labels": BASE / "component_labels_banners_overlay.png",
    "nodes": BASE / "wire_nodes_overlay.png",
}

REGIONS = {
    "top_sources_all": (0, 0, 9200, 1250),
    "top_left_sources": (500, 150, 2700, 1350),
    "top_center_ties": (2500, 150, 6700, 1350),
    "top_right_sources": (6100, 150, 8800, 1350),
    "upper_left_480": (0, 1050, 3300, 2850),
    "upper_center_480": (3000, 1050, 6200, 2850),
    "upper_right_480": (5900, 1050, 9200, 2850),
    "middle_left_controls": (0, 2550, 3300, 4300),
    "middle_center_controls": (3000, 2550, 6200, 4300),
    "middle_right_controls": (5900, 2550, 9200, 4300),
    "lower_left": (0, 4000, 3300, 5600),
    "lower_center": (3000, 4000, 6200, 5600),
    "lower_right": (5900, 4000, 9200, 5600),
    "full_left_half": (0, 0, 4700, 5600),
    "full_right_half": (4500, 0, 9200, 5600),
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for source_name, source_path in SOURCES.items():
        with Image.open(source_path) as image:
            width, height = image.size
            for region_name, box in REGIONS.items():
                x1, y1, x2, y2 = box
                clipped = (max(0, x1), max(0, y1), min(width, x2), min(height, y2))
                crop = image.crop(clipped)
                out_path = OUT / f"{source_name}_{region_name}.png"
                crop.save(out_path)
                rows.append(
                    {
                        "source": source_path.name,
                        "region": region_name,
                        "x1": clipped[0],
                        "y1": clipped[1],
                        "x2": clipped[2],
                        "y2": clipped[3],
                        "output": out_path.name,
                    }
                )
    with (OUT / "crop_index.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["source", "region", "x1", "y1", "x2", "y2", "output"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} crops to {OUT}")


if __name__ == "__main__":
    main()
