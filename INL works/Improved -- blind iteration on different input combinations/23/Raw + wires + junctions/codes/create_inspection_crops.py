from pathlib import Path
from PIL import Image, ImageOps


Image.MAX_IMAGE_PIXELS = None

ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\23\Raw + wires + junctions")
RESULTS = ROOT / "results" / "inspection_crops"
FALLBACK_RESULTS = Path(r"C:\Asif_all_python_projects\INL\INL\doc23_work\inspection_crops")

SOURCES = {
    "raw": ROOT / "raw -- synthetic_npp_electrical_schematic_ats_components_shifted_v18.png",
    "nodes": ROOT / "wire_nodes_overlay.png",
    "wires": ROOT / "wires_mask_overlay.png",
    "mask": ROOT / "wires_mask.png",
}

CROPS = {
    "doc23_top_full": (500, 200, 13900, 1900),
    "doc23_top_left": (500, 200, 5000, 1900),
    "doc23_top_center": (4700, 200, 9500, 1900),
    "doc23_top_right": (9000, 200, 13900, 1900),
    "doc23_mid_full": (500, 1700, 13900, 5200),
    "doc23_mid_left": (500, 1700, 5000, 5200),
    "doc23_mid_center": (4700, 1700, 9500, 5200),
    "doc23_mid_right": (9000, 1700, 13900, 5200),
    "doc23_lower_full": (500, 5000, 13900, 7600),
    "doc23_lower_left": (500, 5000, 5000, 7600),
    "doc23_lower_center": (4700, 5000, 9500, 7600),
    "doc23_lower_right": (9000, 5000, 13900, 7600),
    "doc23_bottom_full": (500, 7400, 13900, 9250),
    "doc23_bottom_left": (500, 7400, 5000, 9250),
    "doc23_bottom_center": (4700, 7400, 9500, 9250),
    "doc23_bottom_right": (9000, 7400, 13900, 9250),
    "doc23_bus_4160_ab": (500, 1200, 7200, 2600),
    "doc23_bus_4160_cd": (6500, 1200, 10300, 2600),
    "doc23_ats_1a": (450, 1850, 3850, 5000),
    "doc23_ats_1b": (3550, 1850, 7000, 5000),
    "doc23_ats_1c": (6650, 1850, 10300, 5000),
    "doc23_ats_2a": (450, 4850, 3850, 7450),
    "doc23_ats_2b": (3550, 4850, 7000, 7450),
    "doc23_ats_2c": (6650, 4850, 10300, 7450),
    "doc23_bottom_left_control": (500, 7200, 5200, 9250),
    "doc23_bottom_right_control": (5000, 7200, 10300, 9250),
    "doc23_notes": (11200, 500, 13900, 4700),
    "doc23_title": (11200, 6900, 13900, 9250),
}


def save_crop(source_name: str, path: Path, output_dir: Path) -> None:
    with Image.open(path) as image:
        for crop_name, box in CROPS.items():
            image.crop(box).save(output_dir / f"{source_name}_{crop_name}.png")
        overview = image.copy()
        overview.thumbnail((2200, 1500))
        overview.save(output_dir / f"{source_name}_overview_1800.png")
        if source_name == "raw":
            gray = ImageOps.grayscale(image)
            for crop_name, box in CROPS.items():
                ImageOps.autocontrast(gray.crop(box)).save(output_dir / f"raw_gray_{crop_name}.png")


def main() -> None:
    output_dir = RESULTS
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        output_dir = FALLBACK_RESULTS
        output_dir.mkdir(parents=True, exist_ok=True)
    for source_name, path in SOURCES.items():
        if path.exists():
            save_crop(source_name, path, output_dir)
    print(f"inspection crops written to {output_dir}")


if __name__ == "__main__":
    main()
