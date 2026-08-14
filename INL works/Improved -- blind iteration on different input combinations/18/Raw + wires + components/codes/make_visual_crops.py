from __future__ import annotations

import re
from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\18\Raw + wires + components")
RESULTS = BASE / "results"
CROPS = RESULTS / "visual_crops"

FILES = [
    "raw -- synthetic_nuclear_electrical_schematic_readable.png",
    "detected_components_overlay.png",
    "wires_mask.png",
    "wires_mask_overlay.png",
]


def safe_folder_name(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]+", "_", Path(name).stem).strip("_")


def save_crop(img: Image.Image, folder: Path, name: str, box: tuple[int, int, int, int]) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    width, height = img.size
    left, top, right, bottom = box
    clipped = (max(0, left), max(0, top), min(width, right), min(height, bottom))
    img.crop(clipped).save(folder / f"{name}.png")


def main() -> None:
    broad = {
        "whole_drawing_area": (0, 0, 7000, 4400),
        "top_left": (0, 0, 2450, 1550),
        "top_center": (2200, 0, 4800, 1550),
        "top_right": (4550, 0, 7000, 1550),
        "middle_left": (0, 1300, 2450, 3000),
        "middle_center": (2200, 1300, 4800, 3000),
        "middle_right": (4550, 1300, 7000, 3000),
        "bottom_left": (0, 2750, 2450, 4400),
        "bottom_center": (2200, 2750, 4800, 4400),
        "bottom_right": (4550, 2750, 7000, 4400),
        "right_notes_title": (5400, 0, 7000, 4400),
    }
    focused_raw = {
        "title_notes_legend": (5350, 0, 7000, 1700),
        "main_bus_top": (0, 0, 7000, 1250),
        "left_train_feeders": (0, 900, 2550, 2850),
        "center_train_feeders": (2300, 900, 4750, 2850),
        "right_train_feeders": (4500, 900, 7000, 2850),
        "lower_control_left": (0, 2550, 2600, 4400),
        "lower_control_center": (2300, 2550, 4800, 4400),
        "lower_control_right": (4500, 2550, 7000, 4400),
        "label_zoom_left_top": (400, 550, 2450, 1550),
        "label_zoom_center_top": (2350, 550, 4700, 1550),
        "label_zoom_right_top": (4550, 550, 6500, 1550),
        "load_labels_left": (300, 1600, 2500, 2900),
        "load_labels_center": (2400, 1600, 4700, 2900),
        "load_labels_right": (4550, 1600, 6750, 2900),
        "zoom_source_switchyard": (250, 250, 1700, 750),
        "zoom_dg_tie_area": (1200, 600, 3050, 1250),
        "zoom_generator_uat": (4300, 350, 5750, 950),
        "zoom_rps_train_a": (1600, 2750, 2600, 3550),
        "zoom_rps_train_b": (4750, 2750, 5850, 3550),
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
