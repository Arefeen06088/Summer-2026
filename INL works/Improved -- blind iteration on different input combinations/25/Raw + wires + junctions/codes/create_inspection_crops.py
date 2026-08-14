from pathlib import Path

from PIL import Image, ImageOps


Image.MAX_IMAGE_PIXELS = None

DOC = 25
ROOT = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\25\Raw + wires + junctions"
)
RESULTS = ROOT / "results" / "inspection_crops"
FALLBACK_RESULTS = Path(r"C:\Asif_all_python_projects\INL\INL\doc25_work\inspection_crops")

SOURCES = {
    "raw": ROOT / "raw -- synthetic_npp_electrical_schematic_revised_v4.png",
    "nodes": ROOT / "wire_nodes_overlay.png",
    "wires": ROOT / "wires_mask_overlay.png",
    "mask": ROOT / "wires_mask.png",
}

CROPS = {
    "doc25_top_full": (0, 0, 6600, 1250),
    "doc25_top_left": (0, 0, 3350, 1400),
    "doc25_top_right": (3250, 0, 6600, 1400),
    "doc25_mid_full": (0, 1100, 6600, 2600),
    "doc25_mid_left": (0, 1050, 3350, 2850),
    "doc25_mid_right": (3250, 1050, 6600, 2850),
    "doc25_bottom_full": (0, 2400, 6600, 4400),
    "doc25_bottom_left": (0, 2550, 3350, 4400),
    "doc25_bottom_right": (3250, 2550, 6600, 4400),
    "doc25_center_bottom": (2450, 2500, 4200, 4100),
    "doc25_center_control": (2100, 2300, 4550, 3900),
    "doc25_top_center": (2350, 350, 4250, 1350),
    "doc25_left_dc_close": (350, 2550, 3050, 4050),
    "doc25_right_dc_close": (3450, 2550, 6150, 4050),
    "doc25_notes": (350, 3750, 3100, 4400),
    "doc25_title": (4150, 3700, 6600, 4400),
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
