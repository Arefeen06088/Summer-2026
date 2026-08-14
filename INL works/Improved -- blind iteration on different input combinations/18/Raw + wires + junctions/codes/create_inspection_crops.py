from pathlib import Path
from PIL import Image, ImageOps


ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\18\Raw + wires + junctions")
RESULTS = ROOT / "results" / "inspection_crops"

SOURCES = {
    "raw": ROOT / "raw -- synthetic_nuclear_electrical_schematic_readable.png",
    "nodes": ROOT / "wire_nodes_overlay.png",
    "wires": ROOT / "wires_mask_overlay.png",
    "mask": ROOT / "wires_mask.png",
}

CROPS = {
    "top_sources_full": (220, 180, 5600, 1120),
    "top_left_sources": (220, 180, 2350, 1120),
    "top_center_sources": (2200, 180, 4200, 1120),
    "top_right_sources": (4000, 180, 5600, 1120),
    "mid_loads_full": (220, 1000, 5600, 2100),
    "mid_loads_left_a": (220, 1000, 1700, 2100),
    "mid_loads_left_b": (1580, 1000, 3050, 2100),
    "mid_loads_right_c": (3000, 1000, 4450, 2100),
    "mid_loads_right_d": (4320, 1000, 5750, 2100),
    "lower_controls_full": (220, 2550, 5750, 3650),
    "lower_left_controls": (220, 2550, 3000, 3650),
    "lower_right_controls": (3000, 2550, 5750, 3650),
    "lower_left_dc": (500, 2850, 2450, 3500),
    "lower_right_dc": (3200, 2850, 5150, 3500),
    "right_notes_tables": (5700, 250, 6800, 1050),
    "title_block": (5450, 3700, 6900, 4300),
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
