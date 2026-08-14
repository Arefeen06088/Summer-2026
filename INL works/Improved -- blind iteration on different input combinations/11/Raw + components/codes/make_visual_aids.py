from __future__ import annotations

from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\11\Raw + components")
RESULTS = BASE / "results"
RAW = BASE / "raw -- synthetic_npp_electrical_schematic_relocated_names.png"
OVERLAY = BASE / "detected_components_and_logical_overlay.png"


CROPS = {
    "01_top_sources_13kv": (520, 150, 5200, 620),
    "02_train_a_full": (480, 620, 1450, 3000),
    "03_train_b_full": (1850, 620, 1450, 3000),
    "04_train_c_full": (3200, 620, 1450, 3000),
    "05_train_d_full": (4550, 620, 1450, 3000),
    "06_bottom_dc_a": (620, 3300, 2350, 820),
    "07_bottom_dc_b": (3320, 3300, 2350, 820),
    "08_cross_train_controls": (2100, 3000, 2600, 850),
    "09_train_a_label_zoom": (520, 780, 1250, 2200),
    "10_train_b_label_zoom": (1880, 780, 1250, 2200),
    "11_train_c_label_zoom": (3250, 780, 1250, 2200),
    "12_train_d_label_zoom": (4600, 780, 1250, 2200),
    "13_dc_a_label_zoom": (680, 3520, 2200, 680),
    "14_dc_b_label_zoom": (3400, 3520, 2200, 680),
}


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    for source_name, path in (("raw", RAW), ("overlay", OVERLAY)):
        image = Image.open(path)
        for crop_name, (x, y, w, h) in CROPS.items():
            crop = image.crop((x, y, x + w, y + h))
            out = RESULTS / f"{source_name}_{crop_name}.png"
            crop.save(out)
            if "zoom" in crop_name or "label" in crop_name:
                crop.resize((crop.width * 2, crop.height * 2)).save(
                    RESULTS / f"{source_name}_{crop_name}_2x.png"
                )
            print(out)


if __name__ == "__main__":
    main()
