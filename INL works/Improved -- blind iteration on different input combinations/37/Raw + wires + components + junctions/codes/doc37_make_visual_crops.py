from __future__ import annotations

from pathlib import Path

from PIL import Image


Image.MAX_IMAGE_PIXELS = None

BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\37\Raw + wires + components + junctions"
)
CODES = BASE / "codes"
CROPS = CODES / "crops"
RESULTS = BASE / "results"
CROPS.mkdir(parents=True, exist_ok=True)
RESULTS.mkdir(parents=True, exist_ok=True)

SOURCES = {
    "raw": BASE / "raw -- synthetic_npp_electrical_schematic_v2(1).png",
    "components": BASE / "detected_components_and_logical_overlay.png",
    "wires": BASE / "wires_mask_overlay.png",
    "wire_nodes": BASE / "wire_nodes_overlay.png",
}

CROPS_DEF = {
    "overview": (0, 0, 5100, 3300),
    "working_area": (120, 120, 4960, 3180),
    "top_sources": (1500, 120, 3500, 620),
    "top_left_train": (200, 430, 2600, 1600),
    "top_right_train": (2500, 430, 4900, 1600),
    "mid_left_loads": (220, 1500, 2550, 2650),
    "mid_right_loads": (2550, 1500, 4900, 2650),
    "bottom_left_dc": (1750, 1850, 2600, 3000),
    "bottom_right_dc": (2500, 1850, 3350, 3000),
    "bottom_control": (1750, 2500, 3450, 3220),
    "left_mcc_detail": (260, 1700, 1950, 2820),
    "right_mcc_detail": (3050, 1700, 4750, 2820),
    "center_tie_control": (2150, 390, 3000, 1900),
}


def save_crop(name: str, image: Image.Image, box: tuple[int, int, int, int], source_name: str) -> None:
    crop = image.crop(box)
    out = CROPS / f"{source_name}__{name}.png"
    crop.save(out)
    if name != "overview":
        w, h = crop.size
        crop.resize((w * 2, h * 2), Image.Resampling.LANCZOS).save(
            CROPS / f"{source_name}__{name}_2x.png"
        )


def main() -> None:
    for source_name, path in SOURCES.items():
        image = Image.open(path).convert("RGB")
        for crop_name, box in CROPS_DEF.items():
            save_crop(crop_name, image, box, source_name)
    print(f"Saved crops to {CROPS}")


if __name__ == "__main__":
    main()
