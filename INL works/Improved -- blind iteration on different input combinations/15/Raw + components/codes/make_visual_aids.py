from __future__ import annotations

from pathlib import Path

from PIL import Image


DOC_ROOT = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\15\Raw + components"
)
RAW = DOC_ROOT / "raw -- improved_synthetic_nuclear_electrical_schematic.png"
OVERLAY = DOC_ROOT / "detected_components_and_logical_overlay.png"
OUT = DOC_ROOT / "results"


BOXES = {
    "01_full_schematic": (180, 70, 6400, 3720),
    "02_offsite_sources_top": (430, 60, 6100, 640),
    "03_div_1a_full": (330, 430, 1900, 3660),
    "04_div_1b_full": (1800, 430, 3350, 3660),
    "05_div_2a_full": (3250, 430, 4900, 3660),
    "06_div_2b_full": (4750, 430, 6350, 3660),
    "07_div_1a_safety_4160_480": (430, 430, 1870, 1540),
    "08_div_1b_safety_4160_480": (1810, 430, 3310, 1540),
    "09_div_2a_safety_4160_480": (3300, 430, 4820, 1540),
    "10_div_2b_safety_4160_480": (4800, 430, 6310, 1540),
    "11_div_1a_mcc_loads": (420, 1510, 1850, 2860),
    "12_div_1b_mcc_loads": (1840, 1510, 3300, 2860),
    "13_div_2a_mcc_loads": (3330, 1510, 4800, 2860),
    "14_div_2b_mcc_loads": (4820, 1510, 6310, 2860),
    "15_div_1a_dc_ups": (430, 2780, 1870, 3650),
    "16_div_1b_dc_ups": (1840, 2780, 3310, 3650),
    "17_div_2a_dc_ups": (3330, 2780, 4820, 3650),
    "18_div_2b_dc_ups": (4820, 2780, 6310, 3650),
    "19_tie_1a_1b": (1500, 520, 2120, 1430),
    "20_tie_2a_2b": (4470, 520, 5120, 1430),
    "21_right_notes_legend": (6250, 430, 7420, 1620),
    "22_load_schedule": (6250, 1640, 7420, 2540),
    "23_reference_qc": (6250, 2620, 7420, 3500),
    "24_title_block": (5200, 4300, 7400, 4870),
    "25_revision_block": (110, 4300, 1700, 4870),
}


UPS_DETAIL_BOXES = {
    "26_div_1a_dc_detail": (450, 3250, 1750, 3570),
    "27_div_1b_dc_detail": (1870, 3250, 3200, 3570),
    "28_div_2a_dc_detail": (3380, 3250, 4700, 3570),
    "29_div_2b_dc_detail": (4880, 3250, 6200, 3570),
}


def save(source: Path, prefix: str) -> None:
    with Image.open(source) as img:
        for name, box in {**BOXES, **UPS_DETAIL_BOXES}.items():
            crop = img.crop(box)
            crop.save(OUT / f"{prefix}_{name}.png")
            if name.startswith(("02_", "07_", "08_", "09_", "10_", "15_", "16_", "17_", "18_", "19_", "20_", "26_", "27_", "28_", "29_")):
                w, h = crop.size
                crop.resize((w * 2, h * 2), Image.Resampling.LANCZOS).save(
                    OUT / f"{prefix}_{name}_2x.png"
                )

        width, height = img.size
        for row in range(2):
            for col in range(4):
                left = round(col * width / 4)
                top = round(row * 3720 / 2)
                right = round((col + 1) * width / 4)
                bottom = round((row + 1) * 3720 / 2)
                img.crop((left, top, right, bottom)).save(
                    OUT / f"{prefix}_grid_r{row + 1}_c{col + 1}.png"
                )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    save(RAW, "raw")
    save(OVERLAY, "overlay")
    print(f"wrote Doc15 Raw + components visual aids to {OUT}")


if __name__ == "__main__":
    main()
