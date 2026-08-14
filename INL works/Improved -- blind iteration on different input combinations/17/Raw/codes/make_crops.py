from pathlib import Path

from PIL import Image


RAW_DIR = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\17\Raw"
)
RAW_IMAGE = RAW_DIR / "raw -- synthetic_npp_aux_power_schematic_overlap_fixed.png"
OUT_DIR = RAW_DIR / "codes" / "crops"


CROPS = {
    "full_drawing_area": (220, 180, 4100, 3360),
    "top_overview": (220, 180, 4100, 960),
    "top_train_a": (220, 180, 2100, 960),
    "top_train_b": (2120, 180, 4100, 960),
    "middle_mcc_overview": (220, 820, 4100, 1800),
    "middle_train_a_loads": (220, 820, 2100, 1800),
    "middle_train_b_loads": (2120, 820, 4100, 1800),
    "lower_overview": (220, 1750, 4100, 3340),
    "lower_train_a_dc_ups": (220, 1750, 2100, 3340),
    "lower_train_b_dc_ups": (2120, 1750, 4100, 3340),
    "central_ties": (1900, 220, 2350, 3340),
    "lower_annunciator_shared": (1500, 2650, 2600, 3340),
    "branch_tails_train_a": (950, 1500, 1800, 3320),
    "branch_tails_train_b": (2550, 1500, 3450, 3320),
    "lower_a_controls": (1300, 2700, 2450, 3520),
    "lower_b_controls": (2450, 2700, 3850, 3520),
    "lower_dc_tie": (1800, 2000, 2400, 3300),
    "notes": (4240, 220, 5400, 1180),
    "reference_drawings": (4240, 1220, 5400, 1800),
    "legend": (4240, 1870, 5400, 2280),
    "revision_block": (4240, 2380, 5400, 2680),
    "title_block": (4240, 2800, 5400, 3360),
}


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    image = Image.open(RAW_IMAGE)
    for name, box in CROPS.items():
        image.crop(box).save(OUT_DIR / f"{name}.png")
    print(f"Wrote {len(CROPS)} crops to {OUT_DIR}")


if __name__ == "__main__":
    main()
