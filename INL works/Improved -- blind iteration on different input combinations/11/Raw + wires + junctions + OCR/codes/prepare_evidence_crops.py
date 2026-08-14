from pathlib import Path

from PIL import Image, ImageEnhance


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\11\Raw + wires + junctions + OCR")
CODES = BASE / "codes"

SOURCES = {
    "raw": BASE / "raw -- synthetic_npp_electrical_schematic_relocated_names.png",
    "labels": BASE / "component_labels_banners_overlay.png",
    "wires": BASE / "wire_nodes_overlay.png",
    "mask_overlay": BASE / "wires_mask_overlay.png",
}

CROPS = {
    "top_sources_13kv": (560, 150, 5850, 950),
    "division_a_full": (480, 560, 1860, 3520),
    "division_b_full": (1800, 560, 3220, 3520),
    "division_c_full": (3150, 560, 4560, 3520),
    "division_d_full": (4500, 560, 5910, 3520),
    "division_a_power_detail": (560, 930, 1770, 2150),
    "division_b_power_detail": (1850, 930, 3110, 2150),
    "division_c_power_detail": (3220, 930, 4450, 2150),
    "division_d_power_detail": (4570, 930, 5800, 2150),
    "division_a_mcc_load_detail": (560, 1900, 1770, 3180),
    "division_b_mcc_load_detail": (1850, 1900, 3110, 3180),
    "division_c_mcc_load_detail": (3220, 1900, 4450, 3180),
    "division_d_mcc_load_detail": (4570, 1900, 5800, 3180),
    "bottom_dc_ups_rps": (650, 3150, 5300, 4240),
    "bottom_dc_ups_rps_wide": (650, 3150, 5900, 4240),
    "bottom_a_dc_ups": (650, 3500, 2700, 4240),
    "bottom_b_dc_ups": (3350, 3500, 5400, 4240),
    "ats_ssps_interlocks": (2050, 3000, 4200, 3900),
    "notes_legend_title": (5920, 360, 7080, 4380),
}


def save_crop(img_path: Path, prefix: str) -> None:
    with Image.open(img_path) as im:
        for name, box in CROPS.items():
            im.crop(box).save(CODES / f"crop_{prefix}_{name}.png")


def save_contrast_crop(img_path: Path, prefix: str, crop_name: str) -> None:
    with Image.open(img_path).convert("RGB") as im:
        crop = im.crop(CROPS[crop_name])
        crop = ImageEnhance.Contrast(crop).enhance(1.9)
        crop = ImageEnhance.Sharpness(crop).enhance(1.55)
        crop.save(CODES / f"contrast_crop_{prefix}_{crop_name}.png")


def main() -> None:
    CODES.mkdir(exist_ok=True)
    for prefix, img_path in SOURCES.items():
        save_crop(img_path, prefix)
    for crop_name in (
        "top_sources_13kv",
        "division_a_power_detail",
        "division_b_power_detail",
        "division_c_power_detail",
        "division_d_power_detail",
        "division_a_mcc_load_detail",
        "division_b_mcc_load_detail",
        "division_c_mcc_load_detail",
        "division_d_mcc_load_detail",
        "bottom_dc_ups_rps",
        "ats_ssps_interlocks",
    ):
        save_contrast_crop(SOURCES["raw"], "raw", crop_name)


if __name__ == "__main__":
    main()
