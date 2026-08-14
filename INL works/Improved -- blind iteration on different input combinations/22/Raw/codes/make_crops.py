from __future__ import annotations

from pathlib import Path

from PIL import Image


RAW_DIR = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\22\Raw"
)
RAW_IMAGE = RAW_DIR / "raw -- synthetic_npp_electrical_schematic_clean.png"
CROP_DIR = RAW_DIR / "codes" / "crops"


def main() -> None:
    CROP_DIR.mkdir(parents=True, exist_ok=True)
    image = Image.open(RAW_IMAGE)
    width, height = image.size

    crops = {
        "full_drawing_area": (0, 0, width, height),
        "top_overview": (0, 0, width, 1800),
        "top_left_sources": (0, 0, 2500, 1800),
        "top_center_buses": (2100, 0, 5000, 1900),
        "top_right_sources": (4600, 0, width, 1900),
        "edg_right_branches_zoom": (4300, 650, 6400, 1600),
        "edg_bus_side_breakers_zoom": (3450, 650, 5050, 1550),
        "middle_overview": (0, 1450, width, 3400),
        "middle_left_feeders": (0, 1350, 2650, 3600),
        "middle_center_feeders": (2300, 1350, 5050, 3600),
        "middle_right_feeders": (4650, 1350, width, 3600),
        "lower_overview": (0, 3150, width, height),
        "lower_left_control": (0, 3000, 2700, height),
        "lower_center_control": (2300, 3000, 5100, height),
        "lower_right_control": (4700, 3000, width, height),
        "control_ladder_upper": (2550, 2750, 5550, 3950),
        "control_ladder_lower": (2550, 3600, 5550, 5050),
        "control_top_aux_zoom": (2750, 2700, 4700, 3300),
        "control_trunk_bottom_zoom": (2750, 3550, 4300, 4800),
        "dc_power_supplies": (1250, 3000, 4100, 5050),
        "inverter_bus_intersections_zoom": (2750, 2850, 4600, 4550),
        "inv120c_output_zoom": (1500, 3700, 4100, 4550),
        "train_a_mcc_detail": (1100, 1550, 3800, 3450),
        "train_b_mcc_detail": (3000, 1550, 6200, 3450),
        "top_switchgear_full": (450, 200, 6150, 1500),
        "train_a_detail": (300, 1500, 1900, 3600),
        "train_b_detail": (1800, 1500, 3400, 3600),
        "train_c_detail": (3300, 1500, 4900, 3600),
        "train_d_detail": (4800, 1500, 6350, 3600),
        "dc_ups_full": (500, 3500, 5850, 4950),
        "dc_ups_left": (500, 3500, 3000, 4950),
        "dc_ups_right": (2900, 3500, 5850, 4950),
        "dc_charger_b_feed_zoom": (2800, 3150, 3900, 4300),
        "dc_charger_b_source_trace": (2600, 1800, 3900, 3900),
        "pt_meter_zoom": (4200, 3350, 5700, 4300),
        "left_full_height": (0, 0, 2600, height),
        "center_full_height": (2300, 0, 5000, height),
        "right_full_height": (4600, 0, width, height),
    }

    for name, box in crops.items():
        image.crop(box).save(CROP_DIR / f"{name}.png")

    print(f"wrote {len(crops)} crops to {CROP_DIR}")


if __name__ == "__main__":
    main()
