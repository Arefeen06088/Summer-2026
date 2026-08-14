from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\5\Raw")
RAW = BASE / "raw -- synthetic_npp_electrical_schematic_final_cleaned_v4.png"
OUT = BASE / "results" / "crops"


CROPS = {
    "top_sources_bus": (150, 60, 5250, 900),
    "safety_division_a": (80, 800, 1450, 3120),
    "safety_division_b": (1350, 800, 2750, 3120),
    "safety_division_c": (2700, 800, 4050, 3120),
    "safety_division_d": (3950, 800, 5150, 3120),
    "protection_control_bay": (5000, 720, 6320, 3150),
    "bottom_dc_ups_a": (980, 2800, 3600, 3860),
    "bottom_dc_ups_b": (3400, 2800, 5400, 3860),
    "bus_ties_and_service": (2350, 700, 4300, 1450),
    "legend_title": (5150, 220, 6300, 4100),
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    image = Image.open(RAW)
    for name, box in CROPS.items():
        image.crop(box).save(OUT / f"{name}.png")
    print(f"wrote {len(CROPS)} crops to {OUT}")


if __name__ == "__main__":
    main()
