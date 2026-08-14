from pathlib import Path

from PIL import Image


RAW_DIR = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\14\Raw")
RAW_IMAGE = RAW_DIR / "raw -- synthetic_npp_electrical_schematic_even_bus_spacing (1).png"
OUT_DIR = RAW_DIR / "codes" / "crops"


def save_crop(img: Image.Image, name: str, box: tuple[int, int, int, int]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    img.crop(box).save(OUT_DIR / f"{name}.png")


def main() -> None:
    img = Image.open(RAW_IMAGE)
    crops = {
        "full_drawing_area": (130, 120, 6350, 3970),
        "upper_train_a_4160": (470, 250, 2800, 1600),
        "upper_train_b_4160": (3000, 250, 5320, 1600),
        "middle_train_a_480": (470, 1520, 2800, 2840),
        "middle_train_b_480": (3000, 1520, 5320, 2840),
        "lower_dc_ups_a": (480, 2820, 2810, 3910),
        "lower_dc_ups_b": (3000, 2820, 5320, 3910),
        "center_ties": (2570, 640, 3200, 3600),
        "panel_bundle_a": (610, 2450, 2850, 3300),
        "panel_bundle_b": (2850, 2450, 5300, 3300),
        "center_panel_bundle": (2600, 2500, 3600, 3600),
        "bottom_terminal_blocks": (500, 3650, 3150, 3970),
        "notes_legend_title": (5300, 250, 6250, 3860),
        "label_check_a05_a09": (2050, 1750, 3800, 2820),
        "label_check_b05_b08": (4100, 1750, 5400, 2820),
    }
    for name, box in crops.items():
        save_crop(img, name, box)
    print(f"wrote {len(crops)} crops to {OUT_DIR}")


if __name__ == "__main__":
    main()
