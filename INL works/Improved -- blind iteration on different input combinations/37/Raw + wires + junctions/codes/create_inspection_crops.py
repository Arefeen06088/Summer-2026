from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\37\Raw + wires + junctions")
RESULTS = ROOT / "results" / "inspection_crops"
FALLBACK_RESULTS = Path(r"C:\Asif_all_python_projects\INL\INL\doc37_work\inspection_crops")

SOURCES = {
    "raw": ROOT / "raw -- synthetic_npp_electrical_schematic_v2(1).png",
    "wires": ROOT / "wires_mask_overlay.png",
    "nodes": ROOT / "wire_nodes_overlay.png",
    "mask": ROOT / "wires_mask.png",
}

CROPS = {
    "doc37_full": (0, 0, 5100, 3300),
    "doc37_top_full": (0, 0, 5100, 1150),
    "doc37_mid_full": (0, 950, 5100, 2300),
    "doc37_bottom_full": (0, 2100, 5100, 3300),
    "doc37_left_full": (0, 0, 1900, 3300),
    "doc37_center_full": (1600, 0, 3500, 3300),
    "doc37_right_full": (3200, 0, 5100, 3300),
    "doc37_top_left": (0, 0, 1900, 1200),
    "doc37_top_center": (1600, 0, 3500, 1200),
    "doc37_top_right": (3200, 0, 5100, 1200),
    "doc37_mid_left": (0, 950, 1900, 2300),
    "doc37_mid_center": (1600, 950, 3500, 2300),
    "doc37_mid_right": (3200, 950, 5100, 2300),
    "doc37_bottom_left": (0, 2100, 1900, 3300),
    "doc37_bottom_center": (1600, 2100, 3500, 3300),
    "doc37_bottom_right": (3200, 2100, 5100, 3300),
    "doc37_control_center": (1750, 1200, 3450, 2550),
    "doc37_rps_detail": (2150, 550, 3150, 1700),
    "doc37_lower_bus_center": (1050, 1750, 4150, 3300),
    "doc37_train_a_dc_detail": (200, 2050, 2600, 3300),
    "doc37_train_b_dc_detail": (2500, 2050, 4900, 3300),
    "doc37_title": (3350, 2650, 5100, 3300),
}


def output_dir() -> Path:
    try:
        RESULTS.mkdir(parents=True, exist_ok=True)
        probe = RESULTS / ".write_probe_doc37"
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
