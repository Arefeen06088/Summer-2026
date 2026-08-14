from pathlib import Path
from PIL import Image, ImageOps


ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\11\Raw + wires + junctions")
RESULTS = ROOT / "results" / "inspection_crops"

SOURCES = {
    "raw": ROOT / "raw -- synthetic_npp_electrical_schematic_relocated_names.png",
    "nodes": ROOT / "wire_nodes_overlay.png",
    "wires": ROOT / "wires_mask_overlay.png",
    "mask": ROOT / "wires_mask.png",
}

CROPS = {
    "full_left_power": (420, 240, 3260, 1300),
    "full_right_power": (3150, 240, 6200, 1300),
    "train_A_upper": (470, 620, 1850, 1850),
    "train_A_lower": (470, 1750, 1850, 3650),
    "train_B_upper": (1820, 620, 3250, 1850),
    "train_B_lower": (1820, 1750, 3250, 3650),
    "train_C_upper": (3200, 620, 4700, 1850),
    "train_C_lower": (3200, 1750, 4700, 3650),
    "train_D_upper": (4580, 620, 6100, 1850),
    "train_D_lower": (4580, 1750, 6100, 3650),
    "bottom_left_dc": (520, 3450, 2850, 4380),
    "bottom_center_interlocks": (2300, 3250, 4300, 4200),
    "bottom_right_dc": (3550, 3450, 5650, 4380),
    "legend_title": (6060, 420, 7150, 4580),
}


def save_crop(source_name: str, path: Path) -> None:
    with Image.open(path) as image:
        for crop_name, box in CROPS.items():
            crop = image.crop(box)
            crop.save(RESULTS / f"{source_name}_{crop_name}.png")

        overview = image.copy()
        overview.thumbnail((1800, 1200))
        overview.save(RESULTS / f"{source_name}_overview_1800.png")

        if source_name == "raw":
            gray = ImageOps.grayscale(image)
            for crop_name, box in CROPS.items():
                crop = gray.crop(box)
                crop = ImageOps.autocontrast(crop)
                crop.save(RESULTS / f"raw_gray_{crop_name}.png")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    for source_name, path in SOURCES.items():
        if path.exists():
            save_crop(source_name, path)
    print(f"inspection crops written to {RESULTS}")


if __name__ == "__main__":
    main()
