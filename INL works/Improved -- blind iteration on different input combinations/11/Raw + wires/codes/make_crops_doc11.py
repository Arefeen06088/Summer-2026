from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageOps


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\11\Raw + wires")
CROPS = BASE / "codes" / "crops_doc11"

RAW = BASE / "raw -- synthetic_npp_electrical_schematic_relocated_names.png"
OVERLAY = BASE / "wires_mask_overlay.png"
MASK = BASE / "wires_mask.png"


CROPS_DEF = {
    "overview": (0, 0, 7200, 4800),
    "drawing_area": (250, 150, 5920, 4550),
    "top_sources_buses": (520, 230, 5700, 1140),
    "train_a_full": (460, 520, 1800, 3520),
    "train_b_full": (1770, 520, 3100, 3520),
    "train_c_full": (3060, 520, 4400, 3520),
    "train_d_full": (4360, 520, 5700, 3520),
    "train_a_loads": (480, 1780, 1780, 3270),
    "train_b_loads": (1800, 1780, 3080, 3270),
    "train_c_loads": (3090, 1780, 4380, 3270),
    "train_d_loads": (4390, 1780, 5680, 3270),
    "bottom_dc_full": (500, 3180, 5350, 4210),
    "bottom_dc_left": (520, 3280, 2550, 4170),
    "bottom_dc_center": (2200, 3280, 4050, 4170),
    "bottom_dc_right": (3550, 3280, 5350, 4170),
    "ats_sps_center": (2100, 2920, 3950, 3810),
    "rps_sps_interlocks": (2360, 3500, 4100, 4050),
    "notes_legend": (5950, 420, 7120, 2220),
    "title_block": (5850, 3520, 7160, 4560),
}


def save_crop(src: Image.Image, stem: str, box: tuple[int, int, int, int], suffix: str, scale: int = 2) -> None:
    crop = src.crop(box)
    out = CROPS / f"{stem}_{suffix}.png"
    crop.save(out)
    if stem != "overview":
        resized = crop.resize((crop.width * scale, crop.height * scale), Image.Resampling.LANCZOS)
        resized.save(CROPS / f"{stem}_{suffix}_{scale}x.png")


def main() -> None:
    CROPS.mkdir(parents=True, exist_ok=True)
    raw = Image.open(RAW).convert("RGB")
    overlay = Image.open(OVERLAY).convert("RGB")
    mask = Image.open(MASK).convert("L")
    mask_inv = ImageOps.invert(mask)
    for stem, box in CROPS_DEF.items():
        save_crop(raw, stem, box, "raw")
        save_crop(overlay, stem, box, "overlay")
        save_crop(mask_inv, stem, box, "mask_inv")


if __name__ == "__main__":
    main()
