from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\6\Raw")
RAW = BASE / "raw -- synthetic_npp_electrical_schematic_variant3_redo_clean_v7.png"
OUT = BASE / "results" / "crops"


def crop(name: str, box: tuple[int, int, int, int]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    image = Image.open(RAW)
    image.crop(box).save(OUT / f"{name}.png")


def main() -> None:
    crops = {
        "full_top_generation_switchyard": (120, 80, 7050, 980),
        "medium_voltage_safety_buses": (120, 720, 7150, 1800),
        "left_480_loads": (120, 1600, 2650, 3150),
        "center_480_loads_tie": (2450, 1500, 5850, 2700),
        "right_480_loads": (4800, 1500, 6900, 3150),
        "dc_ups_bottom": (1950, 2900, 6500, 4100),
        "right_control_bay": (6400, 560, 8880, 2600),
        "right_control_lower": (6400, 2300, 8880, 3450),
        "sixkv_left_sources_detail": (120, 860, 3300, 1950),
        "sixkv_right_sources_detail": (3000, 760, 6200, 1950),
        "generator_branch_detail": (150, 350, 3150, 1150),
        "switchyard_right_detail": (3000, 350, 7050, 1150),
        "instrument_ct_bus_detail": (2300, 700, 5850, 1550),
        "left_loads_lower_detail": (900, 2200, 3050, 3650),
        "right_loads_lower_detail": (5100, 2200, 7000, 3650),
        "control_bay_left_interfaces": (5600, 650, 7600, 3100),
        "notes_legend_title": (120, 140, 8880, 4300),
    }
    for name, box in crops.items():
        crop(name, box)


if __name__ == "__main__":
    main()
