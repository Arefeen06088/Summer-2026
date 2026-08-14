from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "visual_crops"

SOURCES = [
    "raw -- synthetic_npp_electrical_schematic_variant3_redo_clean_v7.png",
    "detected_components_and_logical_overlay.png",
    "wires_mask.png",
    "wires_mask_overlay.png",
]

CROPS = {
    "top_left_generator_switchyard": (150, 150, 4700, 950),
    "top_center_bus_ties": (1800, 600, 6100, 1600),
    "medium_voltage_safety_buses": (150, 900, 6150, 1850),
    "load_centers_left": (150, 1650, 2650, 3200),
    "load_centers_middle": (2550, 1650, 6100, 3200),
    "dc_ups_bottom": (2000, 2920, 6500, 3920),
    "control_bay_right": (6850, 560, 8850, 2520),
    "right_edg_control_entry": (6100, 760, 7600, 1420),
    "whole_power_path_wide": (150, 120, 6800, 3300),
}


def safe_stem(name):
    return "".join(ch if ch.isalnum() else "_" for ch in Path(name).stem)


def main():
    RESULTS.mkdir(parents=True, exist_ok=True)
    for source in SOURCES:
        image = Image.open(ROOT / source)
        out_dir = RESULTS / safe_stem(source)
        out_dir.mkdir(parents=True, exist_ok=True)
        for crop_name, box in CROPS.items():
            image.crop(box).save(out_dir / f"{crop_name}.png")
    print(f"wrote crops to {RESULTS}")


if __name__ == "__main__":
    main()
