from __future__ import annotations

from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\10\Raw")
RAW = BASE / "raw -- synthetic_nuclear_electrical_schematic_layout_labels_clear.png"
OUT = BASE / "results" / "crops"


CROPS = {
    "top_sources_buses": (90, 100, 2600, 620),
    "division_a_full": (100, 360, 1320, 2020),
    "division_b_full": (1320, 360, 2590, 2020),
    "division_a_4160_switchgear": (360, 430, 1160, 1220),
    "division_b_4160_switchgear": (1540, 430, 2320, 1220),
    "division_a_load_centers": (460, 1100, 1220, 1730),
    "division_b_load_centers": (1660, 1100, 2430, 1730),
    "division_a_dc_ups": (230, 1750, 1190, 2050),
    "division_b_dc_ups": (1390, 1750, 2340, 2050),
    "division_a_protection_control": (150, 560, 590, 1560),
    "division_b_protection_control": (1320, 560, 1770, 1560),
    "division_a_fuse_breaker_detail": (430, 1110, 710, 1480),
    "division_b_fuse_breaker_detail": (1605, 1110, 1885, 1480),
    "mcr_annunciator_control_bay": (2380, 360, 2690, 1030),
    "right_notes_legend_title": (2680, 70, 3230, 2100),
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    image = Image.open(RAW)
    for name, box in CROPS.items():
        image.crop(box).save(OUT / f"{name}.png")
    print(f"wrote {len(CROPS)} crops to {OUT}")


if __name__ == "__main__":
    main()
