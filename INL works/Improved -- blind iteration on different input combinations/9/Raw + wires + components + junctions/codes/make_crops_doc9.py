from pathlib import Path

from PIL import Image

BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\9\Raw + wires + components + junctions"
)
RESULTS = BASE / "results"

SOURCES = {
    "raw": BASE / "raw -- synthetic_npp_schematic_expanded_clear_refined_v3_reworked.png",
    "detected": BASE / "detected_components_overlay.png",
    "wire_nodes": BASE / "wire_nodes_overlay.png",
    "wire_mask_overlay": BASE / "wires_mask_overlay.png",
}

CROPS = {
    "top_left_sources": (120, 120, 1580, 850),
    "top_center_sources": (1450, 120, 3050, 900),
    "top_right_sources": (3000, 120, 4300, 900),
    "mid_left_safety": (120, 650, 1650, 1850),
    "mid_center_normal": (1450, 650, 3050, 1950),
    "mid_right_safety": (2850, 650, 4300, 1850),
    "bottom_left_dc": (120, 1750, 1700, 3150),
    "bottom_center_control": (1550, 1700, 2900, 3150),
    "bottom_right_dc": (2800, 1750, 4300, 3150),
    "notes_legend": (4320, 250, 4950, 1750),
    "left_full": (120, 120, 1800, 3150),
    "center_full": (1450, 120, 3150, 3150),
    "right_full": (2800, 120, 4450, 3150),
    "safety_a_loads_close": (250, 1250, 1450, 2450),
    "normal_center_loads_close": (1480, 850, 2820, 2100),
    "safety_b_loads_close": (2850, 1250, 4050, 2450),
    "dc_a_close": (240, 2350, 1600, 3150),
    "dc_b_close": (2800, 2350, 4200, 3150),
}


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    for source_name, source_path in SOURCES.items():
        with Image.open(source_path) as img:
            for crop_name, box in CROPS.items():
                img.crop(box).save(RESULTS / f"{source_name}__{crop_name}.png")
    print(f"Wrote crops to {RESULTS}")


if __name__ == "__main__":
    main()
