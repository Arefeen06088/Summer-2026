from pathlib import Path

from PIL import Image, ImageEnhance


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\10\Raw + wires + junctions + OCR")
CODES = BASE / "codes"

SOURCES = {
    "raw": BASE / "raw -- synthetic_nuclear_electrical_schematic_layout_labels_clear.png",
    "labels": BASE / "component_labels_banners_overlay.png",
    "wires": BASE / "wire_nodes_overlay.png",
    "mask_overlay": BASE / "wires_mask_overlay.png",
}

CROPS = {
    "top_sources_345_4160": (80, 80, 2460, 650),
    "train_a_4160_switchgear": (110, 430, 1180, 1280),
    "train_b_4160_switchgear": (1280, 430, 2360, 1280),
    "train_a_480_mcc_loads": (410, 1180, 1220, 1780),
    "train_b_480_mcc_loads": (1580, 1180, 2400, 1780),
    "train_a_fuse_lc_detail": (430, 1160, 1180, 1535),
    "train_b_fuse_lc_detail": (1600, 1160, 2360, 1535),
    "train_a_dc_ups_ground": (120, 1720, 1185, 2095),
    "train_b_dc_ups_ground": (1290, 1720, 2380, 2095),
    "left_control_panels": (100, 900, 610, 1505),
    "right_control_panels": (1290, 900, 1785, 1505),
    "mcr_annunciator_control_bay": (2360, 430, 2720, 1035),
    "legend_title_notes": (2640, 600, 3245, 1935),
}


def save_crop(img_path: Path, prefix: str) -> None:
    with Image.open(img_path) as im:
        if im.mode not in ("RGB", "RGBA", "L"):
            im = im.convert("RGB")
        for name, box in CROPS.items():
            im.crop(box).save(CODES / f"crop_{prefix}_{name}.png")


def save_contrast_crop(img_path: Path, prefix: str, crop_name: str) -> None:
    with Image.open(img_path).convert("RGB") as im:
        crop = im.crop(CROPS[crop_name])
        crop = ImageEnhance.Contrast(crop).enhance(1.85)
        crop = ImageEnhance.Sharpness(crop).enhance(1.55)
        crop.save(CODES / f"contrast_crop_{prefix}_{crop_name}.png")


def main() -> None:
    CODES.mkdir(exist_ok=True)
    for prefix, img_path in SOURCES.items():
        save_crop(img_path, prefix)
    for crop_name in ("top_sources_345_4160", "train_a_4160_switchgear", "train_b_4160_switchgear",
                      "train_a_480_mcc_loads", "train_b_480_mcc_loads",
                      "train_a_dc_ups_ground", "train_b_dc_ups_ground",
                      "mcr_annunciator_control_bay"):
        save_contrast_crop(SOURCES["raw"], "raw", crop_name)


if __name__ == "__main__":
    main()
