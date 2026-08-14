from __future__ import annotations

from pathlib import Path

from PIL import Image


Image.MAX_IMAGE_PIXELS = None

BASE = Path(__file__).resolve().parents[1]
CROPS = BASE / "codes" / "crops"
CROPS.mkdir(parents=True, exist_ok=True)

SOURCES = {
    "raw": BASE / "raw -- synthetic_npp_electrical_schematic_revised_v4.png",
    "components": BASE / "detected_components_overlay.png",
    "wires": BASE / "wires_mask_overlay.png",
    "wire_nodes": BASE / "wire_nodes_overlay.png",
}

CROPS_DEF = {
    "overview": (0, 0, 6600, 4400),
    "working_area": (200, 160, 6200, 4150),
    "top_left": (180, 180, 2500, 1450),
    "top_center": (2300, 180, 4500, 1450),
    "top_right": (4300, 180, 6300, 1450),
    "mid_left": (180, 1250, 2500, 2850),
    "mid_center": (2300, 1250, 4500, 2850),
    "mid_right": (4300, 1250, 6300, 2850),
    "bottom_left": (180, 2750, 2500, 4200),
    "bottom_center": (2300, 2750, 4500, 4200),
    "bottom_right": (4300, 2750, 6300, 4200),
    "legend_title": (4350, 3100, 6500, 4350),
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


if __name__ == "__main__":
    main()
