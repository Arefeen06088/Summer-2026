from pathlib import Path
from PIL import Image, ImageOps


ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\22\Raw + wires + junctions")
RESULTS = ROOT / "results" / "inspection_crops"
FALLBACK_RESULTS = Path(r"C:\Asif_all_python_projects\INL\INL\doc22_work\inspection_crops")

SOURCES = {
    "raw": ROOT / "raw -- synthetic_npp_electrical_schematic_clean.png",
    "nodes": ROOT / "wire_nodes_overlay.png",
    "wires": ROOT / "wires_mask_overlay.png",
    "mask": ROOT / "wires_mask.png",
}

CROPS = {
    "doc22_top_full": (250, 120, 5900, 1150),
    "doc22_top_left": (250, 120, 2200, 1150),
    "doc22_top_center": (2050, 120, 4050, 1150),
    "doc22_top_right": (3900, 120, 5900, 1150),
    "doc22_480_full": (250, 1050, 5900, 2900),
    "doc22_480_a": (250, 1050, 1650, 2900),
    "doc22_480_b": (1500, 1050, 3100, 2900),
    "doc22_480_c": (2950, 1050, 4550, 2900),
    "doc22_480_d": (4400, 1050, 5900, 2900),
    "doc22_lower_full": (250, 2750, 6000, 4400),
    "doc22_lower_a": (250, 2750, 3150, 4400),
    "doc22_lower_b": (3000, 2750, 6000, 4400),
    "doc22_lower_a_left": (250, 2750, 1700, 4400),
    "doc22_lower_a_right": (1550, 2750, 3150, 4400),
    "doc22_lower_b_left": (3000, 2750, 4550, 4400),
    "doc22_lower_b_right": (4400, 2750, 6000, 4400),
    "doc22_bottom_full": (250, 3900, 6000, 5050),
    "doc22_bottom_a": (250, 3900, 3150, 5050),
    "doc22_bottom_b": (3000, 3900, 6000, 5050),
    "doc22_train_left_ct_rhr_close": (1420, 2050, 2850, 3600),
    "doc22_train_mid_ct_rhr_close": (3200, 2050, 4650, 3600),
    "doc22_pt_meter_close": (5100, 3450, 6900, 4550),
    "doc22_notes": (6000, 250, 7100, 2800),
    "doc22_title": (6000, 3400, 7100, 5000),
}


def save_crop(source_name: str, path: Path, output_dir: Path) -> None:
    with Image.open(path) as image:
        for crop_name, box in CROPS.items():
            image.crop(box).save(output_dir / f"{source_name}_{crop_name}.png")
        overview = image.copy()
        overview.thumbnail((1800, 1200))
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
