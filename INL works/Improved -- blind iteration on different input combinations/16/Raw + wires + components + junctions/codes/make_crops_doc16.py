from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\16\Raw + wires + components + junctions")
OUT = BASE / "codes" / "crops"
OUT.mkdir(parents=True, exist_ok=True)

IMAGES = {
    "raw": BASE / "raw -- synthetic_npp_electrical_schematic_revised(1).png",
    "detected": BASE / "detected_components_overlay.png",
    "wire_nodes": BASE / "wire_nodes_overlay.png",
    "wire_mask_overlay": BASE / "wires_mask_overlay.png",
}

CROPS = {
    "top_4160_full": (130, 150, 2900, 820),
    "top_4160_left": (130, 150, 1500, 820),
    "top_4160_right": (1450, 150, 2900, 820),
    "tie_4kv_center": (1350, 290, 1900, 620),
    "main_480_full": (130, 760, 2920, 1780),
    "feeders_11a_12a": (140, 910, 860, 1760),
    "feeders_21a_31a": (850, 910, 1550, 1760),
    "feeders_11b_12b": (1540, 910, 2240, 1760),
    "feeders_21b_31b": (2220, 910, 2920, 1760),
    "tie_480_center": (1340, 760, 1560, 1040),
    "lower_controls_full": (120, 1700, 2920, 2610),
    "lower_controls_left": (120, 1700, 1120, 2580),
    "lower_controls_center": (1050, 1700, 2020, 2620),
    "lower_controls_right": (1960, 1700, 2920, 2580),
    "dc_vital_left": (160, 2050, 1300, 2580),
    "dc_vital_right": (1640, 2050, 2720, 2580),
    "notes_legend": (2970, 180, 3890, 1760),
    "title_block": (2970, 2180, 3890, 2610),
}


def main() -> None:
    for prefix, path in IMAGES.items():
        with Image.open(path) as img:
            for name, box in CROPS.items():
                img.crop(box).save(OUT / f"{prefix}__{name}.png")


if __name__ == "__main__":
    main()
