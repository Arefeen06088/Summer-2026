from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageOps


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\18\Raw + wires")
OUT = BASE / "codes" / "crops_doc18"

SOURCES = {
    "raw": BASE / "raw -- synthetic_nuclear_electrical_schematic_readable.png",
    "overlay": BASE / "wires_mask_overlay.png",
    "mask": BASE / "wires_mask.png",
}

CROPS = {
    "overview": (0, 0, 7000, 4400),
    "drawing_area": (180, 230, 6100, 3650),
    "top_sources_buses": (250, 250, 5600, 1150),
    "top_left_sources": (250, 250, 2100, 1120),
    "top_a_pt_rps_detail": (850, 760, 1600, 1220),
    "top_center_tie": (2000, 350, 3800, 1120),
    "top_right_sources_notes": (3600, 250, 6600, 1120),
    "top_right_uat_bus": (3950, 350, 5600, 1260),
    "top_b_pt_rps_detail": (4300, 760, 5200, 1220),
    "train_a_loads": (340, 1120, 1620, 2160),
    "train_b_loads": (1640, 1120, 2880, 2160),
    "train_c_loads": (3120, 1120, 4380, 2160),
    "train_d_loads": (4400, 1120, 5600, 2160),
    "load_area_all": (300, 1040, 5650, 2260),
    "bottom_control_all": (300, 2500, 5650, 3520),
    "bottom_control_a": (320, 2500, 2940, 3520),
    "bottom_control_b": (3040, 2500, 5660, 3520),
    "bottom_a_left_dc": (470, 2850, 1760, 3380),
    "bottom_a_right_rps": (1730, 2850, 2900, 3330),
    "bottom_b_left_dc": (3180, 2850, 4480, 3380),
    "bottom_b_right_rps": (4460, 2850, 5620, 3330),
    "legend_notes": (5550, 300, 6750, 1040),
    "title_block": (5350, 3650, 6770, 4250),
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
