from __future__ import annotations

from pathlib import Path

from PIL import Image


BASE_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = BASE_DIR / "results" / "visual_crops"

SOURCES = [
    "raw -- improved_synthetic_nuclear_electrical_schematic.png",
    "detected_components_overlay.png",
    "wires_mask.png",
    "wires_mask_overlay.png",
]

BROAD_CROPS = {
    "whole_drawing_area": (160, 70, 7390, 4760),
    "top_offsite_sources": (460, 70, 5750, 620),
    "division_a_overall": (300, 520, 1810, 3620),
    "division_b_overall": (1770, 520, 3280, 3620),
    "division_c_overall": (3300, 520, 4810, 3620),
    "division_d_overall": (4800, 520, 6350, 3620),
    "middle_tie_and_sip": (1450, 560, 5050, 1400),
    "right_notes": (6150, 430, 7320, 3220),
    "title_block": (5200, 4150, 7330, 4690),
}

FOCUSED_RAW_CROPS = {
    "notes_legend": (6150, 430, 7320, 1620),
    "load_schedule": (6150, 1630, 7320, 2480),
    "revision_and_title": (210, 4180, 7330, 4690),
    "top_bus_left": (470, 80, 3000, 570),
    "top_bus_right": (2900, 80, 5750, 570),
    "top_bus_far_right": (5000, 80, 7040, 620),
    "division_a_4160_and_480": (330, 560, 1780, 1420),
    "division_b_4160_and_480": (1800, 560, 3250, 1420),
    "division_c_4160_and_480": (3330, 560, 4780, 1420),
    "division_d_4160_and_480": (4830, 560, 6320, 1420),
    "division_a_mcc_loads": (330, 1450, 1780, 2890),
    "division_b_mcc_loads": (1800, 1450, 3250, 2890),
    "division_c_mcc_loads": (3330, 1450, 4780, 2890),
    "division_d_mcc_loads": (4830, 1450, 6320, 2890),
    "division_a_dc_control": (330, 3000, 1780, 3630),
    "division_b_dc_control": (1800, 3000, 3250, 3630),
    "division_c_dc_control": (3330, 3000, 4780, 3630),
    "division_d_dc_control": (4830, 3000, 6320, 3630),
    "tie_bus_left_center": (1350, 620, 2200, 1280),
    "tie_bus_right_center": (4410, 620, 5280, 1280),
    "sip_boxes_left": (1440, 830, 2100, 1330),
    "sip_boxes_right": (4430, 830, 5100, 1330),
}


def safe_folder_name(name: str) -> str:
    return Path(name).stem.replace(" ", "_").replace("-", "_")


def crop_source(source: Path, crop_dir: Path, crop_map: dict[str, tuple[int, int, int, int]]) -> None:
    with Image.open(source) as img:
        for crop_name, box in crop_map.items():
            out_path = crop_dir / f"{crop_name}.png"
            out_path.parent.mkdir(parents=True, exist_ok=True)
            img.crop(box).save(out_path)


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    for source_name in SOURCES:
        source = BASE_DIR / source_name
        if not source.exists():
            raise FileNotFoundError(source)
        crop_source(source, RESULTS_DIR / safe_folder_name(source_name), BROAD_CROPS)

    raw = BASE_DIR / SOURCES[0]
    crop_source(raw, RESULTS_DIR / "focused_raw", FOCUSED_RAW_CROPS)

    print(f"Wrote visual crops to {RESULTS_DIR}")


if __name__ == "__main__":
    main()
