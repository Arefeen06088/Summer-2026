from __future__ import annotations

from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\11\Raw")
RAW = BASE / "raw -- synthetic_npp_electrical_schematic_relocated_names.png"
OUT = BASE / "results" / "crops"


CROPS: dict[str, tuple[int, int, int, int]] = {
    "full_drawing_area": (180, 120, 7040, 4620),
    "top_sources_and_13kv_buses": (520, 170, 5850, 760),
    "top_left_bus_a_sources": (520, 170, 3350, 860),
    "top_right_bus_b_sources": (3300, 170, 5850, 860),
    "train_a_full": (430, 560, 1810, 3500),
    "train_b_full": (1770, 560, 3210, 3500),
    "train_c_full": (3180, 560, 4620, 3500),
    "train_d_full": (4530, 560, 5930, 3500),
    "train_a_upper": (430, 560, 1810, 1650),
    "train_b_upper": (1770, 560, 3210, 1650),
    "train_c_upper": (3180, 560, 4620, 1650),
    "train_d_upper": (4530, 560, 5930, 1650),
    "train_a_middle_loads": (430, 1550, 1810, 3000),
    "train_b_middle_loads": (1770, 1550, 3210, 3000),
    "train_c_middle_loads": (3180, 1550, 4620, 3000),
    "train_d_middle_loads": (4530, 1550, 5930, 3000),
    "train_a_rect_ic_ground_detail": (1250, 2100, 1790, 3440),
    "train_b_rect_ic_ground_detail": (2600, 2100, 3150, 3440),
    "train_c_rect_ic_ground_detail": (3980, 2100, 4540, 3440),
    "train_d_rect_ic_ground_detail": (5350, 2100, 5900, 3440),
    "bottom_dc_division_a": (560, 3250, 2850, 4210),
    "bottom_dc_division_b": (2760, 3250, 5250, 4210),
    "ats_and_sps_interlocks": (2100, 2900, 4500, 3900),
    "ats_480_a_detail": (1350, 2600, 3300, 3920),
    "ats_480_b_detail": (3000, 2600, 5000, 3920),
    "bottom_all_dc_rps_ssps": (560, 3000, 5650, 4300),
    "dc_a_c_landing_detail": (1300, 3000, 3900, 4300),
    "dc_b_d_landing_detail": (2600, 3000, 5600, 4300),
    "right_notes_legend_title": (5940, 430, 7010, 4500),
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    image = Image.open(RAW)
    for name, box in CROPS.items():
        image.crop(box).save(OUT / f"{name}.png")
    print(f"Wrote {len(CROPS)} crops to {OUT}")


if __name__ == "__main__":
    main()
