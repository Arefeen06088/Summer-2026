from __future__ import annotations

from pathlib import Path

from PIL import Image


ROOT = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\9\Raw + wires"
)
RESULTS = ROOT / "results"
CROPS = RESULTS / "crops"

RAW = ROOT / "raw -- synthetic_npp_schematic_expanded_clear_refined_v3_reworked.png"
MASK = ROOT / "wires_mask.png"
OVERLAY = ROOT / "wires_mask_overlay.png"

REGIONS = {
    "01_top_sources_full": (160, 120, 4240, 560),
    "02_top_left_sources_detail": (170, 160, 950, 560),
    "03_top_center_unit_aux_detail": (950, 160, 2650, 720),
    "04_top_right_sources_detail": (3100, 160, 4240, 560),
    "05_left_train_a_4160_480": (170, 520, 1580, 1500),
    "06_center_normal_4160_480": (1400, 520, 2700, 1600),
    "07_right_train_b_4160_480": (2630, 520, 4070, 1500),
    "08_left_train_a_loads": (170, 1350, 1560, 2360),
    "09_center_normal_loads_controls": (1400, 1300, 2700, 2350),
    "10_right_train_b_loads": (2630, 1350, 4070, 2360),
    "11_bottom_train_a_dc_control": (170, 2250, 1560, 3100),
    "12_bottom_train_b_dc_control": (2630, 2250, 4070, 3100),
    "13_lower_cross_control": (1000, 1820, 3200, 2920),
    "14_notes_legend_title": (4300, 400, 4900, 3130),
    "15_title_block": (4300, 2700, 4900, 3130),
    "16_full_left_system": (170, 120, 1750, 3100),
    "17_full_center_system": (1400, 120, 2900, 3100),
    "18_full_right_system": (2550, 120, 4250, 3100),
}


def main() -> None:
    CROPS.mkdir(parents=True, exist_ok=True)
    sources = {
        "raw": Image.open(RAW),
        "mask": Image.open(MASK),
        "overlay": Image.open(OVERLAY),
    }
    count = 0
    for source_name, image in sources.items():
        for region_name, box in REGIONS.items():
            image.crop(box).save(CROPS / f"{source_name}_{region_name}.png")
            count += 1
    print(f"Wrote {count} crops to {CROPS}")


if __name__ == "__main__":
    main()
