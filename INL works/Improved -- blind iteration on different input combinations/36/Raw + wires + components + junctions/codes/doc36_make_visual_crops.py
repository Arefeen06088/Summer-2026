from __future__ import annotations

from pathlib import Path

from PIL import Image


Image.MAX_IMAGE_PIXELS = None

BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\36\Raw + wires + components + junctions")
CODES = BASE / "codes"
CROPS = CODES / "crops"
RESULTS = BASE / "results"
CROPS.mkdir(parents=True, exist_ok=True)
RESULTS.mkdir(parents=True, exist_ok=True)

SOURCES = {
    "raw": BASE / "raw -- synthetic_npp_electrical_schematic_v2.png",
    "components": BASE / "detected_components_and_logical_overlay.png",
    "wires": BASE / "wires_mask_overlay.png",
    "wire_nodes": BASE / "wire_nodes_overlay.png",
}

CROPS_DEF = {
    "overview": (0, 0, 4800, 3400),
    "working_area": (80, 80, 4650, 3300),
    "top_left": (80, 80, 1700, 1250),
    "top_center": (1550, 80, 3250, 1250),
    "top_right": (3100, 80, 4650, 1250),
    "mid_left": (80, 1050, 1700, 2350),
    "mid_center": (1550, 1050, 3250, 2350),
    "mid_right": (3100, 1050, 4650, 2350),
    "bottom_left": (80, 2150, 1700, 3300),
    "bottom_center": (1550, 2150, 3250, 3300),
    "bottom_right": (3100, 2150, 4650, 3300),
    "central_ties": (2100, 900, 2900, 2500),
    "left_control": (80, 1850, 2350, 3300),
    "right_control": (2450, 1850, 4650, 3300),
}


def save_crop(source_name: str, source_path: Path, crop_name: str, box: tuple[int, int, int, int]) -> None:
    with Image.open(source_path) as image:
        image = image.convert("RGB")
        crop = image.crop(box)
        if crop_name == "overview":
            overview = crop.copy()
            overview.thumbnail((2400, 1700), Image.Resampling.LANCZOS)
            overview.save(CROPS / f"{source_name}__{crop_name}.png")
            return
        crop.save(CROPS / f"{source_name}__{crop_name}.png")
        crop.resize((crop.width * 2, crop.height * 2), Image.Resampling.LANCZOS).save(
            CROPS / f"{source_name}__{crop_name}_2x.png"
        )


def main() -> None:
    for source_name, source_path in SOURCES.items():
        for crop_name, box in CROPS_DEF.items():
            save_crop(source_name, source_path, crop_name, box)
    print(f"crops: {CROPS}")


if __name__ == "__main__":
    main()
