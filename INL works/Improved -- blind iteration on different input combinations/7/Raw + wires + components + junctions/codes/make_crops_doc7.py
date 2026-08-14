from pathlib import Path

from PIL import Image

BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\7\Raw + wires + components + junctions"
)
RESULTS = BASE / "results"

SOURCES = {
    "raw": BASE / "raw -- synthetic_npp_electrical_schematic_clean (1).png",
    "detected": BASE / "detected_components_and_logical_overlay.png",
    "wire_nodes": BASE / "wire_nodes_overlay.png",
    "wire_mask_overlay": BASE / "wires_mask_overlay.png",
}

CROPS = {
    "top_left_sources": (350, 250, 1900, 1500),
    "top_mid_buses": (1700, 250, 3800, 1500),
    "top_right_sources": (3500, 250, 5700, 1500),
    "load_centers_left": (350, 1450, 2750, 3050),
    "load_centers_right": (3100, 1450, 5650, 3050),
    "dc_control_left": (350, 3000, 2450, 4550),
    "dc_control_right": (3300, 3000, 5650, 4550),
    "control_bottom_cross": (1600, 3600, 5300, 4650),
    "notes": (5750, 400, 7050, 1100),
    "legend": (5750, 1120, 7050, 1700),
    "revision": (5750, 1750, 7050, 2300),
    "title_block": (5650, 3750, 7050, 4650),
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
