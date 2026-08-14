from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageOps


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\19\Raw + wires")
OUT = BASE / "codes" / "crops_doc19"

SOURCES = {
    "raw": BASE / "raw -- synthetic_npp_electrical_schematic_v3.png",
    "overlay": BASE / "wires_mask_overlay.png",
    "mask": BASE / "wires_mask.png",
}

CROPS = {
    "overview": (0, 0, 9200, 5600),
    "drawing_area": (260, 230, 7750, 4350),
    "top_all": (600, 230, 7450, 1050),
    "top_div_a": (650, 220, 4000, 1100),
    "top_div_b": (4800, 220, 7450, 1100),
    "tie_4160_480": (3500, 540, 5100, 1320),
    "load_area_all": (400, 1000, 7700, 3150),
    "load_groups_a_1_3": (430, 990, 2400, 3030),
    "load_groups_a_4_6": (2250, 990, 4050, 3030),
    "load_groups_b_1_3": (4150, 990, 5900, 3030),
    "load_groups_b_4_6": (5750, 990, 7700, 3030),
    "load_a1": (450, 1030, 1200, 3040),
    "load_a2": (1040, 1030, 1800, 3040),
    "load_a3": (1630, 1030, 2380, 3040),
    "load_a4": (2220, 1030, 2970, 3040),
    "load_a5": (2810, 1030, 3560, 3040),
    "load_a6": (3400, 1030, 4140, 3040),
    "load_b1": (4170, 1030, 4930, 3040),
    "load_b2": (4760, 1030, 5520, 3040),
    "load_b3": (5350, 1030, 6110, 3040),
    "load_b4": (5940, 1030, 6700, 3040),
    "load_b5": (6530, 1030, 7290, 3040),
    "load_b6": (7120, 1030, 7780, 3040),
    "bottom_control_all": (420, 3000, 7800, 4280),
    "bottom_control_a": (450, 3000, 4050, 4280),
    "bottom_control_b": (5150, 3000, 7800, 4280),
    "bottom_a_dc": (650, 3420, 2600, 4050),
    "bottom_a_120": (2350, 3450, 4100, 4100),
    "bottom_b_dc": (5200, 3420, 6500, 4050),
    "bottom_b_120": (6200, 3450, 7800, 4100),
    "notes_legend": (7850, 520, 9050, 1950),
    "revision_title": (7850, 1980, 9050, 5350),
}


def save_crop(img: Image.Image, name: str, box: tuple[int, int, int, int], suffix: str) -> None:
    crop = img.crop(box)
    crop.save(OUT / f"{name}_{suffix}.png")
    if name != "overview":
        w, h = crop.size
        crop.resize((w * 2, h * 2), Image.Resampling.LANCZOS).save(OUT / f"{name}_{suffix}_2x.png")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for suffix, path in SOURCES.items():
        img = Image.open(path)
        if suffix == "mask":
            img = ImageOps.invert(img.convert("L")).convert("RGB")
            suffix = "mask_inv"
        for name, box in CROPS.items():
            save_crop(img, name, box, suffix)


if __name__ == "__main__":
    main()
