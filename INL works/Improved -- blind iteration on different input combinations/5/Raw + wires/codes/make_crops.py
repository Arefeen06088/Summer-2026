from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
CROPS = RESULTS / "crops"
RAW = ROOT / "raw -- synthetic_npp_electrical_schematic_final_cleaned_v4.png"
OVERLAY = ROOT / "wires_mask_overlay.png"
MASK = ROOT / "wires_mask.png"


CROPS.mkdir(parents=True, exist_ok=True)

REGIONS = {
    "01_top_left_grid_bus_aux_a": (150, 20, 1850, 850),
    "02_top_center_station_bus_ties": (1800, 20, 4500, 900),
    "03_top_right_grid_bus_aux_b": (4200, 20, 6350, 900),
    "04_division_i_left": (80, 760, 1600, 2700),
    "05_division_ii_mid_left": (1300, 760, 2850, 2700),
    "06_division_iii_mid_right": (2650, 760, 4300, 2700),
    "07_division_iv_right": (3950, 760, 5200, 2700),
    "08_esf_control_right": (5000, 700, 6350, 3050),
    "09_bottom_dc_left": (350, 2600, 3000, 3950),
    "10_bottom_dc_right": (2900, 2600, 5150, 3950),
    "11_ground_title_notes": (2500, 3500, 6350, 4200),
    "12_legend_footer_left": (0, 0, 1800, 4200),
    "13_full_bottom_title": (3600, 3600, 6350, 4200),
}


def save_crops(source: Path, prefix: str) -> None:
    with Image.open(source) as im:
        for name, box in REGIONS.items():
            crop = im.crop(box)
            crop.save(CROPS / f"{prefix}_{name}.png")


def main() -> None:
    save_crops(RAW, "raw")
    save_crops(OVERLAY, "overlay")
    save_crops(MASK, "mask")
    print(f"Wrote {len(REGIONS) * 3} crops to {CROPS}")


if __name__ == "__main__":
    main()
