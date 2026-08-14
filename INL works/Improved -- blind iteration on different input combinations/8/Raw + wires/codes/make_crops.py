from __future__ import annotations

from pathlib import Path

from PIL import Image


ROOT = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\8\Raw + wires"
)
RESULTS = ROOT / "results"
CROPS = RESULTS / "crops"

RAW = ROOT / "raw -- synthetic_npp_schematic_improved_local_refined_v3.png"
MASK = ROOT / "wires_mask.png"
OVERLAY = ROOT / "wires_mask_overlay.png"

REGIONS = {
    "01_top_4160_sources": (150, 120, 3350, 760),
    "02_mid_4160_buses_dg": (150, 680, 3350, 1260),
    "03_left_480_loads": (150, 1120, 1720, 2260),
    "04_right_480_loads": (1880, 1120, 3380, 2260),
    "05_train_a_dc_ups_control": (1260, 1300, 1870, 2280),
    "06_train_b_dc_ups_control": (2920, 1300, 3470, 2280),
    "07_lower_cross_controls": (760, 1860, 3140, 2320),
    "08_notes_legend_title": (3330, 130, 4080, 2860),
    "09_left_system_full": (150, 120, 2050, 2300),
    "10_right_system_full": (1760, 120, 3380, 2300),
    "11_center_ties": (1450, 520, 2050, 1420),
    "12_title_block": (3330, 2060, 4080, 2860),
    "13_top_left_sources_detail": (220, 170, 1260, 720),
    "14_top_center_sources_detail": (1020, 170, 2450, 760),
    "15_top_right_sources_detail": (2220, 170, 3340, 760),
    "16_train_a_load_control_detail": (210, 1420, 1740, 2260),
    "17_train_b_load_control_detail": (1960, 1420, 3370, 2260),
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
