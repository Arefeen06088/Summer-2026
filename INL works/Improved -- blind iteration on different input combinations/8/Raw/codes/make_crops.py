from __future__ import annotations

from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\8\Raw")
RAW = BASE / "raw -- synthetic_npp_schematic_improved_local_refined_v3.png"
OUT = BASE / "results" / "crops"


CROPS = {
    "full_left_power": (130, 120, 2200, 1650),
    "full_right_power": (1900, 120, 3300, 1650),
    "top_4160_normal_switchgear": (150, 120, 3300, 760),
    "diesel_4kv_switchgear": (130, 660, 3300, 1220),
    "protective_relay_a_detail": (1040, 760, 1680, 1220),
    "protective_relay_b_detail": (2500, 760, 3160, 1220),
    "train_a_480_load_centers": (120, 1060, 1670, 1780),
    "train_b_480_load_centers": (1900, 1060, 3260, 1780),
    "train_a_load_feeders": (180, 1500, 1650, 2250),
    "train_b_load_feeders": (1900, 1500, 3260, 2250),
    "train_a_panel_loads_detail": (900, 1260, 1760, 2150),
    "train_b_panel_loads_detail": (2360, 1260, 3300, 2150),
    "train_a_dc_ups_control": (1340, 1320, 1900, 2300),
    "train_b_dc_ups_control": (2800, 1320, 3370, 2300),
    "center_480_tie_detail": (1350, 1060, 2020, 1480),
    "left_control_relays": (930, 1780, 1710, 2320),
    "right_control_relays": (2340, 1780, 3180, 2320),
    "notes_title_legend": (3350, 150, 4080, 2860),
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    image = Image.open(RAW)
    for name, box in CROPS.items():
        crop = image.crop(box)
        crop.save(OUT / f"{name}.png")
    print(f"wrote {len(CROPS)} crops to {OUT}")


if __name__ == "__main__":
    main()
