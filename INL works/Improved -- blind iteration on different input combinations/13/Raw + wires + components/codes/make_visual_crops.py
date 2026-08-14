from __future__ import annotations

import re
from pathlib import Path

from PIL import Image


BASE_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = BASE_DIR / "results"
CROP_DIR = RESULTS_DIR / "visual_crops"


SOURCES = [
    "raw -- synthetic diagram _.png",
    "detected_components_overlay.png",
    "wires_mask.png",
    "wires_mask_overlay.png",
]


BROAD_CROPS = {
    "whole_drawing_area": (150, 130, 5050, 3750),
    "top_station_startup_source": (350, 350, 2450, 870),
    "train_a_overall": (380, 720, 2580, 1900),
    "train_b_overall": (2670, 720, 4880, 1900),
    "diesel_and_middle_tie_region": (350, 1850, 4920, 2250),
    "train_c_overall": (380, 2100, 2580, 3400),
    "train_d_overall": (2670, 2100, 4880, 3400),
    "right_notes_legend_schedule_title": (5030, 210, 6210, 4070),
}


FOCUSED_CROPS = {
    "train_a_top_bus_source": (410, 740, 2450, 1110),
    "train_a_480_mcc_loads": (470, 1050, 2420, 1690),
    "train_a_dc_battery_ups": (1850, 1080, 2500, 1740),
    "train_b_top_bus_source": (2700, 740, 4740, 1110),
    "train_b_480_mcc_loads": (2760, 1050, 4710, 1690),
    "train_b_dc_battery_ups": (4140, 1080, 4800, 1740),
    "train_c_top_bus_source": (410, 2090, 2450, 2500),
    "train_c_480_mcc_loads": (470, 2420, 2420, 3100),
    "train_c_dc_battery_ups": (1850, 2450, 2500, 3110),
    "train_d_top_bus_source": (2700, 2090, 4740, 2500),
    "train_d_480_mcc_loads": (2760, 2420, 4710, 3100),
    "train_d_dc_battery_ups": (4140, 2450, 4800, 3110),
    "shared_grounding_lower_center": (2100, 3140, 3050, 3660),
    "notes_and_legend": (5070, 520, 6180, 2090),
    "feeder_schedule": (5070, 2100, 6170, 2910),
    "title_block": (5030, 3330, 6210, 4070),
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
