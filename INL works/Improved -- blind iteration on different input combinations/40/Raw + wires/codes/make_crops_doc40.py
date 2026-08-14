from pathlib import Path

from PIL import Image, ImageOps


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\40\Raw + wires")
OUT = BASE / "codes" / "crops"

RAW = BASE / "raw -- synthetic_nuclear_distribution_schematic.png"
OVERLAY = BASE / "wires_mask_overlay.png"
MASK = BASE / "wires_mask.png"


REGIONS = {
    "overview": (0, 0, 6600, 4700),
    "drawing_area": (250, 250, 5300, 3650),
    "left_train_full": (320, 480, 2740, 3650),
    "right_train_full": (3000, 480, 5320, 3650),
    "top_sources_tie": (470, 500, 5200, 1500),
    "left_top_source_switchgear": (480, 500, 2850, 1800),
    "right_top_source_switchgear": (3000, 500, 5250, 1800),
    "tie_breaker_center": (2500, 1050, 3300, 1450),
    "left_mcc_loads": (450, 1750, 2750, 2820),
    "right_mcc_loads": (3000, 1750, 5320, 2820),
    "left_dc_rps": (450, 2700, 2750, 3650),
    "right_dc_rps": (3000, 2700, 5320, 3650),
    "center_dc_rectifiers": (2300, 2600, 3800, 3600),
    "left_rps_detail": (650, 2850, 2350, 3600),
    "right_rps_detail": (3800, 2850, 5350, 3600),
    "left_rps_terminals_detail": (1400, 2400, 3000, 3600),
    "right_rps_terminals_detail": (3100, 2400, 4800, 3600),
    "left_trip_loca_detail": (350, 1950, 1700, 3600),
    "right_trip_loca_detail": (3800, 1950, 5400, 3600),
    "notes_legend": (5350, 650, 6400, 2880),
    "cable_index_title": (5350, 2900, 6450, 4500),
}


def save_crop(img: Image.Image, name: str, bbox: tuple[int, int, int, int], suffix: str, scale: int = 1) -> None:
    crop = img.crop(bbox)
    if scale != 1:
        crop = crop.resize((crop.width * scale, crop.height * scale), Image.Resampling.LANCZOS)
    crop.save(OUT / f"{name}_{suffix}{'_2x' if scale != 1 else ''}.png")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    raw = Image.open(RAW).convert("RGB")
    overlay = Image.open(OVERLAY).convert("RGB")
    mask = Image.open(MASK).convert("L")
    mask_inv = ImageOps.invert(mask)

    for name, bbox in REGIONS.items():
        save_crop(raw, name, bbox, "raw")
        save_crop(overlay, name, bbox, "overlay")
        save_crop(mask_inv, name, bbox, "mask_inv")
        if name != "overview":
            save_crop(raw, name, bbox, "raw", scale=2)
            save_crop(overlay, name, bbox, "overlay", scale=2)
            save_crop(mask_inv, name, bbox, "mask_inv", scale=2)

    print(f"Wrote crops to {OUT}")


if __name__ == "__main__":
    main()
