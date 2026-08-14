from pathlib import Path
from PIL import Image, ImageOps


ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\16\Raw + wires + junctions")
RESULTS = ROOT / "results" / "inspection_crops"

SOURCES = {
    "raw": ROOT / "raw -- synthetic_npp_electrical_schematic_revised(1).png",
    "nodes": ROOT / "wire_nodes_overlay.png",
    "wires": ROOT / "wires_mask_overlay.png",
    "mask": ROOT / "wires_mask.png",
}

CROPS = {
    "top_offsite_sources": (240, 25, 3150, 360),
    "division_1A_full": (155, 280, 1000, 1980),
    "division_1B_full": (950, 280, 1810, 1980),
    "division_2A_full": (1765, 280, 2615, 1980),
    "division_2B_full": (2565, 280, 3425, 1980),
    "division_1A_upper": (155, 280, 1000, 840),
    "division_1B_upper": (950, 280, 1810, 840),
    "division_2A_upper": (1765, 280, 2615, 840),
    "division_2B_upper": (2565, 280, 3425, 840),
    "division_1A_mcc_loads": (155, 790, 1000, 1605),
    "division_1B_mcc_loads": (950, 790, 1810, 1605),
    "division_2A_mcc_loads": (1765, 790, 2615, 1605),
    "division_2B_mcc_loads": (2565, 790, 3425, 1605),
    "division_1A_dc_ups": (155, 1540, 1000, 2005),
    "division_1B_dc_ups": (950, 1540, 1810, 2005),
    "division_2A_dc_ups": (1765, 1540, 2615, 2005),
    "division_2B_dc_ups": (2565, 1540, 3425, 2005),
    "center_ties_and_annunciator": (1600, 325, 2700, 1980),
    "lower_left_controls": (0, 1580, 1500, 2360),
    "lower_center_controls": (1250, 1580, 2850, 2360),
    "lower_right_controls": (2450, 1580, 3600, 2360),
    "dc_buses_full": (0, 2050, 3250, 2700),
    "right_notes_tables": (3385, 275, 4000, 1940),
    "title_block": (2820, 2290, 3975, 2660),
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
