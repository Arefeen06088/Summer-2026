from pathlib import Path

from PIL import Image, ImageOps


Image.MAX_IMAGE_PIXELS = None

ROOT = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\26\Raw + wires + junctions"
)
RESULTS = ROOT / "results" / "inspection_crops"
FALLBACK_RESULTS = Path(r"C:\Asif_all_python_projects\INL\INL\doc26_work\inspection_crops")

SOURCES = {
    "raw": ROOT / "raw -- synthetic_npp_electrical_schematic_v3(1).png",
    "nodes": ROOT / "wire_nodes_overlay.png",
    "wires": ROOT / "wires_mask_overlay.png",
    "mask": ROOT / "wires_mask.png",
}

CROPS = {
    "doc26_top_full": (0, 0, 7000, 1300),
    "doc26_top_left": (0, 0, 3500, 1450),
    "doc26_top_right": (3450, 0, 7000, 1450),
    "doc26_mid_full": (0, 1100, 7000, 2700),
    "doc26_mid_left": (0, 1050, 3550, 2950),
    "doc26_mid_right": (3450, 1050, 7000, 2950),
    "doc26_bottom_full": (0, 2450, 7000, 4334),
    "doc26_bottom_left": (0, 2500, 3550, 4334),
    "doc26_bottom_right": (3450, 2500, 7000, 4334),
    "doc26_center_bottom": (2500, 2500, 4550, 4200),
    "doc26_center_control": (2150, 2200, 4900, 3950),
    "doc26_top_center": (2450, 300, 4550, 1350),
    "doc26_left_dc_close": (350, 2500, 3150, 4100),
    "doc26_right_dc_close": (3650, 2500, 6500, 4100),
    "doc26_notes": (4300, 1050, 6900, 2300),
    "doc26_title": (4300, 2850, 6900, 4334),
    "doc26_feeder_left_close": (300, 700, 2450, 2400),
    "doc26_feeder_mid_close": (2400, 700, 4800, 2400),
    "doc26_feeder_right_close": (4550, 700, 7000, 2400),
    "doc26_bottom_rps_close": (300, 2850, 6250, 4334),
    "doc26_A_mcc_control_close": (600, 1750, 3500, 3400),
    "doc26_B_mcc_control_close": (3500, 1750, 6500, 3400),
    "doc26_A_ups_close": (700, 2850, 3600, 4334),
    "doc26_B_ups_close": (3600, 2850, 6500, 4334),
    "doc26_A_interlock_routes": (1700, 1250, 4300, 3900),
    "doc26_B_interlock_routes": (4300, 1250, 6900, 3900),
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
