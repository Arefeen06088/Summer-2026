from __future__ import annotations

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "visual_crops"

SOURCES = [
    "raw -- synthetic_npp_schematic_improved_local_refined_v3.png",
    "detected_components_overlay.png",
    "wires_mask.png",
    "wires_mask_overlay.png",
]

CROPS = {
    "whole_schematic_area": (80, 70, 3300, 2250),
    "top_normal_source_and_terminals": (120, 120, 3250, 720),
    "middle_4160v_buses_and_generators": (120, 650, 3250, 1200),
    "left_train_a_loads": (120, 1130, 1450, 2220),
    "center_train_a_dc_control": (1300, 1100, 2100, 2220),
    "right_train_b_loads": (1950, 1130, 3250, 2220),
    "right_train_b_dc_control": (2750, 1100, 3320, 2220),
    "bottom_interlock_controls": (150, 1700, 3300, 2260),
    "title_legend_notes": (3340, 120, 4070, 2780),
}

FOCUSED = {
    "top_left_normal_source": (180, 180, 1350, 700),
    "top_center_uat_gen_tie": (940, 180, 2300, 760),
    "top_right_normal_source": (2100, 180, 3250, 760),
    "middle_left_bus_52a": (130, 690, 1340, 1160),
    "middle_center_bus_tie": (1320, 690, 2030, 1220),
    "middle_right_bus_52b": (2030, 690, 3230, 1160),
    "left_mcc_loads_zoom": (150, 1180, 1350, 2050),
    "center_a_control_zoom": (1320, 1280, 2100, 2220),
    "right_mcc_loads_zoom": (2000, 1180, 3200, 2050),
    "right_b_control_zoom": (2780, 1280, 3300, 2220),
    "lower_control_interlocks": (850, 1580, 3230, 2250),
}


def safe_stem(path: Path) -> str:
    return "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in path.stem)


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    for source in SOURCES:
        path = ROOT / source
        with Image.open(path) as image:
            out_dir = RESULTS / safe_stem(path)
            out_dir.mkdir(parents=True, exist_ok=True)
            for name, box in CROPS.items():
                image.crop(box).save(out_dir / f"{name}.png")
            if source.startswith("raw --"):
                focused_dir = RESULTS / "focused_raw"
                focused_dir.mkdir(parents=True, exist_ok=True)
                for name, box in FOCUSED.items():
                    image.crop(box).save(focused_dir / f"{name}.png")
    print(f"wrote crops to {RESULTS}")


if __name__ == "__main__":
    main()
