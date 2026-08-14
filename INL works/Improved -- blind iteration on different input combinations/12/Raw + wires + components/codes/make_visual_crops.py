from __future__ import annotations

import re
from pathlib import Path

from PIL import Image


BASE_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = BASE_DIR / "results"
CROP_DIR = RESULTS_DIR / "visual_crops"


SOURCES = [
    "raw -- synthetic_npp_electrical_schematic_rps_rerouted.png",
    "detected_components_overlay.png",
    "wires_mask.png",
    "wires_mask_overlay.png",
]


BROAD_CROPS = {
    "whole_drawing_area": (95, 80, 4105, 2915),
    "top_4160_sources_and_bus": (180, 120, 3180, 660),
    "train_a_overall": (170, 170, 1560, 1950),
    "train_b_overall": (1740, 170, 3120, 1950),
    "bottom_dc_logic_overall": (770, 1810, 3260, 2825),
    "notes_legend_title": (3180, 230, 4105, 2750),
}


FOCUSED_CROPS = {
    "top_left_train_a_sources": (210, 150, 1535, 710),
    "top_right_train_b_sources": (1780, 150, 3090, 710),
    "train_a_480_mcc_loads": (220, 760, 1420, 1840),
    "train_b_480_mcc_loads": (1820, 760, 3020, 1840),
    "train_a_dc_inputs": (1030, 1810, 1535, 2265),
    "train_b_dc_inputs": (2015, 1810, 2530, 2265),
    "bottom_left_rps_logic": (800, 2190, 1770, 2810),
    "bottom_center_ats_esf_bus": (1360, 2050, 2420, 2690),
    "bottom_right_rps_logic": (2200, 2190, 3210, 2810),
    "center_tie_ats_dc_buses": (1340, 1700, 2480, 2380),
    "notes_and_symbols": (3230, 245, 4020, 1180),
    "title_block": (3230, 2180, 4080, 2740),
}


def safe_name(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", Path(name).stem).strip("_")


def save_crop(source: Path, crop_name: str, box: tuple[int, int, int, int], out_dir: Path) -> None:
    with Image.open(source) as img:
        width, height = img.size
        left, top, right, bottom = box
        bounded = (max(0, left), max(0, top), min(width, right), min(height, bottom))
        crop = img.crop(bounded)
        crop.save(out_dir / f"{crop_name}.png")


def main() -> None:
    CROP_DIR.mkdir(parents=True, exist_ok=True)

    for source_name in SOURCES:
        source = BASE_DIR / source_name
        if not source.exists():
            raise FileNotFoundError(source)
        out_dir = CROP_DIR / safe_name(source_name)
        out_dir.mkdir(parents=True, exist_ok=True)
        for name, box in BROAD_CROPS.items():
            save_crop(source, name, box, out_dir)

    raw = BASE_DIR / SOURCES[0]
    focused_dir = CROP_DIR / "focused_raw"
    focused_dir.mkdir(parents=True, exist_ok=True)
    for name, box in FOCUSED_CROPS.items():
        save_crop(raw, name, box, focused_dir)

    print(f"Wrote crops to {CROP_DIR}")
    print(f"Broad crops per source: {len(BROAD_CROPS)}")
    print(f"Focused raw crops: {len(FOCUSED_CROPS)}")


if __name__ == "__main__":
    main()
