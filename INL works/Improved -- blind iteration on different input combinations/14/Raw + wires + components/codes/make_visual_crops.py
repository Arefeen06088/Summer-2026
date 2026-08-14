from __future__ import annotations

import re
from pathlib import Path

from PIL import Image


BASE_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = BASE_DIR / "results"
CROP_DIR = RESULTS_DIR / "visual_crops"


SOURCES = [
    "raw -- synthetic_npp_electrical_schematic_even_bus_spacing (1).png",
    "detected_components_overlay.png",
    "wires_mask.png",
    "wires_mask_overlay.png",
]


BROAD_CROPS = {
    "whole_drawing_area": (150, 80, 6420, 4040),
    "train_a_upper_4160": (470, 250, 2850, 1540),
    "train_b_upper_4160": (3000, 250, 5400, 1540),
    "train_a_480_mcc": (470, 1500, 2880, 2740),
    "train_b_480_mcc": (3000, 1500, 5400, 2740),
    "train_a_dc_ups": (500, 2700, 2900, 3920),
    "train_b_dc_ups": (3000, 2700, 5400, 3920),
    "center_ties_and_panel_links": (2700, 650, 3350, 3850),
    "right_notes_and_title": (5450, 240, 6350, 3900),
}


FOCUSED_CROPS = {
    "notes_legend": (5480, 300, 6300, 1420),
    "title_block": (5480, 3150, 6300, 3860),
    "train_a_sources_bus": (650, 260, 2700, 760),
    "train_b_sources_bus": (3150, 260, 5250, 760),
    "train_a_safety_loads": (1600, 720, 2800, 1540),
    "train_b_safety_loads": (4100, 720, 5300, 1540),
    "train_a_480_feeders_left": (650, 1580, 1800, 2660),
    "train_a_480_feeders_right": (1700, 1580, 2850, 2660),
    "train_b_480_feeders_left": (3150, 1580, 4300, 2660),
    "train_b_480_feeders_right": (4200, 1580, 5350, 2660),
    "train_a_panel_links": (650, 2500, 2950, 3040),
    "train_b_panel_links": (3150, 2500, 5450, 3040),
    "train_a_dc_bus_ups": (650, 3000, 2850, 3900),
    "train_b_dc_bus_ups": (3150, 3000, 5350, 3900),
    "master_terminal_blocks": (520, 3820, 2900, 4090),
    "center_intertrain_links": (2850, 1500, 3450, 3750),
}


def safe_name(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", Path(name).stem).strip("_")


def save_crop(source: Path, crop_name: str, box: tuple[int, int, int, int], out_dir: Path) -> None:
    with Image.open(source) as img:
        width, height = img.size
        left, top, right, bottom = box
        bounded = (max(0, left), max(0, top), min(width, right), min(height, bottom))
        img.crop(bounded).save(out_dir / f"{crop_name}.png")


def main() -> None:
    CROP_DIR.mkdir(parents=True, exist_ok=True)
    for source_name in SOURCES:
        source = BASE_DIR / source_name
        if not source.exists():
            raise FileNotFoundError(source)
        out_dir = CROP_DIR / safe_name(source_name)
        out_dir.mkdir(parents=True, exist_ok=True)
        for crop_name, box in BROAD_CROPS.items():
            save_crop(source, crop_name, box, out_dir)

    focused_dir = CROP_DIR / "focused_raw"
    focused_dir.mkdir(parents=True, exist_ok=True)
    raw = BASE_DIR / SOURCES[0]
    for crop_name, box in FOCUSED_CROPS.items():
        save_crop(raw, crop_name, box, focused_dir)

    print(f"Wrote crops to {CROP_DIR}")
    print(f"Broad crops per source: {len(BROAD_CROPS)}")
    print(f"Focused raw crops: {len(FOCUSED_CROPS)}")


if __name__ == "__main__":
    main()
