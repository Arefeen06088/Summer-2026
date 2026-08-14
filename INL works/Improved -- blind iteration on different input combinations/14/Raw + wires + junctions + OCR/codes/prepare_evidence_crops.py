from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "codes" / "evidence_crops"

IMAGES = {
    "raw": ROOT / "raw -- synthetic_npp_electrical_schematic_even_bus_spacing (1).png",
    "labels": ROOT / "component_labels_banners_overlay.png",
    "wires": ROOT / "wire_nodes_overlay.png",
    "mask_overlay": ROOT / "wires_mask_overlay.png",
}

CROPS = {
    "top_sources_and_4kv": (520, 190, 5050, 1010),
    "left_4kv_bus_a": (650, 250, 3050, 1060),
    "right_4kv_bus_b": (3150, 250, 5000, 1060),
    "upper_loads_a": (1400, 760, 2700, 1540),
    "upper_loads_b": (4200, 760, 4950, 1540),
    "middle_480_tie": (900, 1620, 5350, 2050),
    "middle_loads_a": (1050, 1800, 2800, 2670),
    "middle_loads_b": (3750, 1800, 5300, 2670),
    "lower_panels": (550, 2660, 5000, 3160),
    "lower_dc_and_tie": (900, 2950, 4850, 3720),
    "full_left_half": (560, 190, 3050, 3720),
    "full_right_half": (3150, 190, 5350, 3720),
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
