from __future__ import annotations

from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\9\Raw")
RAW = BASE / "raw -- synthetic_npp_schematic_expanded_clear_refined_v3_reworked.png"
OUT = BASE / "results" / "crops"


CROPS = {
    "top_sources_aux": (150, 150, 4250, 760),
    "train_a_4160_480": (160, 620, 1520, 1570),
    "central_normal_distribution": (1430, 540, 2720, 1840),
    "train_b_4160_480": (2660, 620, 4070, 1570),
    "train_a_loads_detail": (190, 1330, 1440, 2350),
    "train_b_loads_detail": (2810, 1330, 4030, 2350),
    "train_a_dc_control": (170, 2250, 1540, 3090),
    "train_b_dc_control": (2760, 2250, 4130, 3090),
    "central_rtd_terminal_blocks": (1590, 1700, 2530, 2320),
    "left_protection_detail": (1140, 760, 1510, 1260),
    "right_protection_detail": (2670, 760, 3040, 1260),
    "normal_train_a_load_panel": (1470, 1180, 2100, 1740),
    "normal_train_b_load_panel": (2050, 1180, 2660, 1740),
    "title_legend_right": (4350, 300, 4870, 3100),
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    image = Image.open(RAW)
    for name, box in CROPS.items():
        image.crop(box).save(OUT / f"{name}.png")
    print(f"wrote {len(CROPS)} crops to {OUT}")


if __name__ == "__main__":
    main()
