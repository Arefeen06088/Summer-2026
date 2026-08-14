from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\3\Raw")
RAW = BASE / "raw -- synthetic_npp_100_component_electrical_schematic.png"
OUT = BASE / "results" / "crops"


CROPS = {
    "full_left_train_a": (190, 230, 2750, 2050),
    "full_right_train_b": (2750, 230, 5120, 2050),
    "top_bus_tie_and_ground": (740, 430, 3100, 760),
    "bus_tie_ground_close": (2450, 430, 3650, 1070),
    "dc_ups_center": (2200, 780, 3400, 1780),
    "a_feeder_bus": (250, 1750, 2580, 3000),
    "b_feeder_bus": (2600, 1750, 5000, 3000),
    "left_loads_a1_a2": (250, 2050, 2600, 2920),
    "right_loads_b1_b2": (2600, 2050, 5000, 2920),
    "rps_esf_left": (1220, 2850, 2580, 3760),
    "rps_esf_right": (3100, 2850, 4300, 3760),
    "bottom_interlocks": (1980, 2580, 3900, 3440),
    "lower_center_control_runs": (2100, 2450, 4150, 3420),
    "bus120_to_panels_wide": (1800, 1650, 4200, 3350),
    "notes_legend_title": (5100, 220, 5910, 3860),
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    image = Image.open(RAW)
    for name, box in CROPS.items():
        image.crop(box).save(OUT / f"{name}.png")
    print(f"wrote {len(CROPS)} crops to {OUT}")


if __name__ == "__main__":
    main()
