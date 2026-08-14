from pathlib import Path
from PIL import Image, ImageOps


ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\21\Raw + wires + junctions")
RESULTS = ROOT / "results" / "inspection_crops"

SOURCES = {
    "raw": ROOT / "raw -- synthetic_npp_electrical_schematic_fixed.png",
    "nodes": ROOT / "wire_nodes_overlay.png",
    "wires": ROOT / "wires_mask_overlay.png",
    "mask": ROOT / "wires_mask.png",
}

CROPS = {
    "doc21_top_full": (250, 120, 5900, 1150),
    "doc21_top_left": (250, 120, 2200, 1150),
    "doc21_top_center": (2050, 120, 4050, 1150),
    "doc21_top_right": (3900, 120, 5900, 1150),
    "doc21_480_full": (250, 1050, 5900, 2900),
    "doc21_480_a": (250, 1050, 1650, 2900),
    "doc21_480_b": (1500, 1050, 3100, 2900),
    "doc21_480_c": (2950, 1050, 4550, 2900),
    "doc21_480_d": (4400, 1050, 5900, 2900),
    "doc21_lower_full": (250, 2750, 6000, 4400),
    "doc21_lower_a": (250, 2750, 3150, 4400),
    "doc21_lower_b": (3000, 2750, 6000, 4400),
    "doc21_lower_a_left": (250, 2750, 1700, 4400),
    "doc21_lower_a_right": (1550, 2750, 3150, 4400),
    "doc21_lower_b_left": (3000, 2750, 4550, 4400),
    "doc21_lower_b_right": (4400, 2750, 6000, 4400),
    "doc21_notes": (6000, 250, 7100, 2800),
    "doc21_title": (6000, 3400, 7100, 5000),
}


def save_crop(source_name: str, path: Path) -> None:
    with Image.open(path) as image:
        for crop_name, box in CROPS.items():
            image.crop(box).save(RESULTS / f"{source_name}_{crop_name}.png")
        overview = image.copy()
        overview.thumbnail((1800, 1200))
        overview.save(RESULTS / f"{source_name}_overview_1800.png")
        if source_name == "raw":
            gray = ImageOps.grayscale(image)
            for crop_name, box in CROPS.items():
                ImageOps.autocontrast(gray.crop(box)).save(RESULTS / f"raw_gray_{crop_name}.png")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    for source_name, path in SOURCES.items():
        if path.exists():
            save_crop(source_name, path)
    print(f"inspection crops written to {RESULTS}")


if __name__ == "__main__":
    main()
