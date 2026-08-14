from pathlib import Path

from PIL import Image


RAW_DIR = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\20\Raw"
)
RAW_IMAGE = RAW_DIR / "raw -- synthetic_npp_electrical_schematic_v3_label_clearance.png"
CROP_DIR = RAW_DIR / "codes" / "crops"


CROPS = {
    "full_drawing_area": (90, 120, 6040, 4100),
    "top_overview": (90, 120, 6040, 1220),
    "top_left_sources": (90, 120, 2200, 1220),
    "top_center_ties": (2100, 120, 4150, 1220),
    "top_right_sources": (4050, 120, 6040, 1220),
    "middle_overview": (90, 1050, 6040, 2700),
    "middle_left_feeders": (90, 1050, 2200, 2700),
    "middle_center_feeders": (2100, 1050, 4150, 2700),
    "middle_right_feeders": (4050, 1050, 6040, 2700),
    "lower_overview": (90, 2600, 6040, 4100),
    "lower_left_control": (90, 2600, 2200, 4100),
    "lower_center_control": (2100, 2600, 4150, 4100),
    "lower_right_notes_title": (4050, 2600, 6040, 4100),
    "left_full_height": (90, 120, 2200, 4100),
    "center_full_height": (2100, 120, 4150, 4100),
    "right_full_height": (4050, 120, 6040, 4100),
}


def main() -> None:
    CROP_DIR.mkdir(parents=True, exist_ok=True)
    image = Image.open(RAW_IMAGE)
    for name, box in CROPS.items():
        image.crop(box).save(CROP_DIR / f"{name}.png")
    print(f"wrote {len(CROPS)} crops to {CROP_DIR}")


if __name__ == "__main__":
    main()
