from __future__ import annotations

import csv
from pathlib import Path

from PIL import Image


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\18\Raw + wires + junctions + OCR"
)
OUT = BASE / "precision_review_crops"

SOURCES = {
    "raw": BASE / "raw -- synthetic_nuclear_electrical_schematic_readable.png",
    "labels": BASE / "component_labels_banners_overlay.png",
    "nodes": BASE / "wire_nodes_overlay.png",
}

REGIONS = {
    "top_sources": (0, 0, 7000, 1150),
    "upper_bus_left": (0, 700, 2600, 2050),
    "upper_bus_center": (2200, 700, 5000, 2050),
    "upper_bus_right": (4500, 700, 7000, 2050),
    "middle_left_loads": (0, 1700, 2600, 3300),
    "middle_center_loads": (2200, 1700, 5000, 3300),
    "middle_right_loads": (4500, 1700, 7000, 3300),
    "lower_left_control": (0, 2950, 2600, 4400),
    "lower_center_control": (2200, 2950, 5000, 4400),
    "lower_right_control": (4500, 2950, 7000, 4400),
    "full_left_half": (0, 0, 3600, 4400),
    "full_right_half": (3400, 0, 7000, 4400),
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
