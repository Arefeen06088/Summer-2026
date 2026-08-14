from pathlib import Path
from PIL import Image


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\14\Raw + components"
)
RESULTS = BASE / "results"
RAW = BASE / "raw -- synthetic_npp_electrical_schematic_even_bus_spacing (1).png"
OVERLAY = BASE / "detected_components_and_logical_overlay.png"


CROPS = {
    "01_left_schematic_full": (360, 230, 2700, 3600),
    "02_right_schematic_full": (3000, 230, 2500, 3600),
    "03_train_a_4160_top": (520, 270, 2320, 1160),
    "04_train_b_4160_top": (3080, 270, 2320, 1160),
    "05_train_a_480_mcc": (520, 1500, 2320, 1300),
    "06_train_b_480_mcc": (3080, 1500, 2320, 1300),
    "07_train_a_125vdc_ups": (520, 2620, 2450, 1180),
    "08_train_b_125vdc_ups": (3080, 2620, 2350, 1180),
    "09_center_ties_interlocks": (2700, 620, 620, 3100),
    "10_train_a_4160_feed_zoom": (660, 270, 2000, 850),
    "11_train_b_4160_feed_zoom": (3220, 270, 1980, 850),
    "12_train_a_mcc_feed_zoom": (800, 1660, 1900, 1140),
    "13_train_b_mcc_feed_zoom": (3450, 1660, 1800, 1140),
    "14_bottom_terminal_blocks": (500, 3560, 2500, 430),
    "15_notes_legend": (5420, 260, 900, 1320),
    "16_title_block": (5400, 3140, 900, 720),
}


def save_crop(img, prefix, name, box):
    x, y, w, h = box
    crop = img.crop((x, y, x + w, y + h))
    out = RESULTS / f"{prefix}_{name}.png"
    crop.save(out)
    if w <= 2500 and h <= 1600:
        zoom = crop.resize((w * 2, h * 2), Image.Resampling.LANCZOS)
        zoom.save(RESULTS / f"{prefix}_{name}_2x.png")


def main():
    RESULTS.mkdir(parents=True, exist_ok=True)
    for path, prefix in [(RAW, "raw"), (OVERLAY, "overlay")]:
        with Image.open(path) as img:
            for name, box in CROPS.items():
                save_crop(img, prefix, name, box)
    print(f"wrote {len(CROPS) * 2} base crops plus zooms to {RESULTS}")


if __name__ == "__main__":
    main()
