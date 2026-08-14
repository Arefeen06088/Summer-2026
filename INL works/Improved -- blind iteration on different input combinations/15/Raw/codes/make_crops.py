from pathlib import Path

from PIL import Image


RAW_DIR = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\15\Raw")
RAW_IMAGE = RAW_DIR / "raw -- improved_synthetic_nuclear_electrical_schematic.png"
OUT_DIR = RAW_DIR / "codes" / "crops"


def save_crop(img: Image.Image, name: str, box: tuple[int, int, int, int]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    img.crop(box).save(OUT_DIR / f"{name}.png")


def main() -> None:
    img = Image.open(RAW_IMAGE)
    crops = {
        "full_drawing_area": (200, 120, 7200, 3700),
        "top_offsite_sources": (430, 110, 5800, 570),
        "div_1a": (430, 560, 1800, 3650),
        "div_1b": (1760, 560, 3140, 3650),
        "div_2a": (3180, 560, 4560, 3650),
        "div_2b": (4600, 560, 5980, 3650),
        "ties_1a_1b": (1450, 500, 2050, 1400),
        "ties_2a_2b": (4320, 500, 4920, 1400),
        "mcc_1a_branches": (450, 1500, 1760, 2900),
        "mcc_1b_branches": (1780, 1500, 3120, 2900),
        "mcc_2a_branches": (3200, 1500, 4540, 2900),
        "mcc_2b_branches": (4620, 1500, 5960, 2900),
        "dc_1a": (430, 2850, 1800, 3600),
        "dc_1b": (1760, 2850, 3140, 3600),
        "dc_2a": (3180, 2850, 4560, 3600),
        "dc_2b": (4600, 2850, 5980, 3600),
        "right_notes_schedule": (6100, 480, 7200, 3500),
        "title_block": (5200, 4120, 7200, 4700),
    }
    for name, box in crops.items():
        save_crop(img, name, box)
    print(f"wrote {len(crops)} crops to {OUT_DIR}")


if __name__ == "__main__":
    main()
