from pathlib import Path

from PIL import Image, ImageOps


Image.MAX_IMAGE_PIXELS = None

ROOT = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\24\Raw + wires + junctions"
)
RESULTS = ROOT / "results" / "inspection_crops"
FALLBACK_RESULTS = Path(r"C:\Asif_all_python_projects\INL\INL\doc24_work\inspection_crops")

SOURCES = {
    "raw": ROOT / "raw -- synthetic_npp_electrical_schematic_rev2.png",
    "nodes": ROOT / "wire_nodes_overlay.png",
    "wires": ROOT / "wires_mask_overlay.png",
    "mask": ROOT / "wires_mask.png",
}

CROPS = {
    "doc24_top_full": (0, 0, 9200, 1700),
    "doc24_top_left": (0, 0, 4700, 1900),
    "doc24_top_right": (4500, 0, 9200, 1900),
    "doc24_mid_full": (0, 1500, 9200, 3600),
    "doc24_mid_left": (0, 1600, 4700, 3900),
    "doc24_mid_right": (4500, 1600, 9200, 3900),
    "doc24_bottom_full": (0, 3400, 9200, 6200),
    "doc24_bottom_left": (0, 3600, 4700, 6200),
    "doc24_bottom_right": (4500, 3600, 9200, 6200),
    "doc24_center_bottom": (3600, 3500, 5600, 5600),
    "doc24_center_control": (3000, 3200, 6200, 5200),
    "doc24_top_center": (3300, 500, 5900, 1800),
    "doc24_left_dc_close": (500, 3600, 4200, 5600),
    "doc24_right_dc_close": (4800, 3600, 8500, 5600),
    "doc24_notes": (550, 5300, 4300, 6100),
    "doc24_title": (5850, 5250, 9000, 6100),
}


def save_crop(source_name: str, path: Path, output_dir: Path) -> None:
    with Image.open(path) as image:
        for crop_name, box in CROPS.items():
            image.crop(box).save(output_dir / f"{source_name}_{crop_name}.png")
        overview = image.copy()
        overview.thumbnail((2200, 1500))
        overview.save(output_dir / f"{source_name}_overview_1800.png")
        if source_name == "raw":
            gray = ImageOps.autocontrast(ImageOps.grayscale(image))
            for crop_name, box in CROPS.items():
                gray.crop(box).save(output_dir / f"raw_gray_{crop_name}.png")


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
