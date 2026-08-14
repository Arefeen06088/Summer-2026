from pathlib import Path

from PIL import Image

BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\8\Raw + wires + components + junctions"
)
RESULTS = BASE / "results"

SOURCES = {
    "raw": BASE / "raw -- synthetic_npp_schematic_improved_local_refined_v3.png",
    "detected": BASE / "detected_components_overlay.png",
    "wire_nodes": BASE / "wire_nodes_overlay.png",
    "wire_mask_overlay": BASE / "wires_mask_overlay.png",
}

CROPS = {
    "top_left": (0, 0, 1400, 1000),
    "top_mid": (1350, 0, 2850, 1000),
    "top_right": (2800, 0, 4200, 1000),
    "middle_left": (0, 900, 1400, 2000),
    "middle_mid": (1350, 900, 2850, 2000),
    "middle_right": (2800, 900, 4200, 2000),
    "bottom_left": (0, 1900, 1400, 3000),
    "bottom_mid": (1350, 1900, 2850, 3000),
    "bottom_right": (2800, 1900, 4200, 3000),
    "left_full": (0, 0, 1600, 3000),
    "center_full": (1300, 0, 3000, 3000),
    "right_full": (2700, 0, 4200, 3000),
    "title_notes_legend": (3000, 2300, 4200, 3000),
    "switchgear_center": (1200, 650, 2850, 1550),
    "dc_control_a": (2450, 1250, 3450, 2550),
    "dc_control_b": (3150, 1250, 4200, 2550),
    "load_a_close": (300, 1450, 1850, 2600),
    "load_b_close": (1900, 1450, 3500, 2600),
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
