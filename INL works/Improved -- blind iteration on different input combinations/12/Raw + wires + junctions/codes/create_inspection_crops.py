from pathlib import Path
from PIL import Image, ImageOps


ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\12\Raw + wires + junctions")
RESULTS = ROOT / "results" / "inspection_crops"

SOURCES = {
    "raw": ROOT / "raw -- synthetic_npp_electrical_schematic_rps_rerouted.png",
    "nodes": ROOT / "wire_nodes_overlay.png",
    "wires": ROOT / "wires_mask_overlay.png",
    "mask": ROOT / "wires_mask.png",
}

CROPS = {
    "top_sources_and_4160_buses": (170, 130, 3260, 760),
    "train_A_upper": (190, 480, 1680, 1280),
    "train_A_lower_loads": (190, 1000, 1680, 1900),
    "train_B_upper": (1800, 480, 3260, 1280),
    "train_B_lower_loads": (1800, 1000, 3260, 1900),
    "dc_buses_and_ats": (1060, 1800, 2900, 2350),
    "bottom_left_logic": (780, 2180, 1700, 2790),
    "bottom_center_logic": (1450, 2140, 2500, 2810),
    "bottom_right_logic": (2240, 2180, 3300, 2790),
    "full_bottom_interlocks": (170, 1980, 3400, 2850),
    "left_outer_interlocks": (140, 500, 530, 2860),
    "right_outer_interlocks": (3100, 500, 3380, 2350),
    "legend_title": (3260, 120, 4110, 2860),
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
                crop = ImageOps.autocontrast(gray.crop(box))
                crop.save(RESULTS / f"raw_gray_{crop_name}.png")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    for source_name, path in SOURCES.items():
        if path.exists():
            save_crop(source_name, path)
    print(f"inspection crops written to {RESULTS}")


if __name__ == "__main__":
    main()
