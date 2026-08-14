from pathlib import Path
from PIL import Image


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\13\Raw + components"
)
RESULTS = BASE / "results"
RAW = BASE / "raw -- synthetic diagram _.png"
OVERLAY = BASE / "detected_components_and_logical_overlay.png"


CROPS = {
    "01_left_schematic_full": (180, 260, 4950, 3340),
    "02_top_sources_and_4160_buses": (240, 340, 4760, 880),
    "03_train_a_full": (420, 760, 2180, 1040),
    "04_train_b_full": (2640, 760, 2240, 1040),
    "05_train_c_full": (420, 1780, 2180, 1280),
    "06_train_d_full": (2640, 1780, 2240, 1280),
    "07_train_a_loads_dc_zoom": (530, 1040, 2040, 750),
    "08_train_b_loads_dc_zoom": (2750, 1040, 2040, 750),
    "09_train_c_loads_dc_zoom": (530, 2100, 2040, 770),
    "10_train_d_loads_dc_zoom": (2750, 2100, 2040, 770),
    "11_startup_switchyard_feed": (300, 380, 1500, 540),
    "12_train_a_source_detail": (430, 720, 1580, 560),
    "13_train_b_source_detail": (2670, 720, 1580, 560),
    "14_train_c_source_detail": (430, 1760, 1580, 650),
    "15_train_d_source_detail": (2670, 1760, 1580, 650),
    "16_common_ground_and_cross_ties": (2200, 1800, 1300, 1900),
    "17_notes_legend_schedule": (5040, 220, 1200, 2780),
}


def save_crop(img, prefix, name, box):
    x, y, w, h = box
    crop = img.crop((x, y, x + w, y + h))
    out = RESULTS / f"{prefix}_{name}.png"
    crop.save(out)
    if w < 2600 and h < 1600:
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
