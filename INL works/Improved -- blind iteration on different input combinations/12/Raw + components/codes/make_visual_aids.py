from pathlib import Path

from PIL import Image


ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\12\Raw + components")
RESULTS = ROOT / "results"
RAW = ROOT / "raw -- synthetic_npp_electrical_schematic_rps_rerouted.png"
OVERLAY = ROOT / "detected_components_and_logical_overlay.png"


CROPS = {
    "01_top_sources_and_4160_buses": (120, 80, 3200, 720),
    "02_train_a_full": (130, 120, 1650, 2020),
    "03_train_b_full": (1720, 120, 3150, 2020),
    "04_train_a_mcc_480_loads": (180, 760, 1520, 1780),
    "05_train_b_mcc_480_loads": (1820, 760, 3000, 1780),
    "06_dc_instrument_power": (1030, 1880, 2780, 2310),
    "07_bottom_esf_rps_logic": (700, 2230, 3100, 2870),
    "08_left_rps_logic": (780, 2230, 1900, 2860),
    "09_right_rps_logic": (2050, 2230, 3100, 2860),
    "10_center_ats_120vac_bus": (1450, 2100, 2550, 2630),
    "11_train_a_label_zoom": (160, 560, 1580, 1660),
    "12_train_b_label_zoom": (1780, 560, 3050, 1660),
    "13_bottom_label_zoom": (800, 1980, 3050, 2860),
}


def save_crop(image_path, prefix):
    img = Image.open(image_path).convert("RGB")
    for name, box in CROPS.items():
        crop = img.crop(box)
        out = RESULTS / f"{prefix}_{name}.png"
        crop.save(out)
        if name.endswith("_zoom") or "label_zoom" in name or name in {"07_bottom_esf_rps_logic", "10_center_ats_120vac_bus"}:
            enlarged = crop.resize((crop.width * 2, crop.height * 2))
            enlarged.save(RESULTS / f"{prefix}_{name}_2x.png")


def main():
    RESULTS.mkdir(parents=True, exist_ok=True)
    save_crop(RAW, "raw")
    save_crop(OVERLAY, "overlay")
    print(f"Wrote {len(CROPS) * 2} crop sets under {RESULTS}")


if __name__ == "__main__":
    main()
