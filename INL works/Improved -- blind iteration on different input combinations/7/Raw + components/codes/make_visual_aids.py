from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\7\Raw + components")
RESULTS = BASE / "results"
RAW = BASE / "raw -- synthetic_npp_electrical_schematic_clean (1).png"
OVERLAY = BASE / "detected_components_and_logical_overlay.png"


CROPS = {
    "01_top_sources_and_13kv_buses": (250, 230, 5350, 1180),
    "02_mv_bus_a_sources": (250, 650, 3100, 1100),
    "03_mv_bus_b_sources": (3000, 650, 2650, 1100),
    "04_train_a_480_loads": (320, 1550, 2550, 1600),
    "05_train_b_480_loads": (3050, 1550, 2600, 1600),
    "06_train_a_dc_control": (320, 3000, 2350, 1550),
    "07_train_b_dc_control": (3050, 3000, 2400, 1550),
    "08_bottom_cross_train_controls": (1600, 3650, 3550, 850),
    "09_left_load_label_zoom": (420, 2100, 2250, 900),
    "10_right_load_label_zoom": (3150, 2100, 2250, 900),
    "11_left_dc_label_zoom": (450, 3250, 2200, 1000),
    "12_right_dc_label_zoom": (3200, 3250, 2200, 1000),
    "13_top_source_label_zoom": (650, 330, 1800, 850),
    "14_13kv_tie_zoom": (2300, 550, 1700, 850),
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
