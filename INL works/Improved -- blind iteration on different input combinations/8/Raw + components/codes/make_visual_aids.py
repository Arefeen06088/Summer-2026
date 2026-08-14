from __future__ import annotations

from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\8\Raw + components")
RESULTS = BASE / "results"
RAW = BASE / "raw -- synthetic_npp_schematic_improved_local_refined_v3.png"
OVERLAY = BASE / "detected_components_and_logical_overlay.png"


CROPS = {
    "01_top_416kv_sources": (150, 150, 3150, 570),
    "02_safety_416kv_buses": (150, 650, 3150, 560),
    "03_480_distribution": (150, 1080, 3150, 460),
    "04_train_a_loads": (160, 1350, 1320, 780),
    "05_train_a_dc_control": (1350, 1280, 760, 920),
    "06_train_b_loads": (2000, 1350, 1320, 780),
    "07_train_b_dc_control": (2780, 1280, 560, 920),
    "08_bottom_interlocks": (850, 1950, 2350, 430),
    "09_left_source_label_zoom": (210, 200, 1200, 650),
    "10_center_source_label_zoom": (1400, 200, 1200, 700),
    "11_right_source_label_zoom": (2200, 200, 1100, 700),
    "12_left_load_label_zoom": (210, 1480, 1250, 740),
    "13_center_dc_label_zoom": (1380, 1370, 820, 870),
    "14_right_load_label_zoom": (2050, 1480, 1220, 740),
    "15_right_dc_label_zoom": (2780, 1370, 560, 870),
    "16_a_pn480_mcc2c_zoom": (1120, 1180, 700, 820),
    "17_b_pn480_mcc2d_zoom": (2480, 1180, 700, 820),
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
