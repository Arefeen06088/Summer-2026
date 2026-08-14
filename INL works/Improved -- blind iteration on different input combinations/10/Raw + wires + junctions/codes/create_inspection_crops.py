from __future__ import annotations

from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\10\Raw + wires + junctions")
RESULTS = BASE / "results"
CROPS = RESULTS / "inspection_crops"

SOURCES = {
    "raw": BASE / "raw -- synthetic_nuclear_electrical_schematic_layout_labels_clear.png",
    "wires_overlay": BASE / "wires_mask_overlay.png",
    "nodes_overlay": BASE / "wire_nodes_overlay.png",
}

REGIONS = {
    "top_sources_full": (80, 80, 2600, 470),
    "top_left_source": (80, 80, 1260, 470),
    "top_right_source": (1220, 80, 2600, 470),
    "train_a_upper_4160": (120, 410, 1210, 1050),
    "train_b_upper_4160": (1260, 410, 2360, 1050),
    "train_a_lc_feeders": (420, 880, 1210, 1510),
    "train_b_lc_feeders": (1570, 880, 2360, 1510),
    "train_a_low_loads": (420, 1380, 1210, 1790),
    "train_b_low_loads": (1570, 1380, 2360, 1790),
    "train_a_dc_ups": (140, 1620, 1250, 2060),
    "train_b_dc_ups": (1280, 1620, 2380, 2060),
    "train_a_controls_left": (120, 800, 620, 1510),
    "train_b_controls_left": (1250, 800, 1760, 1510),
    "mcr_annunciator": (2350, 360, 2680, 980),
    "notes": (2680, 610, 3220, 1320),
    "legend_title": (2680, 1320, 3220, 2050),
    "left_full_train": (100, 360, 1260, 2070),
    "right_full_train": (1240, 360, 2400, 2070),
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
