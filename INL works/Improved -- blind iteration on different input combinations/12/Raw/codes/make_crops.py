from __future__ import annotations

from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\12\Raw")
RAW = BASE / "raw -- synthetic_npp_electrical_schematic_rps_rerouted.png"
OUT = BASE / "results" / "crops"


CROPS: dict[str, tuple[int, int, int, int]] = {
    "full_drawing_area": (120, 80, 4080, 2920),
    "top_sources_and_4160_buses": (180, 130, 3160, 770),
    "train_a_full": (180, 520, 1680, 1930),
    "train_b_full": (1820, 520, 3180, 1930),
    "train_a_upper_power": (200, 150, 1700, 950),
    "train_b_upper_power": (1810, 150, 3190, 950),
    "train_a_mcc_1a": (230, 840, 1290, 1480),
    "train_a_mcc_2a": (230, 1460, 1300, 1960),
    "train_b_mcc_1b": (1840, 840, 2930, 1480),
    "train_b_mcc_2b": (1840, 1460, 2940, 1960),
    "dc_instrument_power": (1040, 1860, 2680, 2330),
    "bottom_control_logic_full": (760, 2260, 3150, 2820),
    "bottom_control_logic_left": (780, 2260, 1830, 2820),
    "bottom_control_logic_center": (1560, 2220, 2420, 2810),
    "bottom_control_logic_right": (2260, 2260, 3180, 2820),
    "right_notes_legend_title": (3220, 220, 4060, 2840),
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    image = Image.open(RAW)
    for name, box in CROPS.items():
        image.crop(box).save(OUT / f"{name}.png")
    print(f"Wrote {len(CROPS)} crops to {OUT}")


if __name__ == "__main__":
    main()
