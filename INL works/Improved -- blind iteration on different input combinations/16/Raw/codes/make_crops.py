from pathlib import Path

from PIL import Image


RAW_DIR = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\16\Raw"
)
RAW_IMAGE = RAW_DIR / "raw -- synthetic_npp_electrical_schematic_revised(1).png"
OUT_DIR = RAW_DIR / "codes" / "crops"


CROPS = {
    "full_drawing_area": (120, 120, 2960, 2580),
    "top_4160v_distribution": (140, 150, 2950, 790),
    "middle_480v_mcc_overview": (140, 760, 2950, 1770),
    "bottom_rps_vital_overview": (140, 1720, 2950, 2580),
    "left_mcc_loads": (140, 950, 1180, 1800),
    "center_mcc_loads": (1160, 950, 2100, 1800),
    "right_mcc_loads": (1980, 950, 2960, 1800),
    "lower_left_rps_esf_a": (140, 1740, 1060, 2520),
    "lower_center_rps_shared": (960, 1740, 2040, 2580),
    "lower_right_rps_esf_b": (1900, 1740, 2960, 2520),
    "top_left_station_feed": (120, 180, 920, 780),
    "middle_480_tie_and_b_incomer": (1500, 740, 2450, 1160),
    "lower_left_rps_edge": (70, 1740, 700, 2500),
    "lower_a_instrument_mg": (1500, 1720, 2350, 2520),
    "lower_a_tb_esf1_mg": (1700, 1660, 2300, 2240),
    "lower_b_instrument_mg": (2300, 1720, 3040, 2460),
    "notes": (3000, 180, 3930, 1260),
    "legend": (3000, 1320, 3930, 1760),
    "title_block": (3000, 2220, 3930, 2620),
}


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    image = Image.open(RAW_IMAGE)
    for name, box in CROPS.items():
        image.crop(box).save(OUT_DIR / f"{name}.png")
    print(f"Wrote {len(CROPS)} crops to {OUT_DIR}")


if __name__ == "__main__":
    main()
