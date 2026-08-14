from pathlib import Path
from PIL import Image, ImageOps


ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\17\Raw + wires + junctions")
RESULTS = ROOT / "results" / "inspection_crops"

SOURCES = {
    "raw": ROOT / "raw -- synthetic_npp_aux_power_schematic_overlap_fixed.png",
    "nodes": ROOT / "wire_nodes_overlay.png",
    "wires": ROOT / "wires_mask_overlay.png",
    "mask": ROOT / "wires_mask.png",
}

CROPS = {
    "top_ac_full": (160, 150, 4150, 1180),
    "top_left_train": (160, 170, 2100, 1220),
    "top_right_train": (2000, 170, 4150, 1220),
    "top_center_ties": (1800, 130, 2600, 1220),
    "mid_loads_full": (160, 1050, 4200, 1900),
    "mid_left_loads": (160, 1050, 2100, 1900),
    "mid_right_loads": (2050, 1050, 4200, 1900),
    "lower_controls_full": (160, 2100, 4200, 3420),
    "lower_left_controls": (160, 2100, 2100, 3420),
    "lower_right_controls": (2050, 2100, 4200, 3420),
    "lower_center_controls": (1500, 2100, 2800, 3420),
    "far_left_verticals": (130, 600, 780, 3400),
    "far_right_verticals": (3550, 600, 4300, 3400),
    "right_notes_tables": (4200, 200, 5420, 2700),
    "title_block": (4200, 2780, 5420, 3420),
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
