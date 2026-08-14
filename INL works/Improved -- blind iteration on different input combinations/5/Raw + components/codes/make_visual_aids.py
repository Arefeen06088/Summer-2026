from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\5\Raw + components")
RESULTS = BASE / "results"
RAW = BASE / "raw -- synthetic_npp_electrical_schematic_final_cleaned_v4.png"
OVERLAY = BASE / "detected_components_and_logical_overlay.png"


CROPS = {
    "01_top_sources_and_13kv_bus": (120, 0, 5150, 850),
    "02_middle_4kv_and_non_safety_buses": (0, 720, 5100, 1600),
    "03_division_a_train": (40, 850, 1350, 2850),
    "04_division_b_train": (1320, 850, 1350, 2850),
    "05_division_c_train": (2600, 850, 1400, 2850),
    "06_division_d_train": (3900, 850, 1400, 2850),
    "07_dc_ups_battery_bottom": (450, 2600, 4200, 1050),
    "08_protection_esf_bay": (5000, 700, 1300, 2500),
    "09_bus_tie_center_detail": (2300, 670, 1900, 800),
    "10_mcc_labels_a_b_zoom": (430, 1720, 2250, 620),
    "11_mcc_labels_c_d_zoom": (2850, 1720, 2250, 620),
    "12_ats_a_load_paths_zoom": (740, 1900, 1500, 1600),
    "13_ats_b_load_paths_zoom": (3150, 1900, 1500, 1600),
}


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    for source_name, path in (("raw", RAW), ("overlay", OVERLAY)):
        image = Image.open(path)
        for crop_name, (x, y, w, h) in CROPS.items():
            crop = image.crop((x, y, x + w, y + h))
            out = RESULTS / f"{source_name}_{crop_name}.png"
            crop.save(out)
            if crop_name.endswith("_zoom"):
                zoomed = crop.resize((crop.width * 2, crop.height * 2))
                zoomed.save(RESULTS / f"{source_name}_{crop_name}_2x.png")
            print(out)


if __name__ == "__main__":
    main()
