from pathlib import Path

from PIL import Image


RAW_DIR = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\18\Raw"
)
RAW_IMAGE = RAW_DIR / "raw -- synthetic_nuclear_electrical_schematic_readable.png"
OUT_DIR = RAW_DIR / "codes" / "crops"


CROPS = {
    "full_drawing_area": (250, 180, 5450, 3600),
    "top_sources_and_4160": (260, 200, 5450, 1200),
    "top_left_sources": (260, 200, 2300, 1200),
    "top_center_sources_tie": (2200, 200, 3900, 1200),
    "top_right_sources": (3800, 200, 5450, 1200),
    "load_centers_overview": (260, 1100, 5450, 2300),
    "lc_480a": (260, 1120, 1700, 2300),
    "lc_480b": (1650, 1120, 2900, 2300),
    "lc_480c": (3000, 1120, 4300, 2300),
    "lc_480d": (4200, 1120, 5450, 2300),
    "lower_train_a_control_power": (260, 2450, 2950, 3500),
    "lower_train_b_control_power": (3000, 2450, 5600, 3500),
    "lower_a_relays": (1780, 2820, 2920, 3480),
    "lower_b_relays": (4470, 2820, 5600, 3480),
    "legend_notes": (5480, 240, 6750, 1050),
    "title_block": (5350, 3650, 6800, 4200),
}


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    image = Image.open(RAW_IMAGE)
    for name, box in CROPS.items():
        image.crop(box).save(OUT_DIR / f"{name}.png")
    print(f"Wrote {len(CROPS)} crops to {OUT_DIR}")


if __name__ == "__main__":
    main()
