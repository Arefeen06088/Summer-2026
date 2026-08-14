from pathlib import Path

from PIL import Image, ImageOps


Image.MAX_IMAGE_PIXELS = None

ROOT = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\27\Raw + wires + junctions"
)
RESULTS = ROOT / "results" / "inspection_crops"
FALLBACK_RESULTS = Path(r"C:\Asif_all_python_projects\INL\INL\doc27_work\inspection_crops")

SOURCES = {
    "raw": ROOT / "raw -- synthetic_npp_electrical_schematic_readable.png",
    "nodes": ROOT / "wire_nodes_overlay.png",
    "wires": ROOT / "wires_mask_overlay.png",
    "mask": ROOT / "wires_mask.png",
}

CROPS = {
    "doc27_top_full": (0, 0, 10522, 2100),
    "doc27_mid_full": (0, 1800, 10522, 5000),
    "doc27_bottom_full": (0, 4700, 10522, 7307),
    "doc27_left_full": (0, 0, 3700, 7307),
    "doc27_center_full": (3300, 0, 7200, 7307),
    "doc27_right_full": (6800, 0, 10522, 7307),
    "doc27_top_left": (0, 0, 3800, 2500),
    "doc27_top_center": (3300, 0, 7200, 2500),
    "doc27_top_right": (6800, 0, 10522, 2500),
    "doc27_mid_left": (0, 1800, 3900, 5200),
    "doc27_mid_center": (3300, 1800, 7200, 5200),
    "doc27_mid_right": (6800, 1800, 10522, 5200),
    "doc27_bottom_left": (0, 4700, 3900, 7307),
    "doc27_bottom_center": (3300, 4700, 7200, 7307),
    "doc27_bottom_right": (6800, 4700, 10522, 7307),
    "doc27_title": (7350, 5600, 10522, 7307),
    "doc27_notes_legend": (0, 5300, 4200, 7307),
    "doc27_control_center": (3000, 3500, 7600, 6400),
    "doc27_lower_bus_center": (2600, 4550, 8200, 7307),
    "doc27_ab_dc_detail": (3450, 2500, 5850, 4550),
    "doc27_b_right_feeders": (6500, 2500, 8500, 4800),
    "doc27_d_right_ground": (6500, 4150, 9000, 7050),
    "doc27_right_notes_legend": (7000, 900, 10350, 6750),
}


def save_crop(source_name: str, path: Path, output_dir: Path) -> None:
    with Image.open(path) as image:
        for crop_name, box in CROPS.items():
            image.crop(box).save(output_dir / f"{source_name}_{crop_name}.png")
        overview = image.copy()
        overview.thumbnail((2400, 1800))
        overview.save(output_dir / f"{source_name}_overview_2400.png")
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
