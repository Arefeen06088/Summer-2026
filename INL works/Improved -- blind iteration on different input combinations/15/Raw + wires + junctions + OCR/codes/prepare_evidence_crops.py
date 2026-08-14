from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "codes" / "evidence_crops"

IMAGES = {
    "raw": ROOT / "raw -- improved_synthetic_nuclear_electrical_schematic.png",
    "labels": ROOT / "component_labels_banners_overlay.png",
    "wires": ROOT / "wire_nodes_overlay.png",
    "mask_overlay": ROOT / "wires_mask_overlay.png",
}

CROPS = {
    "upper_offsite_sources": (420, 0, 6200, 520),
    "upper_4kv_sources_all": (480, 260, 6300, 980),
    "division_ab_4kv": (450, 500, 3300, 1250),
    "division_cd_4kv": (3300, 500, 6250, 1250),
    "transformers_480_all": (650, 930, 5900, 1450),
    "mcc_buses_all": (350, 1520, 6200, 2030),
    "mcc_loads_a": (420, 1850, 1700, 2860),
    "mcc_loads_b": (1900, 1850, 3180, 2860),
    "mcc_loads_c": (3380, 1850, 4660, 2860),
    "mcc_loads_d": (4860, 1850, 6140, 2860),
    "dc_control_all": (420, 3150, 6140, 3580),
    "dc_control_a": (420, 3180, 1660, 3545),
    "dc_control_b": (1900, 3180, 3140, 3545),
    "dc_control_c": (3380, 3180, 4620, 3545),
    "dc_control_d": (4860, 3180, 6100, 3545),
    "full_division_a": (360, 520, 1780, 3580),
    "full_division_b": (1840, 520, 3260, 3580),
    "full_division_c": (3320, 520, 4740, 3580),
    "full_division_d": (4800, 520, 6220, 3580),
}


def enhance(raw_crop: Image.Image) -> Image.Image:
    gray = ImageOps.grayscale(raw_crop)
    gray = ImageOps.autocontrast(gray)
    return ImageEnhance.Contrast(gray).enhance(1.8)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for image_key, path in IMAGES.items():
        image = Image.open(path)
        for crop_name, box in CROPS.items():
            crop = image.crop(box)
            crop.save(OUT / f"{crop_name}_{image_key}.png")
            if image_key == "raw":
                enhance(crop).save(OUT / f"{crop_name}_raw_contrast.png")

    index_lines = ["crop_name,x0,y0,x1,y1"]
    for crop_name, box in CROPS.items():
        index_lines.append(f"{crop_name},{box[0]},{box[1]},{box[2]},{box[3]}")
    (OUT / "crop_index.csv").write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    print(f"Wrote crops to {OUT}")


if __name__ == "__main__":
    main()
