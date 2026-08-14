from pathlib import Path

from PIL import Image, ImageEnhance


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\13\Raw + wires + junctions + OCR")
CODES = BASE / "codes"

SOURCES = {
    "raw": BASE / "raw -- synthetic diagram _.png",
    "labels": BASE / "component_labels_banners_overlay.png",
    "wires": BASE / "wire_nodes_overlay.png",
    "mask_overlay": BASE / "wires_mask_overlay.png",
}

CROPS = {
    "common_source_230kv_sut": (250, 320, 1650, 920),
    "top_a_power": (430, 720, 2600, 1420),
    "top_b_power": (2680, 720, 4860, 1420),
    "train_a_mcc_dc": (430, 1120, 2600, 1960),
    "train_b_mcc_dc": (2680, 1120, 4860, 1960),
    "middle_source_tie_cd": (330, 1850, 4650, 2380),
    "bottom_c_power": (430, 2020, 2600, 2720),
    "bottom_d_power": (2680, 2020, 4860, 2720),
    "train_c_mcc_dc": (430, 2420, 2600, 3260),
    "train_d_mcc_dc": (2680, 2420, 4860, 3260),
    "plant_ground_center": (2100, 3000, 3000, 3620),
    "notes_legend_schedule_title": (5000, 240, 6320, 4010),
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
        "common_source_230kv_sut",
        "top_a_power",
        "top_b_power",
        "train_a_mcc_dc",
        "train_b_mcc_dc",
        "middle_source_tie_cd",
        "bottom_c_power",
        "bottom_d_power",
        "train_c_mcc_dc",
        "train_d_mcc_dc",
        "plant_ground_center",
    ):
        save_contrast_crop(SOURCES["raw"], "raw", crop_name)


if __name__ == "__main__":
    main()
