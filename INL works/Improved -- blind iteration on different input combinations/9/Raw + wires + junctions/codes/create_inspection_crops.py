from __future__ import annotations

from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\9\Raw + wires + junctions")
RESULTS = BASE / "results"
CROPS = RESULTS / "inspection_crops"

SOURCES = {
    "raw": BASE / "raw -- synthetic_npp_schematic_expanded_clear_refined_v3_reworked.png",
    "wires_overlay": BASE / "wires_mask_overlay.png",
    "nodes_overlay": BASE / "wire_nodes_overlay.png",
}

REGIONS = {
    "top_sources_full": (150, 150, 4300, 620),
    "top_left_sources": (160, 160, 1100, 620),
    "top_center_generator_uat": (980, 160, 2750, 700),
    "top_right_sources": (3150, 160, 4300, 620),
    "train_a_safety_4160": (150, 570, 1580, 1320),
    "normal_aux_4160_480": (1450, 560, 2700, 1520),
    "train_b_safety_4160": (2680, 570, 4150, 1320),
    "train_a_480_loads": (150, 1250, 1600, 2250),
    "normal_aux_loads": (1450, 1180, 2700, 2300),
    "train_b_480_loads": (2680, 1250, 4150, 2250),
    "train_a_mov_panel": (780, 1830, 1580, 2460),
    "train_b_mov_panel": (3350, 1830, 4150, 2460),
    "train_a_dc_control": (150, 2350, 1580, 3100),
    "central_control": (1580, 1980, 2660, 3000),
    "train_b_dc_control": (2680, 2350, 4150, 3100),
    "left_full_system": (150, 520, 1600, 3100),
    "center_full_system": (1450, 520, 2700, 3000),
    "right_full_system": (2680, 520, 4150, 3100),
    "notes_legend": (4300, 410, 4920, 1820),
    "title_block": (4300, 2760, 4920, 3160),
}


def main() -> None:
    CROPS.mkdir(parents=True, exist_ok=True)
    for source_name, source_path in SOURCES.items():
        with Image.open(source_path) as img:
            for region_name, box in REGIONS.items():
                output = CROPS / f"{source_name}__{region_name}.png"
                img.crop(box).save(output)
                print(output)


if __name__ == "__main__":
    main()
