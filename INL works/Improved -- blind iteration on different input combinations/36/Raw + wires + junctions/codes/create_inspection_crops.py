from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\36\Raw + wires + junctions")
RESULTS = ROOT / "results" / "inspection_crops"
FALLBACK_RESULTS = Path(r"C:\Asif_all_python_projects\INL\INL\doc36_work\inspection_crops")

SOURCES = {
    "raw": ROOT / "raw -- synthetic_npp_electrical_schematic_v2.png",
    "wires": ROOT / "wires_mask_overlay.png",
    "nodes": ROOT / "wire_nodes_overlay.png",
    "mask": ROOT / "wires_mask.png",
}

CROPS = {
    "doc36_full": (0, 0, 4800, 3400),
    "doc36_top_full": (0, 0, 4800, 1250),
    "doc36_mid_full": (0, 1000, 4800, 2350),
    "doc36_bottom_full": (0, 2150, 4800, 3400),
    "doc36_left_full": (0, 0, 1750, 3400),
    "doc36_center_full": (1500, 0, 3350, 3400),
    "doc36_right_full": (3100, 0, 4800, 3400),
    "doc36_top_left": (0, 0, 1750, 1250),
    "doc36_top_center": (1500, 0, 3350, 1250),
    "doc36_top_right": (3100, 0, 4800, 1250),
    "doc36_mid_left": (0, 1000, 1750, 2350),
    "doc36_mid_center": (1500, 1000, 3350, 2350),
    "doc36_mid_right": (3100, 1000, 4800, 2350),
    "doc36_bottom_left": (0, 2150, 1750, 3400),
    "doc36_bottom_center": (1500, 2150, 3350, 3400),
    "doc36_bottom_right": (3100, 2150, 4800, 3400),
    "doc36_control_center": (1550, 1350, 3350, 2600),
    "doc36_right_notes": (3500, 650, 4800, 2800),
    "doc36_title": (3350, 2750, 4800, 3400),
    "doc36_lower_bus_center": (1200, 1800, 3800, 3400),
    "doc36_rps_ties_detail": (2050, 700, 2950, 1950),
    "doc36_esf_control_detail": (1950, 1900, 3000, 2950),
    "doc36_train_a_dc_detail": (350, 2150, 2450, 3400),
    "doc36_train_b_dc_detail": (2450, 2150, 4650, 3400),
}


def output_dir() -> Path:
    try:
        RESULTS.mkdir(parents=True, exist_ok=True)
        probe = RESULTS / ".write_probe_doc36"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
        return RESULTS
    except OSError:
        FALLBACK_RESULTS.mkdir(parents=True, exist_ok=True)
        return FALLBACK_RESULTS


def save_overview(image: Image.Image, path: Path) -> None:
    im = image.copy()
    im.thumbnail((2400, 1800), Image.Resampling.LANCZOS)
    im.save(path)


def main() -> None:
    out = output_dir()
    for source_name, source_path in SOURCES.items():
        with Image.open(source_path) as image:
            image = image.convert("RGB")
            save_overview(image, out / f"{source_name}_overview_2400.png")
            for crop_name, box in CROPS.items():
                crop = image.crop(box)
                crop.save(out / f"{source_name}_{crop_name}.png")
                if source_name == "raw":
                    gray = ImageOps.grayscale(crop)
                    gray = ImageOps.autocontrast(gray)
                    gray.save(out / f"raw_gray_{crop_name}.png")
    print(f"inspection crops written to {out}")


if __name__ == "__main__":
    main()
