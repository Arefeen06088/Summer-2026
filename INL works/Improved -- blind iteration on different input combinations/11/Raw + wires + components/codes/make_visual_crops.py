from __future__ import annotations

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "visual_crops"

SOURCES = [
    "raw -- synthetic_npp_electrical_schematic_relocated_names.png",
    "detected_components_overlay.png",
    "wires_mask.png",
    "wires_mask_overlay.png",
]

CROPS = {
    "whole_drawing_area": (170, 120, 6980, 4620),
    "top_source_and_13kv_buses": (520, 150, 5800, 760),
    "train_a_overall": (430, 620, 1780, 3420),
    "train_b_overall": (1780, 620, 3150, 3420),
    "train_c_overall": (3150, 620, 4520, 3420),
    "train_d_overall": (4520, 620, 5900, 3420),
    "bottom_dc_and_interlocks": (840, 3240, 5480, 4200),
    "notes_symbols_title": (5920, 360, 7040, 4460),
}

FOCUSED = {
    "train_a_upper_source_bus": (470, 580, 1780, 1400),
    "train_b_upper_source_bus": (1800, 580, 3150, 1400),
    "train_c_upper_source_bus": (3180, 580, 4520, 1400),
    "train_d_upper_source_bus": (4550, 580, 5900, 1400),
    "train_a_480_mcc_loads": (460, 1320, 1780, 3000),
    "train_b_480_mcc_loads": (1800, 1320, 3150, 3000),
    "train_c_480_mcc_loads": (3180, 1320, 4520, 3000),
    "train_d_480_mcc_loads": (4550, 1320, 5900, 3000),
    "train_a_dc_ground_panel": (800, 2500, 1870, 3400),
    "train_b_dc_ground_panel": (2130, 2500, 3200, 3400),
    "train_c_dc_ground_panel": (3500, 2500, 4570, 3400),
    "train_d_dc_ground_panel": (4870, 2500, 5900, 3400),
    "bottom_division_a_dc_rps": (820, 3420, 3050, 4150),
    "bottom_division_b_dc_rps": (3000, 3420, 5480, 4150),
    "ssps_and_ats_center": (2160, 3120, 4200, 3840),
    "right_notes_legend": (5940, 360, 7040, 2920),
    "right_title_block": (5940, 3520, 7040, 4460),
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
