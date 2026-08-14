from __future__ import annotations

import json
import shutil
from pathlib import Path

from PIL import Image


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\27\Raw + wires + components + junctions"
)
RESULTS = BASE / "results"
CODES = BASE / "codes"
CROP_DIR = RESULTS / "visual_crops"

SOURCES = {
    "raw": BASE / "raw -- synthetic_npp_electrical_schematic_readable.png",
    "components": BASE / "detected_components_overlay.png",
    "wires": BASE / "wires_mask_overlay.png",
    "wire_nodes": BASE / "wire_nodes_overlay.png",
}

# Coordinates are on the 10522 x 7307 original image.
REGIONS = {
    "full_thumb": (0, 0, 10522, 7307),
    "top_13kv_sources": (260, 300, 8500, 2050),
    "top_left_source_detail": (300, 460, 3600, 1800),
    "top_mid_tie_detail": (2500, 300, 7200, 1900),
    "top_right_source_detail": (6500, 420, 8700, 1900),
    "4160_a_bus_and_left_transformer": (420, 1200, 4700, 2700),
    "4160_b_bus_and_right_transformer": (4400, 1200, 9000, 2700),
    "train_a_load_center_a_full": (520, 2150, 4450, 4200),
    "train_b_load_center_b_full": (4450, 2150, 8300, 4200),
    "train_c_load_center_c_full": (520, 4050, 4450, 6400),
    "train_d_load_center_d_full": (4450, 4050, 8300, 6400),
    "load_center_a_left_half": (520, 2300, 2600, 4100),
    "load_center_a_right_half": (2350, 2300, 4450, 4100),
    "load_center_b_left_half": (4450, 2300, 6400, 4100),
    "load_center_b_right_half": (6200, 2300, 8300, 4100),
    "load_center_c_left_half": (520, 4200, 2600, 6250),
    "load_center_c_right_half": (2350, 4200, 4450, 6250),
    "load_center_d_left_half": (4450, 4200, 6400, 6250),
    "load_center_d_right_half": (6200, 4200, 8300, 6250),
    "dc_bus_125a_and_control": (3600, 3000, 6100, 4350),
    "right_side_notes_legend": (8500, 300, 10400, 6650),
    "bottom_ground_paths": (450, 5700, 8400, 6900),
}


def crop_and_save() -> None:
    CROP_DIR.mkdir(parents=True, exist_ok=True)
    CODES.mkdir(parents=True, exist_ok=True)
    manifest = []
    for source_name, source_path in SOURCES.items():
        image = Image.open(source_path).convert("RGB")
        width, height = image.size
        for region_name, box in REGIONS.items():
            x1, y1, x2, y2 = box
            x1 = max(0, min(width, x1))
            y1 = max(0, min(height, y1))
            x2 = max(x1 + 1, min(width, x2))
            y2 = max(y1 + 1, min(height, y2))
            crop = image.crop((x1, y1, x2, y2))
            if region_name == "full_thumb":
                crop.thumbnail((2400, 1700))
            out_path = CROP_DIR / f"{source_name}_{region_name}.png"
            crop.save(out_path)
            manifest.append(
                {
                    "source": source_name,
                    "source_file": str(source_path),
                    "region": region_name,
                    "box": [x1, y1, x2, y2],
                    "output": str(out_path),
                    "size": list(crop.size),
                }
            )
    (CROP_DIR / "crop_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    shutil.copy2(Path(__file__).resolve(), CODES / Path(__file__).name)
    print(json.dumps({"crop_count": len(manifest), "crop_dir": str(CROP_DIR)}, indent=2))


if __name__ == "__main__":
    crop_and_save()
