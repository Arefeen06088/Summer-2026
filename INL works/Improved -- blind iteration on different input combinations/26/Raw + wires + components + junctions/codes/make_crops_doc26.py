from __future__ import annotations

from pathlib import Path

from PIL import Image


Image.MAX_IMAGE_PIXELS = None

BASE = Path(__file__).resolve().parents[1]
CROPS = BASE / "codes" / "crops"
CROPS.mkdir(parents=True, exist_ok=True)

SOURCES = {
    "raw": BASE / "raw -- synthetic_npp_electrical_schematic_v3(1).png",
    "components": BASE / "detected_components_overlay.png",
    "wires": BASE / "wires_mask_overlay.png",
    "wire_nodes": BASE / "wire_nodes_overlay.png",
}

CROPS_DEF = {
    "overview": (0, 0, 7000, 4334),
    "working_area": (180, 180, 6820, 4050),
    "top_left": (180, 180, 2500, 1600),
    "top_center": (2350, 180, 4800, 1600),
    "top_right": (4650, 180, 6820, 1600),
    "mid_left": (180, 1450, 2500, 3000),
    "mid_center": (2350, 1450, 4800, 3000),
    "mid_right": (4650, 1450, 6820, 3000),
    "bottom_left": (180, 2850, 2500, 4050),
    "bottom_center": (2350, 2850, 4800, 4050),
    "bottom_right": (4650, 2850, 6820, 4050),
    "deep_bottom_left": (180, 3300, 2500, 4334),
    "deep_bottom_center": (2350, 3300, 4800, 4334),
    "deep_bottom_right": (4650, 3300, 6820, 4334),
    "central_control": (2850, 1300, 4300, 3900),
    "bottom_a_control": (700, 2700, 3600, 4100),
    "bottom_b_control": (3450, 2700, 6450, 4100),
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
