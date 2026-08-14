from pathlib import Path

from PIL import Image


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\19\Raw + wires + components + junctions"
)
OUT = BASE / "codes" / "crops"

SOURCES = {
    "raw": BASE / "raw -- synthetic_npp_electrical_schematic_v3.png",
    "components": BASE / "detected_components_overlay.png",
    "wire_nodes": BASE / "wire_nodes_overlay.png",
    "wires": BASE / "wires_mask_overlay.png",
}

# Coordinates are in original 9200 x 5600 image pixels.
CROPS = {
    "full_working_area": (380, 230, 7750, 4320),
    "top_division_a_4160": (650, 240, 4300, 1180),
    "top_division_b_4160": (4700, 240, 7500, 1180),
    "top_center_tie": (3600, 520, 5000, 1160),
    "mid_division_a_left": (380, 1000, 1900, 3140),
    "mid_division_a_center": (1720, 1000, 3220, 3140),
    "mid_division_a_right": (3050, 1000, 4240, 3140),
    "mid_division_b_left": (4000, 1000, 5320, 3140),
    "mid_division_b_center": (5120, 1000, 6520, 3140),
    "mid_division_b_right": (6320, 1000, 7650, 3140),
    "bottom_control_a": (420, 3180, 4050, 4300),
    "bottom_control_b": (5200, 3180, 7650, 4300),
    "bottom_control_a_detail": (450, 3200, 4000, 4100),
    "bottom_control_b_detail": (5220, 3200, 7600, 4100),
    "division_a_loads_wide": (420, 1030, 4080, 3100),
    "division_b_loads_wide": (4050, 1030, 7600, 3100),
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for source_name, path in SOURCES.items():
        image = Image.open(path)
        for crop_name, box in CROPS.items():
            crop = image.crop(box)
            crop.save(OUT / f"{source_name}__{crop_name}.png")
            if crop_name.endswith("_detail") or crop_name.startswith("mid_"):
                crop.resize((crop.size[0] * 2, crop.size[1] * 2)).save(
                    OUT / f"{source_name}__{crop_name}_2x.png"
                )
    print(f"Wrote crops to {OUT}")


if __name__ == "__main__":
    main()
