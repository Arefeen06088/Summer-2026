from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\4\Raw")
RAW = BASE / "raw.png"
OUT = BASE / "results" / "crops"


CROPS = {
    "top_left_sources_and_bus": (300, 250, 2700, 1450),
    "top_mid_feeders": (1750, 700, 5600, 2350),
    "top_right_feeders_and_tie": (5000, 700, 7450, 2350),
    "left_vertical_lc_and_bus": (650, 1100, 1800, 3900),
    "bottom_left_load_center": (950, 3700, 3600, 5200),
    "bottom_right_load_center": (4200, 3650, 6500, 5200),
    "load_center_tie": (3300, 3450, 5000, 4550),
    "load_center_b_incoming": (6100, 2400, 7600, 4550),
    "central_dc_ups": (4200, 2100, 7500, 3850),
    "central_dc_ups_left": (4200, 2100, 5850, 3350),
    "central_dc_ups_right": (5600, 2100, 7500, 3850),
    "right_reactor_transformers": (6800, 2100, 7600, 3750),
    "title_notes_legend": (7350, 300, 8500, 5200),
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    image = Image.open(RAW)
    for name, box in CROPS.items():
        image.crop(box).save(OUT / f"{name}.png")
    print(f"wrote {len(CROPS)} crops to {OUT}")


if __name__ == "__main__":
    main()
