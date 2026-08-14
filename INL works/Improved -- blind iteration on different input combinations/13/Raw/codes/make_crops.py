from pathlib import Path

from PIL import Image


RAW_DIR = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\13\Raw")
RAW_IMAGE = RAW_DIR / "raw -- synthetic diagram _.png"
OUT_DIR = RAW_DIR / "codes" / "crops"


def save_crop(img: Image.Image, name: str, box: tuple[int, int, int, int]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    crop = img.crop(box)
    crop.save(OUT_DIR / f"{name}.png")


def main() -> None:
    img = Image.open(RAW_IMAGE)
    # Coordinate boxes are chosen from the full 6400 x 4300 raw schematic.
    crops = {
        "full_drawing_area": (150, 150, 5075, 3400),
        "top_left_train_a": (300, 380, 2600, 1900),
        "top_right_train_b": (2600, 450, 4900, 1900),
        "bottom_left_train_c": (260, 1850, 2600, 3350),
        "bottom_right_train_d": (2600, 1850, 4950, 3350),
        "station_startup_source": (330, 360, 1800, 900),
        "left_middle_alternate_feed": (180, 1800, 1700, 2300),
        "dc_ups_a": (2150, 1050, 2520, 1850),
        "dc_ups_b": (4430, 1050, 4800, 1850),
        "dc_ups_c": (2150, 2500, 2520, 3300),
        "dc_ups_d": (4430, 2500, 4800, 3300),
        "right_notes_legend_schedule": (5050, 210, 6250, 2950),
    }
    for name, box in crops.items():
        save_crop(img, name, box)
    print(f"wrote {len(crops)} crops to {OUT_DIR}")


if __name__ == "__main__":
    main()
