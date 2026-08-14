from __future__ import annotations

from pathlib import Path

from PIL import Image


Image.MAX_IMAGE_PIXELS = None

BASE = Path(__file__).resolve().parents[1]
CROPS = BASE / "codes" / "crops"
CROPS.mkdir(parents=True, exist_ok=True)

SOURCES = {
    "raw": BASE / "raw -- synthetic_npp_electrical_schematic_rev2.png",
    "components": BASE / "detected_components_overlay.png",
    "wires": BASE / "wires_mask_overlay.png",
    "wire_nodes": BASE / "wire_nodes_overlay.png",
}

CROPS_DEF = {
    "overview": (0, 0, 9200, 6200),
    "working_area": (250, 250, 8600, 5850),
    "top_left": (250, 250, 3300, 2100),
    "top_center": (3000, 250, 6100, 2100),
    "top_right": (5900, 250, 8600, 2100),
    "mid_left": (250, 1800, 3300, 4000),
    "mid_center": (3000, 1800, 6100, 4000),
    "mid_right": (5900, 1800, 8600, 4000),
    "bottom_left": (250, 3800, 3300, 5850),
    "bottom_center": (3000, 3800, 6100, 5850),
    "bottom_right": (5900, 3800, 8600, 5850),
    "legend_title": (6900, 3200, 9000, 6000),
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
