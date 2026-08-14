from __future__ import annotations

import re
from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\17\Raw + wires + components")
RESULTS = BASE / "results"
CROPS = RESULTS / "visual_crops"


FILES = [
    "raw -- synthetic_npp_aux_power_schematic_overlap_fixed.png",
    "detected_components_overlay.png",
    "wires_mask.png",
    "wires_mask_overlay.png",
]


def safe_folder_name(name: str) -> str:
    stem = Path(name).stem
    return re.sub(r"[^A-Za-z0-9_]+", "_", stem).strip("_")


def save_crop(img: Image.Image, folder: Path, name: str, box: tuple[int, int, int, int]) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    w, h = img.size
    left, top, right, bottom = box
    clipped = (max(0, left), max(0, top), min(w, right), min(h, bottom))
    img.crop(clipped).save(folder / f"{name}.png")


def main() -> None:
    broad = {
        "whole_drawing_area": (0, 0, 5600, 3600),
        "top_power_distribution": (0, 0, 5600, 1120),
        "middle_mcc_loads": (0, 760, 5600, 2400),
        "bottom_control_vital": (0, 2150, 5600, 3600),
        "right_notes_legend_title": (4020, 0, 5600, 3600),
        "left_half": (0, 0, 2850, 3600),
        "right_half": (2750, 0, 5600, 3600),
    }
    focused_raw = {
        "notes_legend_title": (4200, 0, 5600, 1120),
        "top_left_sources": (0, 0, 1650, 850),
        "top_center_buses": (1400, 0, 3300, 880),
        "top_right_sources": (3000, 0, 4700, 900),
        "top_far_right": (4300, 0, 5600, 900),
        "mcc_left": (0, 760, 1900, 1780),
        "mcc_center": (1650, 760, 3700, 1780),
        "mcc_right": (3450, 760, 5600, 1780),
        "loads_left": (0, 1450, 1900, 2500),
        "loads_center": (1650, 1450, 3700, 2500),
        "loads_right": (3450, 1450, 5600, 2500),
        "control_left": (0, 2350, 2200, 3600),
        "control_center": (1900, 2350, 3900, 3600),
        "control_right": (3600, 2350, 5600, 3600),
        "bottom_vital_power_left": (0, 2800, 2200, 3600),
        "bottom_vital_power_center": (1900, 2800, 3900, 3600),
        "bottom_vital_power_right": (3600, 2800, 5600, 3600),
        "top_4160_left_half_fine": (240, 470, 2450, 1280),
        "top_4160_right_half_fine": (2250, 470, 4050, 1280),
        "bus480_a_feeders_1": (620, 1120, 1650, 2440),
        "bus480_a_feeders_2": (1450, 1120, 2550, 2440),
        "bus480_b_feeders_1": (2350, 1120, 3450, 2440),
        "bus480_b_feeders_2": (3250, 1120, 4350, 2440),
        "bus480_b_feeders_3": (4050, 1120, 4700, 2440),
        "dc_control_a_fine": (680, 2500, 2450, 3600),
        "ann_control_center_fine": (2200, 2500, 3400, 3600),
        "dc_control_b_fine": (3350, 2500, 5000, 3600),
    }
    for filename in FILES:
        img = Image.open(BASE / filename)
        folder = CROPS / safe_folder_name(filename)
        for name, box in broad.items():
            save_crop(img, folder, name, box)
    raw_img = Image.open(BASE / FILES[0])
    raw_folder = CROPS / "focused_raw"
    for name, box in focused_raw.items():
        save_crop(raw_img, raw_folder, name, box)
    print(f"wrote crops under {CROPS}")


if __name__ == "__main__":
    main()
