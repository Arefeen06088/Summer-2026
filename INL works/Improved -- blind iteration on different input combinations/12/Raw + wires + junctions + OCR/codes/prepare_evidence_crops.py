from pathlib import Path

from PIL import Image, ImageEnhance


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\12\Raw + wires + junctions + OCR")
CODES = BASE / "codes"

SOURCES = {
    "raw": BASE / "raw -- synthetic_npp_electrical_schematic_rps_rerouted.png",
    "labels": BASE / "component_labels_banners_overlay.png",
    "wires": BASE / "wire_nodes_overlay.png",
    "mask_overlay": BASE / "wires_mask_overlay.png",
}

CROPS = {
    "top_power_sources_bus": (190, 150, 3180, 900),
    "left_4160_480_detail": (430, 520, 1480, 1000),
    "right_4160_480_detail": (1770, 520, 2850, 1000),
    "left_mcc1_loads": (220, 850, 1280, 1430),
    "right_mcc1_loads": (1880, 850, 2920, 1430),
    "left_mcc2_loads": (280, 1350, 1220, 1900),
    "right_mcc2_loads": (1940, 1350, 2840, 1900),
    "dc_inverter_center": (1020, 1800, 2650, 2360),
    "bottom_rps_left": (760, 2140, 1780, 2700),
    "bottom_rps_center": (1320, 2100, 2350, 2720),
    "bottom_rps_right": (2220, 2140, 3100, 2700),
    "bottom_rps_full": (760, 2040, 3100, 2780),
    "notes_legend_title": (3230, 210, 4100, 2860),
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
        "top_power_sources_bus",
        "left_4160_480_detail",
        "right_4160_480_detail",
        "left_mcc1_loads",
        "right_mcc1_loads",
        "left_mcc2_loads",
        "right_mcc2_loads",
        "dc_inverter_center",
        "bottom_rps_full",
        "bottom_rps_left",
        "bottom_rps_right",
    ):
        save_contrast_crop(SOURCES["raw"], "raw", crop_name)


if __name__ == "__main__":
    main()
