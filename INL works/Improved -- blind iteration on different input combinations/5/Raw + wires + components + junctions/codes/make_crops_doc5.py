from pathlib import Path

from PIL import Image


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\5\Raw + wires + components + junctions"
)
RESULTS = BASE / "results"

SOURCES = {
    "raw": BASE / "raw -- synthetic_npp_electrical_schematic_final_cleaned_v4.png",
    "detected": BASE / "detected_components_and_logical_overlay.png",
    "wire_nodes": BASE / "wire_nodes_overlay.png",
    "wire_mask_overlay": BASE / "wires_mask_overlay.png",
}

CROPS = {
    "top_full": (80, 30, 6320, 900),
    "top_sources_buses": (120, 30, 5200, 850),
    "top_left_source": (80, 40, 1200, 520),
    "top_center_source": (2500, 40, 3800, 520),
    "top_right_source": (4450, 40, 6320, 520),
    "legend_notes": (5140, 210, 6220, 760),
    "left_division_a": (80, 750, 1320, 2850),
    "mid_left_division_b": (1300, 750, 2630, 2850),
    "mid_right_division_c": (2550, 760, 3860, 2850),
    "right_division_d": (3780, 760, 5060, 2850),
    "protection_control_bay": (5000, 740, 6320, 3550),
    "dc_vital_a": (430, 2700, 1740, 3660),
    "dc_vital_b": (3650, 2700, 4920, 3660),
    "bottom_ups_a": (470, 3380, 2070, 3720),
    "bottom_ups_b": (3650, 3370, 4850, 3720),
    "battery_bus_tie": (1500, 3390, 3300, 3720),
    "bottom_dc_relay_chain": (1500, 3330, 4250, 3720),
    "station_ground_title": (160, 3600, 6260, 4160),
    "center_bus_ties": (1080, 1080, 4200, 1420),
    "left_load_center_detail": (520, 1540, 1280, 2260),
    "right_control_detail": (5230, 880, 6160, 2350),
}


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    for source_name, source_path in SOURCES.items():
        with Image.open(source_path) as img:
            for crop_name, box in CROPS.items():
                crop = img.crop(box)
                crop.save(RESULTS / f"{source_name}__{crop_name}.png")
    print(f"Wrote crops to {RESULTS}")


if __name__ == "__main__":
    main()
