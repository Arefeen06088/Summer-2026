from pathlib import Path
from PIL import Image, ImageOps


ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\15\Raw + wires + junctions")
RESULTS = ROOT / "results" / "inspection_crops"

SOURCES = {
    "raw": ROOT / "raw -- improved_synthetic_nuclear_electrical_schematic.png",
    "nodes": ROOT / "wire_nodes_overlay.png",
    "wires": ROOT / "wires_mask_overlay.png",
    "mask": ROOT / "wires_mask.png",
}

CROPS = {
    "top_offsite_sources": (450, 50, 5850, 650),
    "division_1A_full": (300, 520, 1850, 3600),
    "division_1B_full": (1780, 520, 3350, 3600),
    "division_2A_full": (3300, 520, 4850, 3600),
    "division_2B_full": (4780, 520, 6350, 3600),
    "division_1A_upper": (300, 520, 1850, 1530),
    "division_1B_upper": (1780, 520, 3350, 1530),
    "division_2A_upper": (3300, 520, 4850, 1530),
    "division_2B_upper": (4780, 520, 6350, 1530),
    "division_1A_mcc_loads": (300, 1450, 1850, 2920),
    "division_1B_mcc_loads": (1780, 1450, 3350, 2920),
    "division_2A_mcc_loads": (3300, 1450, 4850, 2920),
    "division_2B_mcc_loads": (4780, 1450, 6350, 2920),
    "division_1A_dc_ups": (300, 2820, 1850, 3650),
    "division_1B_dc_ups": (1780, 2820, 3350, 3650),
    "division_2A_dc_ups": (3300, 2820, 4850, 3650),
    "division_2B_dc_ups": (4780, 2820, 6350, 3650),
    "center_ties_and_annunciator": (3000, 600, 5000, 3600),
    "right_notes_tables": (6300, 500, 7420, 3550),
    "title_block": (5250, 4200, 7380, 4850),
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
