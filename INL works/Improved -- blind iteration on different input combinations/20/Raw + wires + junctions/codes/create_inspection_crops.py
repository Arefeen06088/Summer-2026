from pathlib import Path
from PIL import Image, ImageOps


ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\20\Raw + wires + junctions")
RESULTS = ROOT / "results" / "inspection_crops"

SOURCES = {
    "raw": ROOT / "raw -- synthetic_npp_electrical_schematic_v3_label_clearance.png",
    "nodes": ROOT / "wire_nodes_overlay.png",
    "wires": ROOT / "wires_mask_overlay.png",
    "mask": ROOT / "wires_mask.png",
}

CROPS = {
    "doc20_top_full": (280, 120, 4800, 950),
    "doc20_top_left": (280, 120, 1900, 950),
    "doc20_top_center": (1700, 120, 3400, 950),
    "doc20_top_right": (3200, 120, 4800, 950),
    "doc20_480_full": (280, 930, 4800, 2350),
    "doc20_480_a": (280, 930, 1320, 2350),
    "doc20_480_b": (1180, 930, 2500, 2350),
    "doc20_480_c": (2350, 930, 3650, 2350),
    "doc20_480_d": (3500, 930, 4800, 2350),
    "doc20_lower_full": (280, 2200, 4850, 3450),
    "doc20_lower_a": (280, 2200, 2500, 3450),
    "doc20_lower_b": (2450, 2200, 4850, 3450),
    "doc20_lower_a_left": (280, 2200, 1350, 3450),
    "doc20_lower_a_right": (1250, 2200, 2500, 3450),
    "doc20_lower_b_left": (2450, 2200, 3650, 3450),
    "doc20_lower_b_right": (3550, 2200, 4850, 3450),
    "doc20_notes": (4950, 250, 6000, 2300),
    "doc20_title": (4950, 3000, 6000, 4200),
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
