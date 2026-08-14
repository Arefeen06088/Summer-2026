from pathlib import Path

from PIL import Image


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\15\Raw + wires + components + junctions"
)
CROPS = BASE / "codes" / "crops"

SOURCES = {
    "raw": BASE / "raw -- improved_synthetic_nuclear_electrical_schematic.png",
    "detected": BASE / "detected_components_overlay.png",
    "wire_nodes": BASE / "wire_nodes_overlay.png",
    "wire_mask_overlay": BASE / "wires_mask_overlay.png",
}

CROP_BOXES = {
    "top_sources_full": (420, 60, 6100, 950),
    "top_sources_left": (420, 60, 3250, 1200),
    "top_sources_right": (3150, 60, 6100, 1200),
    "div_1a_full": (420, 450, 1830, 3550),
    "div_1b_full": (1760, 450, 3200, 3550),
    "div_2a_full": (3370, 450, 4800, 3550),
    "div_2b_full": (4700, 450, 6200, 3550),
    "div_1a_mcc": (420, 1500, 1830, 2950),
    "div_1b_mcc": (1760, 1500, 3200, 2950),
    "div_2a_mcc": (3370, 1500, 4800, 2950),
    "div_2b_mcc": (4700, 1500, 6200, 2950),
    "div_1a_dc": (420, 3050, 1830, 3650),
    "div_1b_dc": (1760, 3050, 3200, 3650),
    "div_2a_dc": (3370, 3050, 4800, 3650),
    "div_2b_dc": (4700, 3050, 6200, 3650),
    "tie_1_center": (1450, 500, 2350, 1450),
    "tie_2_center": (4400, 500, 5250, 1450),
    "notes_legend": (6200, 430, 7300, 1600),
    "load_schedule": (6200, 1600, 7300, 2450),
    "title_block": (5200, 4100, 7350, 4800),
    "left_half": (350, 80, 3250, 3700),
    "right_half": (3250, 80, 6200, 3700),
}


def main():
    CROPS.mkdir(parents=True, exist_ok=True)
    for source_name, source_path in SOURCES.items():
        image = Image.open(source_path)
        for crop_name, box in CROP_BOXES.items():
            output = CROPS / f"{source_name}__{crop_name}.png"
            image.crop(box).save(output)
            print(output)


if __name__ == "__main__":
    main()
