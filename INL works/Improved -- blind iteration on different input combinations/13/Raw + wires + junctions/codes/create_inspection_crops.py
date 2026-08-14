from pathlib import Path
from PIL import Image, ImageOps


ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\13\Raw + wires + junctions")
RESULTS = ROOT / "results" / "inspection_crops"

SOURCES = {
    "raw": ROOT / "raw -- synthetic diagram _.png",
    "nodes": ROOT / "wire_nodes_overlay.png",
    "wires": ROOT / "wires_mask_overlay.png",
    "mask": ROOT / "wires_mask.png",
}

CROPS = {
    "startup_source_top_left": (330, 360, 1850, 780),
    "top_intertrain_sources": (1120, 620, 5020, 1050),
    "train_A_full": (420, 790, 2560, 1880),
    "train_B_full": (2720, 790, 4860, 1880),
    "train_C_full": (420, 2030, 2560, 3140),
    "train_D_full": (2720, 2030, 4860, 3140),
    "train_A_loads_left": (600, 1160, 1560, 1740),
    "train_A_loads_right_dc": (1490, 1120, 2480, 1770),
    "train_B_loads_left": (2880, 1160, 3850, 1740),
    "train_B_loads_right_dc": (3760, 1120, 4760, 1770),
    "train_C_loads_left": (600, 2410, 1560, 3000),
    "train_C_loads_right_dc": (1490, 2360, 2480, 3010),
    "train_D_loads_left": (2880, 2410, 3850, 3000),
    "train_D_loads_right_dc": (3760, 2360, 4760, 3010),
    "bottom_grounding_shared": (390, 3020, 2820, 3650),
    "center_vertical_ties": (2350, 700, 3040, 3700),
    "right_notes_legend": (5060, 240, 6260, 4170),
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
