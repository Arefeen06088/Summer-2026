from __future__ import annotations

from pathlib import Path

from PIL import Image


BASE_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = BASE_DIR / "results" / "visual_crops"

SOURCES = [
    "raw -- synthetic_npp_electrical_schematic_revised(1).png",
    "detected_components_overlay.png",
    "wires_mask.png",
    "wires_mask_overlay.png",
]

BROAD_CROPS = {
    "whole_drawing_area": (90, 80, 3975, 2635),
    "top_4160_distribution": (130, 160, 2930, 800),
    "middle_480_load_centers": (130, 800, 2930, 1710),
    "bottom_rps_vital_power": (130, 1710, 2930, 2550),
    "right_notes_legend_title": (2980, 180, 3910, 2550),
}

FOCUSED_RAW_CROPS = {
    "notes": (2980, 190, 3900, 1260),
    "legend": (2980, 1320, 3890, 1760),
    "title_block": (2980, 2180, 3890, 2540),
    "top_left_grid_and_bus_a": (135, 185, 1630, 795),
    "top_center_tie_and_edg_a": (1460, 185, 2350, 795),
    "top_right_edg_b_and_bus_b": (2100, 185, 2920, 795),
    "480_left_bus_and_mccs": (130, 815, 1510, 1265),
    "480_right_bus_and_mccs": (1360, 815, 2930, 1265),
    "load_feeders_left": (145, 1120, 1510, 1810),
    "load_feeders_right": (1360, 1120, 2930, 1810),
    "rps_control_left": (135, 1780, 1510, 2290),
    "rps_control_right": (1360, 1780, 2930, 2290),
    "vital_power_left": (135, 2150, 1510, 2545),
    "vital_power_right": (1360, 2150, 2930, 2545),
    "bottom_center_ups_ground": (1240, 2100, 2340, 2600),
    "central_rps_measurement": (790, 1780, 1780, 2280),
    "right_rps_measurement": (1840, 1780, 2860, 2280),
}


def safe_folder_name(name: str) -> str:
    return Path(name).stem.replace(" ", "_").replace("-", "_").replace("(", "").replace(")", "")


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
