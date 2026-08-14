from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\6\Raw + components")
RESULTS = BASE / "results"
RAW = BASE / "raw -- synthetic_npp_electrical_schematic_variant3_redo_clean_v7.png"
OVERLAY = BASE / "detected_components_and_logical_overlay.png"


CROPS = {
    "01_generator_switchyard": (120, 120, 4600, 720),
    "02_mv_safety_bus_left_center": (120, 650, 4300, 1050),
    "03_mv_safety_bus_center_right": (3300, 650, 3500, 1050),
    "04_480_loads_left": (120, 1550, 2500, 1500),
    "05_480_loads_center": (2450, 1550, 2300, 1500),
    "06_480_loads_right": (4300, 1550, 2200, 1500),
    "07_dc_ups_bottom": (1900, 2850, 4200, 950),
    "08_esf_rps_control_bay": (6650, 650, 2050, 1800),
    "09_right_diesel_and_control_crossing": (5800, 650, 2000, 1050),
    "10_bus_tie_and_non_safety_zoom": (2650, 1020, 2500, 720),
    "11_left_load_label_zoom": (300, 2050, 1850, 900),
    "12_right_load_label_zoom": (3900, 2050, 1900, 900),
    "13_dc_label_zoom": (2000, 3000, 3800, 750),
}


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    for source_name, path in (("raw", RAW), ("overlay", OVERLAY)):
        image = Image.open(path)
        for crop_name, (x, y, w, h) in CROPS.items():
            crop = image.crop((x, y, x + w, y + h))
            out = RESULTS / f"{source_name}_{crop_name}.png"
            crop.save(out)
            if crop_name.endswith("_zoom") or "label_zoom" in crop_name:
                zoomed = crop.resize((crop.width * 2, crop.height * 2))
                zoomed.save(RESULTS / f"{source_name}_{crop_name}_2x.png")
            print(out)


if __name__ == "__main__":
    main()
