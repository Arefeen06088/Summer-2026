from pathlib import Path

from PIL import Image


RAW_DIR = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\19\Raw"
)
RAW_IMAGE = RAW_DIR / "raw -- synthetic_npp_electrical_schematic_v3.png"
CROP_DIR = RAW_DIR / "codes" / "crops"


CROPS = {
    "full_drawing_area": (180, 180, 9000, 5350),
    "top_sources_overview": (180, 180, 9000, 1700),
    "top_left_sources": (180, 180, 3300, 1700),
    "top_center_sources": (3200, 180, 6200, 1700),
    "top_right_sources": (6100, 180, 9000, 1700),
    "middle_overview": (180, 1550, 9000, 3300),
    "middle_left": (180, 1550, 3300, 3300),
    "middle_center": (3200, 1550, 6200, 3300),
    "middle_right": (6100, 1550, 9000, 3300),
    "lower_overview": (180, 3150, 9000, 5350),
    "lower_left": (180, 3150, 3300, 5350),
    "lower_center": (3200, 3150, 6200, 5350),
    "lower_right": (6100, 3150, 9000, 5350),
    "far_left_full_height": (180, 180, 2500, 5350),
    "center_full_height": (2500, 180, 6700, 5350),
    "far_right_full_height": (6700, 180, 9000, 5350),
    "legend_title": (7350, 4450, 9000, 5350),
}


def main() -> None:
    CROP_DIR.mkdir(parents=True, exist_ok=True)
    image = Image.open(RAW_IMAGE)
    for name, box in CROPS.items():
        crop = image.crop(box)
        crop.save(CROP_DIR / f"{name}.png")
    print(f"wrote {len(CROPS)} crops to {CROP_DIR}")


if __name__ == "__main__":
    main()
